import React, { useState, useEffect } from 'react';
import Home from './components/Home';
import ResumeUpload from './components/ResumeUpload';
import JDInput from './components/JDInput';
import Auth from './components/Auth';
import Profile from './components/Profile';
import './styles/main.css';

function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [showProfilePage, setShowProfilePage] = useState(false);

  useEffect(() => {
    const checkExistingAuth = () => {
      try {
        const authToken = localStorage.getItem('authToken');
        const userStr = localStorage.getItem('user');
        
        if (authToken && userStr) {
          const user = JSON.parse(userStr);
          setCurrentUser(user);
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.error('Error checking authentication:', error);
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
      } finally {
        setIsCheckingAuth(false);
      }
    };

    checkExistingAuth();
  }, []);

  const handleAuthSuccess = () => {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      const user = JSON.parse(userStr);
      setCurrentUser(user);
    }
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    setCurrentUser(null);
    setIsAuthenticated(false);
    setActiveTab('home');
    setShowProfilePage(false);
  };

  const handleProfileClick = () => {
    setShowProfilePage(true);
  };

  const handleBackToDashboard = () => {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      const user = JSON.parse(userStr);
      setCurrentUser(user);
    }
    setShowProfilePage(false);
  };

  if (isCheckingAuth) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        fontSize: '1.2rem',
        color: '#1e40af'
      }}>
        Loading...
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Auth onAuthSuccess={handleAuthSuccess} />;
  }

  return (
    <div className="App">
      <header className="top-header">
        <div className="header-title-section">
          <h1>AI Resume Analyzer</h1>
          <p className="header-subtitle">
            {currentUser ? `Welcome, ${currentUser.full_name}` : 'Enterprise-grade resume parsing and intelligent job matching solution'}
          </p>
        </div>
        <div className="header-actions">
          <button 
            className="profile-button" 
            onClick={handleProfileClick}
          >
            <div className="profile-avatar">
              {currentUser?.profile_pic ? (
                <img src={currentUser.profile_pic} alt="Profile" style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '50%' }} />
              ) : (
                currentUser?.full_name?.charAt(0).toUpperCase() || 'U'
              )}
            </div>
            <span className="profile-name">{currentUser?.full_name || 'User'}</span>
          </button>
          <button className="logout-button" onClick={handleLogout}>
            Log out
          </button>
        </div>
      </header>

      {showProfilePage ? (
        <Profile currentUser={currentUser} onBack={handleBackToDashboard} />
      ) : (
        <>
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
              <div style={{ display: activeTab === 'home' ? 'block' : 'none' }}>
                <Home onNavigate={setActiveTab} />
              </div>
              <div style={{ display: activeTab === 'resume' ? 'block' : 'none' }}>
                <ResumeUpload />
              </div>
              <div style={{ display: activeTab === 'jd' ? 'block' : 'none' }}>
                <JDInput />
              </div>
            </main>
          </div>
        </>
      )}

      <footer className="app-footer">
        <p>© 2026 AI Resume Analyzer. Powered by Advanced NLP & Machine Learning Technology.</p>
      </footer>
    </div>
  );
}

export default App;
