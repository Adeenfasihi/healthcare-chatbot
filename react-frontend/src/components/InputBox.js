import React, { useState } from "react";

function InputBox({ onSendMessage }) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    onSendMessage(input);
    setInput(""); // Clear input after sending
  };

  return (
    <div className="input-box">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Describe your symptoms..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default InputBox;
