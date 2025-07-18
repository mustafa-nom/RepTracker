import React, { useState } from 'react';

const FullBillsPage = ({ bills = [], reps = [], onClose }) => {
  const [filter, setFilter] = useState('');

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
            <span style={{ color: "#1d2e8f" }}>Comprehensive</span>{' '}
            <span style={{ color: "#c62828" }}>Bills View</span>
          </h1>
          <p style={{
            fontSize: "1rem",
            color: "#ddd",
            maxWidth: "600px",
            lineHeight: "1.5",
            marginBottom: "0.5rem",
            textShadow: "2px 2px 4px rgba(0,0,0,0.35)"
          }}>
            Explore a detailed overview of all bills, their impacts, and how your representatives voted.
          </p>
          <a 
            href="/" 
            style={{
              color: "#fff",
              fontStyle: "italic",
              textDecoration: "underline",
              fontSize: "0.9rem",
              transition: "color 0.2s ease"
            }}
            onMouseEnter={(e) => e.target.style.color = '#a8c6ff'}
            onMouseLeave={(e) => e.target.style.color = '#fff'}
          >
            Back to Home
          </a>
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

      {/* close button */}
      <div style={{
        maxWidth: "1200px",
        margin: "2rem auto",
        position: "relative"
      }}>
        <button 
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '0',
            right: '0',
            background: '#c62828',
            color: 'white',
            border: 'none',
            padding: '0.5rem 1rem',
            borderRadius: '4px',
            cursor: 'pointer',
            fontFamily: '"Times New Roman", serif'
          }}
        >
          Close
        </button>
      </div>

      {/* filter and table */}
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 2rem' }}>
        <div style={{ marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <p style={{ fontFamily: '"Times New Roman", serif', margin: 0 }}>
            Detailed view of all bills with voting records
          </p>
          
          <div style={{ position: 'relative' }}>
            <select 
              value={filter} 
              onChange={e => setFilter(e.target.value)}
              style={{ 
                appearance: 'none',
                background: '#1d2e8f',
                color: 'white',
                padding: '0.6rem 2.5rem 0.6rem 1.2rem',
                borderRadius: '6px',
                border: 'none',
                fontSize: '0.9rem',
                cursor: 'pointer',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                fontFamily: '"Times New Roman", serif'
              }}
            >
              <option value="">Filter By</option>
              <option value="Status">Status</option>
              <option value="Impact">Impact</option>
              <option value="RepVotes">Your Reps' Vote</option>
            </select>
            <div style={{
              position: 'absolute',
              right: '1rem',
              top: '50%',
              transform: 'translateY(-50%)',
              pointerEvents: 'none',
              color: 'white',
              fontFamily: '"Times New Roman", serif'
            }}>
              ▼
            </div>
          </div>
        </div>

        <div style={{
          background: 'white',
          borderRadius: '12px',
          boxShadow: '0 6px 16px rgba(0,0,0,0.1)',
          padding: '2rem',
          fontFamily: '"Times New Roman", serif'
        }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#f2f2f2' }}>
                <th style={{ padding: '1rem', textAlign: 'left' }}>Title</th>
                <th style={{ padding: '1rem', textAlign: 'left' }}>Status</th>
                <th style={{ padding: '1rem', textAlign: 'left' }}>Impact</th>
                <th style={{ padding: '1rem', textAlign: 'left' }}>Date</th>
                <th style={{ padding: '1rem', textAlign: 'left' }}>Description</th>
                <th style={{ padding: '1rem', textAlign: 'left' }}>Your Representatives Votes</th>
              </tr>
            </thead>
            <tbody>
            {(bills || []).map((bill, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid #ddd' }}>
                  <td style={{ padding: '1rem' }}>{bill.title}</td>
                  <td style={{ padding: '1rem' }}>{bill.status}</td>
                  <td style={{ padding: '1rem' }}>{bill.impact}</td>
                  <td style={{ padding: '1rem', whiteSpace: 'nowrap' }}>{bill.date}</td>
                  <td style={{ padding: '1rem' }}>
                    {bill.description || 'No description available'}
                  </td>
                  <td style={{ padding: '1rem' }}>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                    {(reps || []).map(rep => {
                        const votedYes = Math.random() > 0.5;
                        return (
                          <span key={rep.name} style={{
                            background: votedYes ? '#c8e6c9' : '#ffcdd2',
                            color: votedYes ? '#004d40' : '#c62828',
                            padding: '0.3rem 0.7rem',
                            borderRadius: '5px',
                            fontSize: '0.8rem',
                            whiteSpace: 'nowrap'
                          }}>
                            {rep.name}: {votedYes ? 'Yes' : 'No'} {rep.party === 'Republican' ? '(R)' : '(D)'}
                          </span>
                        )
                      })}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
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

export default FullBillsPage;
