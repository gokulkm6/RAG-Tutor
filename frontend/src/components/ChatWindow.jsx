import React from "react";

const ChatWindow = ({ messages }) => (
  <div className="chat-box">
    {messages.map((m, i) => (
      <div key={i} className={m.role}>
        <b>{m.role === "user" ? "You: " : "Tutor: "}</b> {m.text}
      </div>
    ))}
  </div>
);
export default ChatWindow;