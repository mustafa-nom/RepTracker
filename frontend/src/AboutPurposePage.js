import React from 'react';

const AboutPurposePage = ({ onClose }) => {
  return (
    <div style={{
      backgroundColor: '#F9FAFC',
      minHeight: '100vh',
      overflowX: 'hidden',
      fontFamily: '"Times New Roman", serif'
    }}>
      {/* hero section */}
      <div style={{
        position: "relative",
        backgroundImage: `
          linear-gradient(to right, rgba(24,40,72,0.6), rgba(75,108,183,0.6)),
          url('https://upload.wikimedia.org/wikipedia/commons/a/a3/United_States_Capitol_west_front_edit2.jpg')
        `,
        backgroundSize: "cover",
        backgroundPosition: "center",
        color: "white",
        padding: "6rem 2rem",
        overflow: "hidden"
      }}>
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
        <div style={{ maxWidth: "700px", marginLeft: "8%", textAlign: "left" }}>
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
            <span style={{ color: "#c62828" }}>Purpose</span>
          </h1>
          <p style={{
            fontSize: "1rem",
            color: "#ddd",
            maxWidth: "600px",
            lineHeight: "1.5",
            marginBottom: "1rem",
            textShadow: "2px 2px 4px rgba(0,0,0,0.35)"
          }}>
            Why this platform exists and the issue it aims to solve.
          </p>
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

      {/* centered purpose card */}
      <div style={{ maxWidth: "900px", margin: "3rem auto", padding: "0 2rem" }}>
        <div style={{
          background: "white",
          borderRadius: "12px",
          boxShadow: "0 6px 16px rgba(0,0,0,0.1)",
          padding: "2rem"
        }}>
          <div style={{ textAlign: "center" }}>
            <h2 style={{ marginBottom: "1rem" }}>Holding Elected Officials Accountable</h2>
          </div>
          <p style={{ fontSize: "1.1rem", color: "#555", marginBottom: "1.2rem", lineHeight: "1.6" }}>
            Over <strong>80%</strong> of Americans say they often feel disconnected from what Congress is doing. 
            With thousands of bills proposed each year, it's challenging to keep track of how your representatives 
            are voting on issues that matter most to you and your community.
          </p>
          <p style={{ fontSize: "1.1rem", color: "#555", marginBottom: "1.2rem", lineHeight: "1.6" }}>
            Our platform bridges that gap by making it easy to see exactly how your local lawmakers vote, 
            empowering you to make informed decisions and engage in democracy.
          </p>
          <p style={{ fontSize: "1.1rem", color: "#555", lineHeight: "1.6" }}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed facilisis nunc ut purus fermentum, 
            non bibendum turpis porttitor. Nulla facilisi. Integer dictum nisi vitae elit malesuada, 
            sit amet hendrerit urna interdum. Ut sed odio at elit mollis elementum et nec sapien.
          </p>
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

export default AboutPurposePage;
