import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;
    console.log('Teams API endpoint:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const teamsList = data.results || data;
        setTeams(teamsList);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching teams:', error);
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
          <p className="mt-3 text-muted">Loading teams...</p>
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
      <h1 className="page-title">Teams</h1>
      {teams.length === 0 ? (
        <div className="alert alert-info" role="alert">
          <h4 className="alert-heading">No Teams Yet</h4>
          <p>No teams have been created yet. Check back later!</p>
        </div>
      ) : (
        <div className="row">
          {teams.map(team => (
            <div key={team._id} className="col-md-4 mb-4">
              <div className="card h-100">
                <div className="card-header bg-primary text-white">
                  <h5 className="card-title mb-0">{team.name}</h5>
                </div>
                <div className="card-body">
                  <p className="card-text">{team.description}</p>
                  <div className="mt-3">
                    <span className="badge bg-success">
                      <i className="bi bi-people-fill"></i> {team.member_count || 0} Members
                    </span>
                  </div>
                </div>
                <div className="card-footer bg-transparent">
                  <small className="text-muted">
                    <i className="bi bi-calendar"></i> Created: {new Date(team.created_at).toLocaleDateString()}
                  </small>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Teams;
