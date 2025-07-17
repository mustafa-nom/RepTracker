import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  // mock data for representatives since we're not fetching real data yet
  const mockReps = [
    {
      name: "Rep. Glenn Thompson",
      district: "PA-15",
      term: "2019-2021",
      party: "Republican",
      photo: "https://via.placeholder.com/80"
    },
    {
      name: "Rep. Sarah Williams",
      district: "NY-03",
      term: "2021-2023",
      party: "Democrat",
      photo: "https://via.placeholder.com/80"
    },
    {
      name: "Rep. Alex Martinez",
      district: "CA-12",
      term: "2018-2020",
      party: "Republican",
      photo: "https://via.placeholder.com/80"
    }
  ];

  // mock data for bills to show how they'd display
  const mockBills = [
    { title: "Clean Energy Act", status: "Passed", impact: "High", date: "2025-05-10" },
    { title: "Healthcare Expansion", status: "Failed", impact: "Low", date: "2025-04-21" },
    { title: "Tax Reform Bill", status: "Passed", impact: "High", date: "2025-03-30" },
    { title: "Education Grant Funding", status: "Pending", impact: "Medium", date: "2025-02-15" }
  ];

  const [filter, setFilter] = useState('');
  const [zip, setZip] = useState('');
  const [reps, setReps] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // makes anchor links scroll smoothly instead of jumping
  useEffect(() => {
    const handleSmoothScroll = (e) => {
      if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      }
    };
    document.addEventListener('click', handleSmoothScroll);
    return () => document.removeEventListener('click', handleSmoothScroll);
  }, []);

  // Fetch representatives from backend
  const fetchReps = async () => {
    setLoading(true);
    setError('');
    setReps([]);
    try {
      const response = await fetch(`http://localhost:5000/representatives?zip=${zip}`);
      if (!response.ok) throw new Error('Failed to fetch representatives');
      const data = await response.json();
      setReps(data.results || []);
    } catch (err) {
      setError('Failed to fetch representatives.');
      setReps([]);
    }
    setLoading(false);
  };

  return (
    <div style={{ fontFamily: '"Times New Roman", serif' }}>
      {/* hero section with search box - first thing users see */}
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
        <div style={{ maxWidth: "500px", marginLeft: "8%", textAlign: "left" }}>
          <h1 style={{
            fontSize: "4.3rem",
            fontWeight: "normal",
            whiteSpace: "nowrap",
            marginBottom: "0rem",
            fontStyle: "italic",
            fontFamily: "'Times New Roman', cursive",
            textShadow: "2px 2px 4px rgba(0,0,0,0.35)"
          }}>
            <span style={{ color: "#1d2e8f" }}>Representative</span>{' '}
            <span style={{ color: "#c62828" }}>Tracker</span>
          </h1>
          <p style={{
            fontSize: "1rem",
            color: "#ddd",
            maxWidth: "450px",
            lineHeight: "1.5",
            marginBottom: "3rem",
            textShadow: "2px 2px 4px rgba(0,0,0,0.35)"
          }}>
            Many Americans vote for congressmen and entrust them to make decisions on their behalf,
            but can't always track every bill their congressmen vote on. This tool helps you stay informed.
          </p>
          <div style={{
            background: "white",
            color: "#333",
            borderRadius: "10px",
            padding: "1rem 1.5rem",
            boxShadow: "0 4px 12px rgba(0,0,0,0.25)",
            width: "80%"
          }}>
            <h2 style={{ color: "#1d2e8f", fontSize: "1.2rem", marginBottom: "5px" }}>Find your Representative</h2>
            <p style={{ margin: "0.3rem 0 0.8rem 0", fontSize: "0.75rem" }}>Hold Your Representative Accountable</p>
            <div style={{ display: "flex", margin: "0.5rem 0" }}>
              <input
                type="text"
                placeholder="Input U.S. Zip Code"
                value={zip}
                onChange={e => setZip(e.target.value)}
                style={{
                  flex: 1,
                  padding: "0.5rem 1rem",
                  border: "1px solid #ccc",
                  borderTopLeftRadius: "4px",
                  borderBottomLeftRadius: "4px",
                  fontSize: "1rem",
                  outline: "none"
                }}
              />
              <button
                style={{
                  background: "#c62828",
                  color: "white",
                  border: "none",
                  padding: "0 1.2rem",
                  fontSize: "1rem",
                  borderTopRightRadius: "4px",
                  borderBottomRightRadius: "4px",
                  cursor: "pointer"
                }}
                onClick={fetchReps}
                disabled={loading || !zip}
              >Search</button>
            </div>
            <p style={{ fontSize: "0.65rem", color: "#777", margin: 0 }}>Never stored, saved, or sold.</p>
            {loading && <div style={{ color: '#c62828', marginTop: '0.5rem' }}>Loading...</div>}
            {error && <div style={{ color: '#c62828', marginTop: '0.5rem' }}>{error}</div>}
          </div>
        </div>
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Flag-map_of_the_United_States.svg/2560px-Flag-map_of_the_United_States.svg.png"
          alt="USA flag map"
          style={{
            position: "absolute",
            right: "8%",
            bottom: "10%",
            width: "40%",
            transform: "rotate(-20deg) scale(1)",
            opacity: 0.9,
            filter: "drop-shadow(4px 4px 8px rgba(0,0,0,0.4))"
          }}
        />
      </div>

      {/* shows the user's local representatives in cards */}
      <div style={{ background: "#F9FAFC", padding: "3rem 2rem" }}>
        <div style={{ maxWidth: "1100px", margin: "0 auto" }}>
          <h2>Your Representatives</h2>
          <p>See their office, party and photo</p>
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
            gap: "2rem",
            marginTop: "2rem"
          }}>
            {(reps.length > 0 ? reps : mockReps).map((rep, idx) => {
              const emblem = rep.party === "Republican"
                ? "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Republicanlogo.svg/1200px-Republicanlogo.svg.png"
                : "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/DemocraticLogo.svg/1200px-DemocraticLogo.svg.png";
              return (
                <div key={idx} style={{
                  background: "white",
                  borderRadius: "12px",
                  padding: "1.5rem",
                  boxShadow: "0 6px 16px rgba(0,0,0,0.1)",
                  display: "flex",
                  alignItems: "center",
                  gap: "1.2rem"
                }}>
                  <img src={rep.photo_url || rep.photo} alt={`${rep.name} portrait`}
                    style={{ width: "60px", height: "60px", borderRadius: "50%" }}
                  />
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: "1.3rem", marginBottom: "0.2rem" }}>{rep.name}</div>
                    {rep.district && rep.term && (
                      <div style={{ fontSize: "0.95rem", color: "#777" }}>{rep.district} • {rep.term}</div>
                    )}
                    <div style={{ marginTop: "0.8rem", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                      <img src={emblem} alt={`${rep.party} emblem`} style={{ width: "25px", height: "25px" }} />
                      <div style={{ fontSize: "0.85rem", color: "#777" }}>{rep.party}</div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
      {/*
      highlights important bills at the top bc they're most relevant ?
      <div style={{ background: "#F9FAFC", padding: "3rem 2rem" }}>
        <div style={{ maxWidth: "1100px", margin: "0 auto" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <h2>Key Local Bills</h2>
              <p>See how these bills impact your community</p>
            </div>
            <a href="#all-bills" style={{
              background: "#1d2e8f",
              color: "white",
              padding: "0.6rem 1.2rem",
              borderRadius: "6px",
              fontSize: "0.9rem",
              textDecoration: "none",
              height: "fit-content"
            }}>View All Bills</a>
          </div>
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(400px, 1fr))",
            gap: "2rem",
            marginTop: "2rem"
          }}>
            {[1, 2].map((bill) => (
              <div key={bill} style={{
                background: "white",
                borderRadius: "12px",
                boxShadow: "0 6px 16px rgba(0,0,0,0.1)",
                padding: "1.5rem",
                display: "flex",
                flexDirection: "column"
              }}>
                <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1rem" }}>
                  <span style={{
                    background: "#d1c4e9",
                    color: "#512da8",
                    padding: "0.2rem 0.6rem",
                    borderRadius: "4px",
                    fontSize: "0.8rem"
                  }}>High Impact</span>
                  <span style={{
                    background: "#c8e6c9",
                    color: "#004d40",
                    padding: "0.2rem 0.6rem",
                    borderRadius: "4px",
                    fontSize: "0.8rem"
                  }}>Passed</span>
                </div>
                <h3 style={{ margin: "0 0 0.5rem 0" }}>Infrastructure Investment and Jobs Act</h3>
                <p style={{ fontSize: "0.95rem", color: "#555", marginBottom: "0.8rem" }}>
                  Massive investment in roads, bridges, and broadband nationwide
                </p>
                <p style={{ fontSize: "0.9rem", color: "#777", marginBottom: "1rem" }}>
                  This infrastructure package brings improvements to transportation, internet access, and public works, with substantial benefits for your area.
                </p>
                <div style={{
                  background: "#e8f0fe",
                  padding: "0.8rem",
                  borderRadius: "8px",
                  fontSize: "0.9rem",
                  marginBottom: "1rem"
                }}>
                  <strong style={{ color: "#1d2e8f" }}>Impact on You:</strong> $27B for local state
                </div>
                <span style={{ fontSize: "0.85rem", color: "#777" }}>
                  Your Supporting Reps: <span style={{ color: "#2E7D32" }}>{mockReps.map(r => r.name).join(', ')}</span>
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>*/}

      {/*
      <div id="all-bills" style={{ background: "#F9FAFC", padding: "3rem 2rem", fontFamily: '"Times New Roman", serif' }}>
        <div style={{ maxWidth: "1100px", margin: "0 auto" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <h2 style={{ fontFamily: '"Times New Roman", serif', marginBottom: "0.5rem" }}>All Bills</h2>
              <p style={{ fontFamily: '"Times New Roman", serif', margin: 0 }}>Explore all local and national bills affecting your area.</p>
            </div>
            <div style={{ position: "relative" }}>
              <select 
                value={filter} 
                onChange={e => setFilter(e.target.value)}
                style={{ 
                  appearance: "none",
                  background: "#1d2e8f",
                  color: "white",
                  padding: "0.6rem 2.5rem 0.6rem 1.2rem",
                  borderRadius: "6px",
                  border: "none",
                  fontSize: "0.9rem",
                  cursor: "pointer",
                  boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
                  fontFamily: '"Times New Roman", serif'
                }}
              >
                <option value="">Filter By</option>
                <option value="Status">Status</option>
                <option value="Impact">Impact</option>
                <option value="RepVotes">Your Reps' Vote</option>
              </select>
              <div style={{
                position: "absolute",
                right: "1rem",
                top: "50%",
                transform: "translateY(-50%)",
                pointerEvents: "none",
                color: "white",
                fontFamily: '"Times New Roman", serif'
              }}>
                ▼
              </div>
            </div>
          </div>
          <div style={{
            background: "white",
            marginTop: "2rem",
            borderRadius: "12px",
            boxShadow: "0 6px 16px rgba(0,0,0,0.1)",
            padding: "2rem",
            fontFamily: '"Times New Roman", serif'
          }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontFamily: '"Times New Roman", serif' }}>
              <thead>
                <tr style={{ background: "#f2f2f2" }}>
                  <th style={{ padding: "0.8rem", textAlign: "left", fontFamily: '"Times New Roman", serif' }}>Title</th>
                  <th style={{ padding: "0.8rem", textAlign: "left", fontFamily: '"Times New Roman", serif' }}>Status</th>
                  <th style={{ padding: "0.8rem", textAlign: "left", fontFamily: '"Times New Roman", serif' }}>Impact</th>
                  <th style={{ padding: "0.8rem", textAlign: "left", fontFamily: '"Times New Roman", serif' }}>Date</th>
                  <th style={{ padding: "0.8rem", textAlign: "left", fontFamily: '"Times New Roman", serif' }}>Your Representatives Votes</th>
                </tr>
              </thead>
              <tbody>
                {mockBills.map((bill, idx) => (
                  <tr key={idx} style={{ borderBottom: "1px solid #ddd" }}>
                    <td style={{ padding: "0.8rem", fontFamily: '"Times New Roman", serif' }}>{bill.title}</td>
                    <td style={{ padding: "0.8rem", fontFamily: '"Times New Roman", serif' }}>{bill.status}</td>
                    <td style={{ padding: "0.8rem", fontFamily: '"Times New Roman", serif' }}>{bill.impact}</td>
                    <td style={{ padding: "0.8rem", fontFamily: '"Times New Roman", serif' }}>{bill.date}</td>
                    <td style={{ padding: "0.8rem", fontFamily: '"Times New Roman", serif' }}>
                      <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
                        {mockReps.map(rep => {
                          const votedYes = Math.random() > 0.5;
                          return (
                            <span key={rep.name} style={{
                              background: votedYes ? "#c8e6c9" : "#ffcdd2",
                              color: votedYes ? "#004d40" : "#c62828",
                              padding: "0.2rem 0.6rem",
                              borderRadius: "4px",
                              fontSize: "0.8rem"
                            }}>
                              {rep.name}: {votedYes ? "Yes" : "No"} {rep.party === "Republican" ? "(R)" : "(D)"}
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
      </div>*/}

      
      {/* simple footer with voter registration link */}
      <div style={{
        background: "#f5f5f5",
        padding: "2rem",
        textAlign: "center"  
      }}>
        <a href="https://www.usa.gov/voter-registration" target='_blank' rel="noopener noreferrer"
          style={{ 
            color: "#c62828",
            fontSize: "1rem",  
          }}>Register to Vote Today!</a>
      </div>
    </div>
  );
}

export default App;