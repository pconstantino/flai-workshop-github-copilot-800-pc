import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
    console.log('Workouts API endpoint:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsList = data.results || data;
        setWorkouts(workoutsList);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
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
          <p className="mt-3 text-muted">Loading workouts...</p>
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
      <h1 className="page-title">Workout Suggestions</h1>
      {workouts.length === 0 ? (
        <div className="alert alert-info" role="alert">
          <h4 className="alert-heading">No Workouts Available</h4>
          <p>No workout suggestions are available at this time. Check back later!</p>
        </div>
      ) : (
        <div className="row">
          {workouts.map(workout => {
            const difficultyColor = 
              workout.difficulty === 'Easy' ? 'success' :
              workout.difficulty === 'Medium' ? 'warning' : 'danger';
            
            return (
              <div key={workout._id} className="col-md-6 mb-4">
                <div className="card h-100">
                  <div className="card-header bg-primary text-white">
                    <h5 className="card-title mb-0">{workout.name}</h5>
                  </div>
                  <div className="card-body">
                    <p className="card-text">{workout.description}</p>
                    <ul className="list-group list-group-flush mt-3">
                      <li className="list-group-item d-flex justify-content-between align-items-center">
                        <strong>Activity Type:</strong>
                        <span className="badge bg-info">{workout.activity_type}</span>
                      </li>
                      <li className="list-group-item d-flex justify-content-between align-items-center">
                        <strong>Difficulty:</strong>
                        <span className={`badge bg-${difficultyColor}`}>{workout.difficulty}</span>
                      </li>
                      <li className="list-group-item d-flex justify-content-between align-items-center">
                        <strong>Duration:</strong>
                        <span>{workout.duration} minutes</span>
                      </li>
                      <li className="list-group-item d-flex justify-content-between align-items-center">
                        <strong>Est. Calories:</strong>
                        <span className="badge bg-success">{workout.calories_estimate}</span>
                      </li>
                    </ul>
                  </div>
                  <div className="card-footer bg-transparent text-center">
                    <button className="btn btn-primary btn-sm">Start Workout</button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default Workouts;
