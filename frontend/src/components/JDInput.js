import React, { useState } from 'react';
import { uploadJobDescription, uploadJobDescriptionFile } from '../services/api';

function JDInput() {
  const [jdText, setJdText] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [inputMethod, setInputMethod] = useState('text'); // 'text' or 'file'
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [editableRequiredSkills, setEditableRequiredSkills] = useState([]);
  const [newRequiredSkill, setNewRequiredSkill] = useState('');

  const syncRequiredSkills = (skills) => {
    setEditableRequiredSkills(skills);
    setResult((prev) => {
      if (!prev || !prev.jd_data) return prev;
      return {
        ...prev,
        jd_data: {
          ...prev.jd_data,
          required_skills: skills
        }
      };
    });
  };

  const addRequiredSkill = () => {
    const skill = newRequiredSkill.trim();
    if (!skill) return;

    const exists = editableRequiredSkills.some((item) => item.toLowerCase() === skill.toLowerCase());
    if (exists) {
      setNewRequiredSkill('');
      return;
    }

    const updated = [...editableRequiredSkills, skill];
    syncRequiredSkills(updated);
    setNewRequiredSkill('');
  };

  const removeRequiredSkill = (indexToRemove) => {
    const updated = editableRequiredSkills.filter((_, index) => index !== indexToRemove);
    syncRequiredSkills(updated);
  };

  const handleTextChange = (event) => {
    setJdText(event.target.value);
    setError(null);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Validate file type
      const validTypes = [
        'application/pdf', 
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain'
      ];
      if (validTypes.includes(file.type) || file.name.endsWith('.txt')) {
        setSelectedFile(file);
        setError(null);
      } else {
        setError('Invalid file format. Please upload a PDF, DOCX, or TXT file.');
        setSelectedFile(null);
      }
    }
  };

  const handleSubmit = async () => {
    if (inputMethod === 'text') {
      if (!jdText.trim()) {
        setError('Please enter a job description to analyze.');
        return;
      }

      setLoading(true);
      setError(null);
      setResult(null);
      setEditableRequiredSkills([]);
      setNewRequiredSkill('');

      try {
        const response = await uploadJobDescription(jdText);
        setResult(response);
        syncRequiredSkills(response?.jd_data?.required_skills || []);
        console.log('Job description processed successfully:', response);
      } catch (err) {
        setError(err.response?.data?.detail || 'An error occurred while analyzing the job description. Please try again.');
        console.error('Processing error:', err);
      } finally {
        setLoading(false);
      }
    } else {
      if (!selectedFile) {
        setError('Please select a file to analyze.');
        return;
      }

      setLoading(true);
      setError(null);
      setResult(null);
      setEditableRequiredSkills([]);
      setNewRequiredSkill('');

      try {
        const response = await uploadJobDescriptionFile(selectedFile);
        setResult(response);
        syncRequiredSkills(response?.jd_data?.required_skills || []);
        console.log('Job description file processed successfully:', response);
      } catch (err) {
        setError(err.response?.data?.detail || 'An error occurred while processing the file. Please try again.');
        console.error('Upload error:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  const handleClear = () => {
    setJdText('');
    setSelectedFile(null);
    setResult(null);
    setError(null);
    setEditableRequiredSkills([]);
    setNewRequiredSkill('');
  };

  return (
    <div className="jd-input-container">
      <h2>Job Description Analysis</h2>
      
      <div className="input-method-toggle">
        <button 
          className={inputMethod === 'text' ? 'method-button active' : 'method-button'}
          onClick={() => {
            setInputMethod('text');
            setSelectedFile(null);
            setError(null);
          }}
        >
          Paste Text
        </button>
        <button 
          className={inputMethod === 'file' ? 'method-button active' : 'method-button'}
          onClick={() => {
            setInputMethod('file');
            setJdText('');
            setError(null);
          }}
        >
          Upload File
        </button>
      </div>

      <div className="input-section">
        {inputMethod === 'text' ? (
          <textarea
            value={jdText}
            onChange={handleTextChange}
            placeholder="Enter or paste the complete job description here for analysis..."
            rows="10"
            disabled={loading}
            className="jd-textarea"
          />
        ) : (
          <div className="file-upload-area">
            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileChange}
              disabled={loading}
            />
            {selectedFile && (
              <p className="file-info">Document Selected: {selectedFile.name}</p>
            )}
          </div>
        )}
        
        <div className="button-group">
          <button 
            onClick={handleSubmit} 
            disabled={(inputMethod === 'text' && !jdText.trim()) || (inputMethod === 'file' && !selectedFile) || loading}
            className="submit-button"
          >
            {loading ? 'Analyzing' : 'Analyze Job Description'}
          </button>
          
          <button 
            onClick={handleClear} 
            disabled={loading}
            className="clear-button"
          >
            Clear
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="result-section">
          <h3>Analysis Complete - Extracted Requirements</h3>
          <div className="jd-data">
            <div className="skills-section">
              <p><strong>Required Skills (Editable):</strong></p>
              <div className="skill-editor">
                <input
                  type="text"
                  value={newRequiredSkill}
                  onChange={(e) => setNewRequiredSkill(e.target.value)}
                  placeholder="Add required skill"
                  className="skill-input"
                />
                <button type="button" onClick={addRequiredSkill} className="clear-button">Add Skill</button>
              </div>
              <ul className="skill-pill-list">
                {editableRequiredSkills.length > 0 ? (
                  editableRequiredSkills.map((skill, index) => (
                    <li key={index} className="skill-pill">
                      <span className="skill-pill-label">{skill}</span>
                      <button
                        type="button"
                        onClick={() => removeRequiredSkill(index)}
                        className="skill-pill-remove"
                        aria-label={`Remove ${skill}`}
                      >
                        x
                      </button>
                    </li>
                  ))
                ) : (
                  <li>No skills detected</li>
                )}
              </ul>
            </div>
            
            <div className="keywords-section">
              <p><strong>Keywords:</strong></p>
              <ul>
                {result.jd_data.keywords.length > 0 ? (
                  result.jd_data.keywords.map((keyword, index) => (
                    <li key={index}>{keyword}</li>
                  ))
                ) : (
                  <li>No keywords detected</li>
                )}
              </ul>
            </div>

            {result.jd_data.scoring && (
              <div className="jd-score-block">
                <p><strong>JD Confidence & Role Fit Signals:</strong></p>
                <div className="jd-score-grid">
                  <div className="jd-score-card">
                    <span className="jd-score-label">Skill Coverage</span>
                    <span className="jd-score-value">{result.jd_data.scoring.skill_coverage_pct}%</span>
                  </div>
                  <div className="jd-score-card">
                    <span className="jd-score-label">Top Keyword Density</span>
                    <span className="jd-score-value">{result.jd_data.scoring.top_keyword_density_pct}%</span>
                  </div>
                </div>
                <div className="jd-role-hints">
                  <p><strong>Role Hints:</strong></p>
                  {result.jd_data.scoring.role_hints && result.jd_data.scoring.role_hints.length > 0 ? (
                    <ul>
                      {result.jd_data.scoring.role_hints.map((role, index) => (
                        <li key={index}>{role}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="jd-role-empty">No strong role hints found yet.</p>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default JDInput;
