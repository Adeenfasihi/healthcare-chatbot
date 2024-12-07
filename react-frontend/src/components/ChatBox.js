import React from "react";

function ChatBox({ messages }) {
  return (
    <div className="chat-box">
      {messages.map((msg, index) => (
        <div key={index} className={`message ${msg.type === "user" ? "user-message" : "bot-message"}`}>
          {msg.text}
          {msg.type === "user" && msg.detectedLanguage && (
            <div className="detected-language">
              <small>Language: {msg.detectedLanguage.toUpperCase()}</small>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default ChatBox;


// import React from "react";

// function ChatBox({ messages }) {
//   return (
//     <div className="chat-box">
//       {messages.map((msg, index) => (
//         <div key={index} className={`message ${msg.type === "user" ? "user-message" : "bot-message"}`}>
//           {msg.text}
//           {msg.type === "user" && msg.detectedLanguage && (
//             <div className="detected-language">
//               <small>Language: {msg.detectedLanguage.toUpperCase()}</small>
//             </div>
//           )}
//         </div>
//       ))}
//     </div>
//   );
// }

// export default ChatBox;
