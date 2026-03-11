import React, { useState } from 'react';
import Home from './components/Home';
import ResumeUpload from './components/ResumeUpload';
import JDInput from './components/JDInput';
import Auth from './components/Auth';
import './styles/main.css';

function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleAuthSuccess = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setActiveTab('home');
  };

  if (!isAuthenticated) {
    return <Auth onAuthSuccess={handleAuthSuccess} />;
  }

  return (
    <div className="App">
      <header className="top-header">
        <div className="header-title-section">
          <h1>AI Resume Analyzer</h1>
          <p className="header-subtitle">Enterprise-grade resume parsing and intelligent job matching solution</p>
        </div>
        <button className="logout-button" onClick={handleLogout}>
          Log out
        </button>
      </header>

      <aside className="sidebar">
        <nav className="sidebar-nav">
          <button 
            className={activeTab === 'home' ? 'nav-item active' : 'nav-item'}
            onClick={() => setActiveTab('home')}
          >
            Home
          </button>
          <button 
            className={activeTab === 'resume' ? 'nav-item active' : 'nav-item'}
            onClick={() => setActiveTab('resume')}
          >
            Resume Analysis
          </button>
          <button 
            className={activeTab === 'jd' ? 'nav-item active' : 'nav-item'}
            onClick={() => setActiveTab('jd')}
          >
            Job description
          </button>
        </nav>
      </aside>

      <div className="content-wrapper">
        <main className="main-content">
          {activeTab === 'home' && <Home onNavigate={setActiveTab} />}
          {activeTab === 'resume' && <ResumeUpload />}
          {activeTab === 'jd' && <JDInput />}
        </main>
      </div>

      <footer className="app-footer">
        <p>© 2026 AI Resume Analyzer. Powered by Advanced NLP & Machine Learning Technology.</p>
      </footer>
    </div>
  );
}

export default App;
