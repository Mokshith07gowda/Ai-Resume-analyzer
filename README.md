# AI Resume Analyzer

An AI-powered resume analysis tool that extracts structured information from resumes and job descriptions, enabling intelligent matching and recommendations.

## 🎯 Week 2 Implementation Status

### ✅ Completed Features

- **Resume Upload & Parsing**
  - PDF and DOCX file support
  - Extract name, skills, education, and experience
  - Extract projects, languages, hobbies
  - Extract additional info (email, phone, LinkedIn, GitHub, certifications)
  - Structured data output

- **Job Description Processing**
  - Text input for job descriptions
  - File upload support (PDF, DOCX, TXT)
  - Skill extraction
  - Keyword extraction using NLP

- **Backend APIs**
  - `POST /api/upload_resume` - Upload and parse resume
  - `POST /api/upload_jd` - Process job description text
  - `POST /api/upload_jd_file` - Upload and process job description file
  - Health check endpoint

- **Frontend UI**
  - Resume upload page with file validation
  - Job description input page
  - Results display for both resume and JD
  - Responsive design

## 🏗️ Project Structure

```
ai-resume-analyzer/
│
├── frontend/                     # React application
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/          # UI components
│   │   │   ├── ResumeUpload.js
│   │   │   ├── JDInput.js
│   │   │   └── ...
│   │   ├── pages/               # Page views
│   │   ├── services/            # API calls
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   └── main.css
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
│
├── backend/                     # FastAPI backend
│   ├── main.py                  # FastAPI entry point
│   ├── routers/                 # API endpoints
│   │   ├── resume_routes.py
│   │   └── jd_routes.py
│   ├── services/                # AI processing modules
│   │   ├── resume_parser.py
│   │   ├── jd_processor.py
│   │   └── skill_extractor.py
│   └── models/                  # Data models
│       ├── resume_model.py
│       └── jd_model.py
│
├── requirements.txt             # Python dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to project root**
   ```bash
   cd "AI Resume Analyzer demo"
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Run the backend server**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   
   API Documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

   The app will open at `http://localhost:3000`

## 📋 API Endpoints

### Resume Upload
```
POST /api/upload_resume
Content-Type: multipart/form-data

Response:
{
  "message": "Resume uploaded and parsed successfully",
  "resume_data": {
    "name": "John Doe",
    "skills": ["Python", "SQL", "Machine Learning"],
    "education": "B.Tech, M.Tech",
    "experience": "3 years",
    "projects": ["AI Resume Analyzer", "E-commerce Platform"],
    "languages": ["Python", "JavaScript", "English", "Hindi"],
    "hobbies": ["Reading", "Coding", "Photography"],
    "additional_info": {
      "email": "john.doe@example.com",
      "phone": "+1234567890",
      "linkedin": "linkedin.com/in/johndoe",
      "github": "github.com/johndoe",
      "certifications": ["AWS Certified", "Python Expert"]
    }
  },
  "filename": "resume.pdf"
}
```

### Job Description Processing
```
POST /api/upload_jd
Content-Type: application/json

Body:
{
  "job_description": "We need a backend developer with Python, SQL and Docker experience..."
}

Response:
{
  "message": "Job description processed successfully",
  "jd_data": {
    "required_skills": ["Python", "SQL", "Docker"],
    "keywords": ["backend", "developer", "experience", "API"]
  }
}
```

### Job Description File Upload
```
POST /api/upload_jd_file
Content-Type: multipart/form-data

Response:
{
  "message": "Job description file processed successfully",
  "jd_data": {
    "required_skills": ["Python", "SQL", "Docker"],
    "keywords": ["backend", "developer", "experience", "API"]
  }
}
```

## 🧪 Testing

### Test Resume Upload

1. Prepare a test resume (PDF or DOCX)
2. Open `http://localhost:3000`
3. Click "Upload Resume" tab
4. Select your resume file
5. Click "Upload Resume"
6. View extracted data

### Test Job Description

1. Open `http://localhost:3000`
2. Click "Job Description Processing" tab
3. Choose input method:
   - **Paste Text**: Enter job description directly
   - **Upload File**: Upload PDF, DOCX, or TXT file
4. Click "Analyze Job Description"
5. View extracted skills and keywords

## 🛠️ Technologies Used

### Backend
- **FastAPI** - Modern web framework
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX parsing
- **spaCy** - NLP for keyword extraction
- **Pydantic** - Data validation

### Frontend
- **React** - UI framework
- **Axios** - HTTP client
- **CSS3** - Styling

## 📝 Week 2 Deliverables Checklist

- ✅ Resume upload working
- ✅ Resume text extracted
- ✅ Resume skills detected
- ✅ JD input working
- ✅ JD skills extracted
- ✅ Backend APIs working
- ✅ Frontend forms working

## 🔜 Next Steps (Week 3+)

- Matching engine for resume-JD comparison
- ATS scoring algorithm
- Role prediction
- Recommendation engine
- Report generation
- Charts and visualizations

## 📄 License

This project is part of a learning implementation.

## 👥 Contributors

Your Team

---

**Note:** This is Week 2 implementation. More features will be added in upcoming weeks.
