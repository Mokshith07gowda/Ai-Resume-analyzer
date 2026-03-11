import React from 'react';

function Home({ onNavigate }) {
  const features = [
    {
      title: 'Resume Analysis',
      description: 'Upload and parse resumes in PDF, DOCX, or TXT format. Extract comprehensive information including personal details, education, experience, projects, skills, languages, and hobbies.',
      icon: '📄'
    },
    {
      title: 'JD Processing',
      description: 'Process job descriptions through text input or file upload. Intelligent extraction of required skills, qualifications, and key responsibilities using advanced NLP.',
      icon: '💼'
    },
    {
      title: 'Skill Extraction',
      description: 'Automatically identify and extract 100+ technical and soft skills from resumes and job descriptions across programming, web development, databases, cloud, data science, and more.',
      icon: '🎯'
    },
    {
      title: 'ATS Scoring',
      description: 'Calculate Applicant Tracking System (ATS) compatibility scores to evaluate how well resumes match against job requirements and industry standards.',
      icon: '📊'
    },
    {
      title: 'Role Prediction',
      description: 'Leverage machine learning algorithms to predict the most suitable job roles based on candidate skills, experience, and educational background.',
      icon: '🔮'
    },
    {
      title: 'Matching Engine',
      description: 'Intelligent matching algorithm that compares candidate profiles with job descriptions, calculating compatibility scores and identifying skill gaps.',
      icon: '🔗'
    },
    {
      title: 'Recommendation Engine',
      description: 'Generate personalized recommendations for skill development, career advancement, and profile optimization based on market trends and job requirements.',
      icon: '💡'
    },
    {
      title: 'Report Generation',
      description: 'Create comprehensive, professional reports with detailed analytics, visualizations, and actionable insights for recruiters and candidates.',
      icon: '📋'
    }
  ];

  return (
    <div className="home-container">
      <section className="hero-section">
        <h2>Welcome to AI Resume Analyzer</h2>
        <p className="hero-subtitle">
          Transform your recruitment process with intelligent resume parsing, 
          advanced job matching, and comprehensive candidate analysis powered by 
          cutting-edge AI and Natural Language Processing.
        </p>
      </section>

      <section className="features-section">
        <h3>Key Features</h3>
        <div className="features-grid">
          {features.map((feature, index) => (
            <div key={index} className="feature-card">
              <div className="feature-icon">{feature.icon}</div>
              <h4>{feature.title}</h4>
              <p>{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="cta-section">
        <h3>Get Started</h3>
        <p>Choose a feature from the navigation above to begin analyzing resumes and processing job descriptions.</p>
        <div className="cta-buttons">
          <button className="cta-button primary" onClick={() => onNavigate('resume')}>
            Upload Resume
          </button>
          <button className="cta-button secondary" onClick={() => onNavigate('jd')}>
            Process Job Description
          </button>
        </div>
      </section>
    </div>
  );
}

export default Home;
