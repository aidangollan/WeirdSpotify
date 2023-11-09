import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SearchPage from './pages/SearchPage';
import LoginPage from './pages/LoginPage';
import './styles.css';

function App() {
    return (
        <Router>
            <div className="App">
              <Routes>
                  <Route path="/" element={<LoginPage />} />
                  <Route path="/search" element={<SearchPage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;