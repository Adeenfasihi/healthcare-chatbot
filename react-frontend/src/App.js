import React, { useState } from "react";
import "./App.css";
import ChatBox from "./components/ChatBox";
import InputBox from "./components/InputBox";
import LanguageSelector from "./components/LanguageSelector";

function App() {
  const [messages, setMessages] = useState([]);
  const [language, setLanguage] = useState("auto");

  const handleSendMessage = (message) => {
    if (!message.trim()) return;

    // Add the user's message
    const userMessage = { text: message, type: "user", detectedLanguage: null };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // Send the message to the backend
    fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, language }),
    })
      .then((res) => res.json())
      .then((data) => {
        // Update the detected language for the last user message
        setMessages((prevMessages) =>
          prevMessages.map((msg, index) =>
            index === prevMessages.length - 1
              ? { ...msg, detectedLanguage: data.detectedLanguage.language }
              : msg
          )
        );

        // Add the bot's message
        const botMessage = { text: data.translatedResponse, type: "bot", targetLanguage: data.targetLanguage.language };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      })
      .catch((err) => {
        console.error("Error:", err);
      });
  };

  return (
    <div className="App">
      <LanguageSelector setLanguage={setLanguage} />
      <ChatBox messages={messages} />
      <InputBox onSendMessage={handleSendMessage} />
    </div>
  );
}

export default App;