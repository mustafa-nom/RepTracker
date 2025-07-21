import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const ActivityPage = () => {
  const [legislatorsData, setLegislatorsData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [loadingMore, setLoadingMore] = useState({});
  const location = useLocation();
  const navigate = useNavigate();
  
  const searchParams = new URLSearchParams(location.search);
  const zip = searchParams.get('zip');

  useEffect(() => {
    if (!zip) {
      navigate('/');
      return;
    }
    fetchActivity();
  }, [zip]);

  const fetchActivity = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`http://localhost:5000/activity?zip=${zip}&max_bills=5`);
      if (!response.ok) throw new Error('Failed to fetch activity');
      const data = await response.json();
      
      const legislatorsObj = {};
      data.legislators.forEach(legislator => {
        legislatorsObj[legislator.bioguide_id] = {
          ...legislator,
          isLoading: false
        };
      });
      
      setLegislatorsData(legislatorsObj);
    } catch (err) {
      setError('Failed to fetch legislative activity. Please try again.');
      console.error(err);
    }
    setLoading(false);
  };

  const loadMoreBills = async (bioguideId) => {
    setLoadingMore(prev => ({ ...prev, [bioguideId]: true }));
    
    const legislator = legislatorsData[bioguideId];
    if (!legislator) return;
    
    try {
      const response = await fetch(
        `http://localhost:5000/activity/legislator/${bioguideId}?offset=${legislator.offset}&limit=5`
      );
      if (!response.ok) throw new Error('Failed to fetch more bills');
      const data = await response.json();
      
      setLegislatorsData(prev => ({
        ...prev,
        [bioguideId]: {
          ...prev[bioguideId],
          bills: [...prev[bioguideId].bills, ...data.bills],
          offset: data.offset,
          has_more: data.has_more
        }
      }));
    } catch (err) {
      console.error('Failed to load more bills:', err);
    } finally {
      setLoadingMore(prev => ({ ...prev, [bioguideId]: false }));
    }
  };

  return (
    <>
      <div style={{ 
        backgroundColor: '#F9FAFC', 
        minHeight: '100vh',
        fontFamily: '"Times New Roman", serif'
      }}>
        <div style={{
          background: 'linear-gradient(to right, rgba(24,40,72,0.8), rgba(75,108,183,0.8))',
          color: 'white',
          padding: '3rem 2rem',
          textAlign: 'center'
        }}>
          <h1 style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>
            Legislative Activity
          </h1>
          <p style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>
            Bills sponsored by your representatives in ZIP: {zip}
          </p>
          <button
            onClick={() => navigate('/')}
            style={{
              background: 'white',
              color: '#1d2e8f',
              border: 'none',
              padding: '0.6rem 1.5rem',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '1rem'
            }}
          >
            ← Back to Home
          </button>
        </div>
      </div>

      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '2rem' }}>
        {loading && (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            <div style={{ fontSize: '1.5rem', color: '#1d2e8f' }}>
              Loading legislative activity...
            </div>
            <p style={{ color: '#666', marginTop: '1rem' }}>
              This may take a moment as we fetch the latest data
            </p>
          </div>
        )}

        {error && (
          <div style={{
            background: '#ffebee',
            color: '#c62828',
            padding: '1rem',
            borderRadius: '8px',
            textAlign: 'center'
          }}>
            {error}
          </div>
        )}

        {!loading && !error && Object.keys(legislatorsData).length === 0 && (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            No legislative activity found for this ZIP code.
          </div>
        )}

        {!loading && !error && Object.values(legislatorsData).map((legislator) => (
          <div key={legislator.bioguide_id} style={{
            background: 'white',
            borderRadius: '12px',
            padding: '2rem',
            marginBottom: '2rem',
            boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
          }}>
            <div style={{
              borderBottom: '2px solid #f0f0f0',
              paddingBottom: '1rem',
              marginBottom: '1.5rem'
            }}>
              <h2 style={{ 
                color: '#1d2e8f',
                marginBottom: '0.3rem',
                fontSize: '1.8rem'
              }}>
                {legislator.name}
              </h2>
              <p style={{ color: '#666', margin: 0 }}>
                {legislator.type === 'senator' ? 'U.S. Senator' : 'U.S. Representative'} • 
                Showing {legislator.bills_shown} of {legislator.total_bills} sponsored bills
              </p>
            </div>

            {legislator.bills.map((bill, billIdx) => (
              <div key={billIdx} style={{
                background: '#f8f9fa',
                padding: '1.5rem',
                borderRadius: '8px',
                marginBottom: '1rem'
              }}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'start',
                  marginBottom: '0.8rem'
                }}>
                  <h3 style={{ 
                    margin: 0,
                    color: '#333',
                    fontSize: '1.3rem',
                    flex: 1
                  }}>
                    {bill.title || `${bill.type} ${bill.number}`}
                  </h3>
                  <span style={{
                    background: '#1d2e8f',
                    color: 'white',
                    padding: '0.3rem 0.8rem',
                    borderRadius: '4px',
                    fontSize: '0.85rem',
                    marginLeft: '1rem'
                  }}>
                    {bill.congress}th Congress
                  </span>
                </div>

                <div style={{ marginBottom: '1rem' }}>
                  <span style={{
                    color: '#666',
                    fontSize: '0.9rem',
                    marginRight: '1rem'
                  }}>
                    Bill {bill.type.toUpperCase()} {bill.number}
                  </span>
                  {bill.introducedDate && (
                    <span style={{
                      color: '#666',
                      fontSize: '0.9rem'
                    }}>
                      Introduced: {new Date(bill.introducedDate).toLocaleDateString()}
                    </span>
                  )}
                </div>

                {bill.latestAction && (
                  <div style={{
                    background: '#e8f0fe',
                    padding: '0.8rem',
                    borderRadius: '6px',
                    marginBottom: '1rem'
                  }}>
                    <strong style={{ color: '#1d2e8f' }}>Latest Action:</strong>
                    <p style={{ margin: '0.3rem 0 0 0', fontSize: '0.95rem' }}>
                      {bill.latestAction.text} ({new Date(bill.latestAction.actionDate).toLocaleDateString()})
                    </p>
                  </div>
                )}

                {bill.summary && bill.summary !== "No summary available." && (
                  <div style={{ marginTop: '1rem' }}>
                    <strong style={{ color: '#333' }}>Summary:</strong>
                    <p style={{ 
                      margin: '0.5rem 0 0 0',
                      color: '#555',
                      lineHeight: '1.6'
                    }}>
                      {bill.summary}
                    </p>
                  </div>
                )}

                {bill.url && (
                  <div style={{ marginTop: '1rem' }}>
                    <a 
                      href={bill.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        color: '#1d2e8f',
                        textDecoration: 'none',
                        fontSize: '0.9rem',
                        fontWeight: 'bold'
                      }}
                    >
                      View Full Bill Text →
                    </a>
                  </div>
                )}
              </div>
            ))}

            {legislator.has_more && (
              <div style={{ textAlign: 'center', marginTop: '1rem' }}>
                <button
                  onClick={() => loadMoreBills(legislator.bioguide_id)}
                  disabled={loadingMore[legislator.bioguide_id]}
                  style={{
                    background: legislator.total_bills > 50 ? '#1d2e8f' : '#f0f0f0',
                    color: legislator.total_bills > 50 ? 'white' : '#666',
                    border: 'none',
                    padding: '0.8rem 2rem',
                    borderRadius: '6px',
                    cursor: loadingMore[legislator.bioguide_id] ? 'not-allowed' : 'pointer',
                    fontSize: '0.95rem',
                    opacity: loadingMore[legislator.bioguide_id] ? 0.7 : 1,
                    transition: 'all 0.2s ease'
                  }}
                  onMouseEnter={(e) => {
                    if (!loadingMore[legislator.bioguide_id]) {
                      e.target.style.transform = 'translateY(-1px)';
                      e.target.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
                    }
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.transform = 'translateY(0)';
                    e.target.style.boxShadow = 'none';
                  }}
                >
                  {loadingMore[legislator.bioguide_id] ? (
                    <span>Loading more bills...</span>
                  ) : (
                    <span>
                      Load More Bills ({legislator.offset} of {legislator.total_bills})
                    </span>
                  )}
                </button>

                {legislator.total_bills > 20 && !loadingMore[legislator.bioguide_id] && (
                  <button
                    onClick={() => {
                      const remaining = legislator.total_bills - legislator.offset;
                      if (remaining > 20) {
                        alert(`Loading all ${remaining} remaining bills. This may take a moment...`);
                      }
                      loadMoreBills(legislator.bioguide_id);
                    }}
                    style={{
                      background: 'transparent',
                      color: '#1d2e8f',
                      border: 'none',
                      padding: '0.5rem',
                      cursor: 'pointer',
                      fontSize: '0.85rem',
                      textDecoration: 'underline',
                      marginLeft: '1rem'
                    }}
                  >
                    or load all remaining bills
                  </button>
                )}
              </div>
            )}

            {!legislator.has_more && legislator.bills.length > 0 && (
              <div style={{
                textAlign: 'center',
                marginTop: '1rem',
                color: '#666',
                fontSize: '0.9rem',
                fontStyle: 'italic'
              }}>
                All {legislator.total_bills} bills loaded
              </div>
            )}
          </div>
        ))}
      </div>
    </>
  );
};

export default ActivityPage;
