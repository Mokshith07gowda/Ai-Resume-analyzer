import React, { useState } from 'react';
import { uploadResume } from '../services/api';

function ResumeUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [editableSkills, setEditableSkills] = useState([]);
  const [newSkill, setNewSkill] = useState('');

  const syncResultSkills = (skills) => {
    setEditableSkills(skills);
    setResult((prev) => {
      if (!prev || !prev.resume_data) return prev;
      return {
        ...prev,
        resume_data: {
          ...prev.resume_data,
          skills
        }
      };
    });
  };

  const addSkill = () => {
    const skill = newSkill.trim();
    if (!skill) return;

    const exists = editableSkills.some((item) => item.toLowerCase() === skill.toLowerCase());
    if (exists) {
      setNewSkill('');
      return;
    }

    const updated = [...editableSkills, skill];
    syncResultSkills(updated);
    setNewSkill('');
  };

  const removeSkill = (indexToRemove) => {
    const updated = editableSkills.filter((_, index) => index !== indexToRemove);
    syncResultSkills(updated);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Validate file type
      const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      if (validTypes.includes(file.type)) {
        setSelectedFile(file);
        setError(null);
      } else {
        setError('Invalid file format. Please upload a PDF or DOCX document.');
        setSelectedFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a document to analyze.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setEditableSkills([]);
    setNewSkill('');

    try {
      const response = await uploadResume(selectedFile);
      setResult(response);
      syncResultSkills(response?.resume_data?.skills || []);
      console.log('Resume uploaded successfully:', response);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while processing the document. Please try again.');
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="resume-upload-container">
      <h2>Resume Document Analysis</h2>
      
      <div className="upload-section">
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={handleFileChange}
          disabled={loading}
        />
        
        {selectedFile && (
          <p className="file-info">Document Selected: {selectedFile.name}</p>
        )}
        
        <button 
          onClick={handleUpload} 
          disabled={!selectedFile || loading}
          className="upload-button"
        >
          {loading ? 'Analyzing Document' : 'Analyze Resume'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="result-section">
          <h3>Analysis Complete - Extracted Information</h3>
          <div className="resume-data">
            <p><strong>Name:</strong> {result.resume_data.name}</p>
            <p><strong>Education:</strong> {result.resume_data.education}</p>
            <p><strong>Experience:</strong> {result.resume_data.experience}</p>
            
            <div className="section-divider">
              <p><strong>Skills (Editable):</strong></p>
              <div className="skill-editor">
                <input
                  type="text"
                  value={newSkill}
                  onChange={(e) => setNewSkill(e.target.value)}
                  placeholder="Add a skill"
                  className="skill-input"
                />
                <button type="button" onClick={addSkill} className="clear-button">Add Skill</button>
              </div>
              <ul className="skill-pill-list">
                {editableSkills.map((skill, index) => (
                  <li key={index} className="skill-pill">
                    <span className="skill-pill-label">{skill}</span>
                    <button
                      type="button"
                      onClick={() => removeSkill(index)}
                      className="skill-pill-remove"
                      aria-label={`Remove ${skill}`}
                    >
                      x
                    </button>
                  </li>
                ))}
              </ul>
            </div>

            {result.resume_data.projects && result.resume_data.projects.length > 0 && (
              <div className="section-divider">
                <p><strong>Projects:</strong></p>
                <ul>
                  {result.resume_data.projects.map((project, index) => (
                    <li key={index}>{project}</li>
                  ))}
                </ul>
              </div>
            )}

            {result.resume_data.languages && result.resume_data.languages.length > 0 && (
              <div className="section-divider">
                <p><strong>Spoken Languages:</strong></p>
                <ul>
                  {result.resume_data.languages.map((language, index) => (
                    <li key={index}>{language}</li>
                  ))}
                </ul>
              </div>
            )}

            {result.resume_data.hobbies && result.resume_data.hobbies.length > 0 && (
              <div className="section-divider">
                <p><strong>Hobbies & Interests:</strong></p>
                <ul>
                  {result.resume_data.hobbies.map((hobby, index) => (
                    <li key={index}>{hobby}</li>
                  ))}
                </ul>
              </div>
            )}

            {result.resume_data.additional_info && (
              <div className="section-divider">
                <p><strong>Additional Information:</strong></p>
                <div className="additional-info">
                  {result.resume_data.additional_info.email && (
                    <p>📧 Email: {result.resume_data.additional_info.email}</p>
                  )}
                  {result.resume_data.additional_info.phone && (
                    <p>📱 Phone: {result.resume_data.additional_info.phone}</p>
                  )}
                  {result.resume_data.additional_info.linkedin && (
                    <p>🔗 LinkedIn: {result.resume_data.additional_info.linkedin}</p>
                  )}
                  {result.resume_data.additional_info.github && (
                    <p>💻 GitHub: {result.resume_data.additional_info.github}</p>
                  )}
                  {result.resume_data.additional_info.certifications && 
                   result.resume_data.additional_info.certifications.length > 0 && (
                    <div>
                      <p><strong>Certifications:</strong></p>
                      <ul>
                        {result.resume_data.additional_info.certifications.map((cert, index) => (
                          <li key={index}>{cert}</li>
                        ))}
                      </ul>
                    </div>
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

export default ResumeUpload;
