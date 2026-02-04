import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Users from './components/Users';
import Activities from './components/Activities';
import Teams from './components/Teams';
import Leaderboard from './components/Leaderboard';
import Workouts from './components/Workouts';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              <img src="/octofitapp-small.svg" alt="OctoFit Logo" className="navbar-logo" />
              <strong>OctoFit Tracker</strong>
            </Link>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                <li className="nav-item">
                  <Link className="nav-link" to="/users">
                    Users
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">
                    Activities
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">
                    Teams
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">
                    Leaderboard
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">
                    Workouts
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <div className="content">
          <Routes>
            <Route path="/" element={
              <div className="container mt-5 text-center">
                <h1>Welcome to OctoFit Tracker</h1>
                <p className="lead">Track your fitness journey and compete with your team!</p>
                <div className="row mt-4">
                  <div className="col-md-3">
                    <Link to="/users" className="text-decoration-none">
                      <div className="card card-hover">
                        <div className="card-body">
                          <h5 className="card-title">Users</h5>
                          <p className="card-text">View and manage user profiles</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-3">
                    <Link to="/activities" className="text-decoration-none">
                      <div className="card card-hover">
                        <div className="card-body">
                          <h5 className="card-title">Activities</h5>
                          <p className="card-text">Log your workouts and monitor your progress</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-3">
                    <Link to="/teams" className="text-decoration-none">
                      <div className="card card-hover">
                        <div className="card-body">
                          <h5 className="card-title">Teams</h5>
                          <p className="card-text">Collaborate and compete with others</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-3">
                    <Link to="/leaderboard" className="text-decoration-none">
                      <div className="card card-hover">
                        <div className="card-body">
                          <h5 className="card-title">Leaderboard</h5>
                          <p className="card-text">See how you rank against others</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                </div>
              </div>
            } />
            <Route path="/users" element={<Users />} />
            <Route path="/activities" element={<Activities />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/workouts" element={<Workouts />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
