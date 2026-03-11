import axios from 'axios';

// Base URL for the backend API
const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Upload resume file to backend
 * @param {File} file - Resume file (PDF or DOCX)
 * @returns {Promise} API response with parsed resume data
 */
export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post(`${API_BASE_URL}/upload_resume`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading resume:', error);
    throw error;
  }
};

/**
 * Submit job description to backend
 * @param {string} jobDescription - Job description text
 * @returns {Promise} API response with processed JD data
 */
export const uploadJobDescription = async (jobDescription) => {
  try {
    const response = await api.post('/upload_jd', {
      job_description: jobDescription,
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading job description:', error);
    throw error;
  }
};

/**
 * Upload job description file to backend
 * @param {File} file - Job description file (PDF, DOCX, or TXT)
 * @returns {Promise} API response with processed JD data
 */
export const uploadJobDescriptionFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await axios.post(`${API_BASE_URL}/upload_jd_file`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading job description file:', error);
    throw error;
  }
};

/**
 * Health check endpoint
 * @returns {Promise} API health status
 */
export const healthCheck = async () => {
  try {
    const response = await axios.get('http://localhost:8000/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

export default api;
