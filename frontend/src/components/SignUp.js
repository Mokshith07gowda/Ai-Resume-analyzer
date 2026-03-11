import React, { useState, useEffect } from 'react';

function SignUp({ onSwitchToSignIn, onSignUpSuccess }) {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.fullName) {
      newErrors.fullName = 'Full name is required';
    } else if (formData.fullName.length < 2) {
      newErrors.fullName = 'Name must be at least 2 characters';
    }

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          full_name: formData.fullName,
          email: formData.email,
          password: formData.password
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Registration failed');
      }

      console.log('Registration successful:', data);
      
      localStorage.setItem('user', JSON.stringify(data));
      
      onSignUpSuccess && onSignUpSuccess();
      
    } catch (error) {
      console.error('Registration error:', error);
      setErrors({
        email: error.message || 'Registration failed. Please try again.'
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="landing-container">
      <div className="landing-hero">
        <div className="landing-nav">
          <div className="landing-logo">
            <h1>AI Resume Analyzer</h1>
          </div>
          <div className="landing-nav-buttons">
            <button onClick={onSwitchToSignIn} className="nav-signin-button">Sign In</button>
          </div>
        </div>

        <div className="landing-content">
          <div className="landing-left">
            <div className="landing-text-content">
              <h2 className="landing-title">
                Start Your Journey to <span className="highlight">Better Career</span> Opportunities
              </h2>
              <p className="landing-subtitle">
                Join thousands of professionals who have improved their resumes and landed their dream jobs. 
                Create your free account today and unlock AI-powered resume analysis.
              </p>

              <div className="landing-features">
                <div className="feature-item">
                  <span className="feature-icon">✓</span>
                  <span>Comprehensive resume analysis</span>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">✓</span>
                  <span>Personalized recommendations</span>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">✓</span>
                  <span>Track your progress over time</span>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">✓</span>
                  <span>Industry-specific insights</span>
                </div>
              </div>
            </div>
          </div>

          <div className="landing-right">
            <div className="auth-card">
              <div className="auth-header">
                <h2>Create Account</h2>
                <p>Join AI Resume Analyzer to get started</p>
              </div>

              <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="fullName">Full Name</label>
            <input
              type="text"
              id="fullName"
              name="fullName"
              value={formData.fullName}
              onChange={handleChange}
              className={errors.fullName ? 'input-error' : ''}
              placeholder="Enter your full name"
            />
            {errors.fullName && <span className="error-text">{errors.fullName}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? 'input-error' : ''}
              placeholder="Enter your email"
            />
            {errors.email && <span className="error-text">{errors.email}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="password-input-container">
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className={errors.password ? 'input-error' : ''}
                placeholder="Create a password"
              />
              <button
                type="button"
                className="password-toggle-btn"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            {errors.password && <span className="error-text">{errors.password}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <div className="password-input-container">
              <input
                type={showConfirmPassword ? "text" : "password"}
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className={errors.confirmPassword ? 'input-error' : ''}
                placeholder="Confirm your password"
              />
              <button
                type="button"
                className="password-toggle-btn"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                aria-label={showConfirmPassword ? "Hide password" : "Show password"}
              >
                {showConfirmPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            {errors.confirmPassword && <span className="error-text">{errors.confirmPassword}</span>}
          </div>

                <button type="submit" className="auth-submit-button" disabled={isLoading}>
                  {isLoading ? 'Creating Account...' : 'Sign Up'}
                </button>
              </form>

              <div className="auth-footer">
                <p>Already have an account? <button onClick={onSwitchToSignIn} className="switch-auth-link">Sign In</button></p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <section className="landing-section features-section">
        <div className="section-container">
          <h2 className="section-title">Unlock Your Potential</h2>
          <p className="section-subtitle">Join the community that's redefining career success</p>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon-box">⚡</div>
              <h3>Instant Analysis</h3>
              <p>Get immediate feedback on your resume with real-time parsing and analysis in under 10 seconds.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-box">🎓</div>
              <h3>Career Growth</h3>
              <p>Identify skill gaps and get targeted learning recommendations to advance your career faster.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-box">🏆</div>
              <h3>Stand Out</h3>
              <p>Optimize your resume to beat applicant tracking systems and get noticed by recruiters.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-box">💼</div>
              <h3>Job Readiness</h3>
              <p>Match your profile against real job descriptions and know exactly how qualified you are.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-box">📱</div>
              <h3>Accessible Anywhere</h3>
              <p>Access your analysis reports and recommendations anytime, anywhere from any device.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon-box">🔒</div>
              <h3>Privacy First</h3>
              <p>Your data is encrypted and secure. We never share your personal information with third parties.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="landing-section how-it-works-section">
        <div className="section-container">
          <h2 className="section-title">Your Path to Success</h2>
          <p className="section-subtitle">What happens after you sign up</p>
          
          <div className="steps-container">
            <div className="step-item">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Complete Your Profile</h3>
                <p>Upload your resume and let our AI extract all relevant information automatically to build your professional profile.</p>
              </div>
            </div>
            
            <div className="step-item">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Discover Opportunities</h3>
                <p>Compare your profile against multiple job descriptions to find the perfect fit and understand your strengths.</p>
              </div>
            </div>
            
            <div className="step-item">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>Improve & Apply</h3>
                <p>Follow personalized recommendations to enhance your resume and increase your chances of landing interviews.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer className="landing-footer">
        <p>© 2026 AI Resume Analyzer. Powered by Advanced NLP & Machine Learning Technology.</p>
      </footer>
    </div>
  );
}

export default SignUp;
