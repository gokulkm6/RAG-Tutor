import React, { useState, useEffect, useRef } from "react";
import ChatWindow from "./ChatWindow";

const API_BASE = "http://localhost:8000";

function Mascot() {
  const [listening, setListening] = useState(false);
  const [messages, setMessages] = useState([]);
  const recognitionRef = useRef(null);

  // Initialize Speech Recognition
  useEffect(() => {
    if (!("webkitSpeechRecognition" in window || "SpeechRecognition" in window)) {
      alert("Speech Recognition not supported in this browser.");
      return;
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      handleUserInput(transcript);
    };
    recognition.onend = () => setListening(false);
    recognitionRef.current = recognition;
  }, []);

  const startListening = () => {
    if (recognitionRef.current) {
      setListening(true);
      recognitionRef.current.start();
    }
  };

  const handleUserInput = async (text) => {
    setMessages((prev) => [...prev, { role: "user", text }]);
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: text }),
    });
    const data = await res.json();
    setMessages((prev) => [...prev, { role: "assistant", text: data.text, emotion: data.emotion }]);
    speak(data.text);
    triggerEmotion(data.emotion);
  };

  const speak = (text) => {
    if (!("speechSynthesis" in window)) return;
    const utter = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utter);
  };

  const triggerEmotion = (emotion) => {
    const el = document.getElementById("mascot-face");
    el.className = "face " + emotion;
  };

  return (
    <div className="mascot-wrapper">
      <div id="mascot-face" className="face neutral">
        <div className="eyes"></div>
        <div className="mouth"></div>
      </div>
      <button onMouseDown={startListening}>
        {listening ? "🎤 Listening..." : "🎙️ Hold to Talk"}
      </button>
      <ChatWindow messages={messages} />
    </div>
  );
}
export default Mascot;