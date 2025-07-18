import React, { useState } from 'react';

const ChatbotPage = ({ onClose }) => {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi there! How can I help you stay informed today?" }
  ]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { sender: "user", text: input }]);
    setTimeout(() => {
      setMessages(prev => [...prev, { sender: "bot", text: "Thanks for your message. We'll get back to you shortly!" }]);
    }, 800);
    setInput("");
  };

  return (
    <div style={{
      backgroundColor: '#F9FAFC',
      minHeight: '100vh',
      overflowX: 'hidden',
      fontFamily: '"Times New Roman", serif'
    }}>
      {/* Hero section */}
      <div style={{
        position: "relative",
        backgroundImage: `
          linear-gradient(to right, rgba(24,40,72,0.6), rgba(75,108,183,0.6)),
          url('https://upload.wikimedia.org/wikipedia/commons/a/a3/United_States_Capitol_west_front_edit2.jpg')
        `,
        backgroundSize: "cover",
        backgroundPosition: "center",
        color: "white",
        padding: "6rem 2rem 4rem",
        overflow: "hidden"
      }}>
        {/* back to hone button */}
        <div style={{ maxWidth: "500px", marginLeft: "8%", textAlign: "left" }}>
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Seal_of_the_United_States_House_of_Representatives.svg/1024px-Seal_of_the_United_States_House_of_Representatives.svg.png"
            alt="U.S. House Seal"
            style={{
              position: "absolute",
              top: "4rem",
              left: "3rem",
              width: "70px",
              height: "70px",
              opacity: 0.95
            }}
          />
          <h1 style={{
            fontSize: "4rem",
            fontWeight: "normal",
            whiteSpace: "nowrap",
            marginBottom: "0.5rem",
            fontStyle: "italic",
            fontFamily: "'Times New Roman', cursive",
            textShadow: "2px 2px 4px rgba(0,0,0,0.35)"
          }}>
            <span style={{ color: "#1d2e8f" }}>Our</span>{' '}
            <span style={{ color: "#c62828" }}>Chatbot</span>
          </h1>
          <p style={{
            fontSize: "1rem",
            color: "#ddd",
            maxWidth: "600px",
            lineHeight: "1.5",
            marginBottom: "1rem",
            textShadow: "2px 2px 4px rgba(0,0,0,0.35)"
          }}>
            Ask your questions about Congress, bills, and more.
          </p>
          {/* link */}
          <span 
            onClick={onClose}
            style={{
              color: "#fff",
              fontStyle: "italic",
              cursor: "pointer",
              transition: "color 0.2s ease",
              fontSize: "0.9rem",
              textDecoration: "underline"
            }}
            onMouseEnter={(e) => e.target.style.color = '#a8c6ff'}
            onMouseLeave={(e) => e.target.style.color = '#fff'}
          >
            Back to Home
          </span>
        </div>
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Flag-map_of_the_United_States.svg/2560px-Flag-map_of_the_United_States.svg.png"
          alt="USA flag map"
          style={{
            position: "absolute",
            right: "8%",
            bottom: "10%",
            width: "30%",
            transform: "rotate(-20deg) scale(1)",
            opacity: 0.9,
            filter: "drop-shadow(4px 4px 8px rgba(0,0,0,0.4))"
          }}
        />
      </div>

      {/* Chatbot UI */}
      <div style={{ maxWidth: "800px", margin: "3rem auto", padding: "0 2rem" }}>
        <div style={{
          backgroundColor: "white",
          borderRadius: "12px",
          boxShadow: "0 6px 16px rgba(0,0,0,0.1)",
          padding: "2rem",
          display: "flex",
          flexDirection: "column",
          height: "300px"
        }}>
          <div style={{
            flex: 1,
            overflowY: "auto",
            marginBottom: "1rem",
            paddingRight: "0.5rem"
          }}>
            {messages.map((msg, i) => (
              <div key={i} style={{
                textAlign: msg.sender === "user" ? "right" : "left",
                marginBottom: "0.75rem"
              }}>
                <span style={{
                  display: "inline-block",
                  padding: "0.6rem 1rem",
                  backgroundColor: msg.sender === "user" ? "#c62828" : "#e3e8f8",
                  color: msg.sender === "user" ? "white" : "#333",
                  borderRadius: "16px",
                  maxWidth: "70%",
                  fontSize: "1rem"
                }}>
                  {msg.text}
                </span>
              </div>
            ))}
          </div>
          <div style={{ display: "flex" }}>
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === "Enter" && handleSend()}
              placeholder="Type your message..."
              style={{
                flex: 1,
                padding: "0.8rem",
                borderRadius: "8px",
                border: "1px solid #ccc",
                marginRight: "0.5rem",
                fontFamily: "inherit",
                fontSize: "1rem"
              }}
            />
            <button
              onClick={handleSend}
              style={{
                backgroundColor: "#1d2e8f",
                color: "white",
                border: "none",
                borderRadius: "8px",
                padding: "0.8rem 1.2rem",
                fontSize: "1rem",
                cursor: "pointer"
              }}
            >
              Send
            </button>
          </div>
        </div>
      </div>

      {/* footer */}
      <div style={{
        background: "#f5f5f5",
        padding: "2rem",
        textAlign: "center",
        marginTop: "3rem"
      }}>
        <a href="https://www.usa.gov/voter-registration" target="_blank" rel="noopener noreferrer"
          style={{ color: "#c62828", fontSize: "1rem" }}>
          Register to Vote Today!
        </a>
      </div>
    </div>
  );
};

export default ChatbotPage;