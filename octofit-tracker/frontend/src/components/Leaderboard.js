import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
    console.log('Leaderboard API endpoint:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardList = data.results || data;
        setLeaderboard(leaderboardList);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3 text-muted">Loading leaderboard...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <h1 className="page-title">Leaderboard</h1>
      <div className="card">
        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-striped table-hover mb-0">
              <thead className="table-dark">
                <tr>
                  <th>Rank</th>
                  <th>User</th>
                  <th>Team</th>
                  <th>Total Calories</th>
                  <th>Activities</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="text-center text-muted py-4">
                      No leaderboard data available
                    </td>
                  </tr>
                ) : (
                  leaderboard.map((entry, index) => {
                    const rankClass = index === 0 ? 'text-warning' : index === 1 ? 'text-secondary' : index === 2 ? 'text-bronze' : '';
                    return (
                      <tr key={entry._id}>
                        <td>
                          <strong className={rankClass}>#{index + 1}</strong>
                        </td>
                        <td><strong>{entry.user_name}</strong></td>
                        <td><span className="badge bg-info">{entry.team}</span></td>
                        <td>
                          <span className="badge bg-success fs-6">{entry.total_calories}</span>
                        </td>
                        <td>{entry.total_activities || 0}</td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Leaderboard;
