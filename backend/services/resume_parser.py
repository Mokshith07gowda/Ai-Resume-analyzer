import pdfplumber
from docx import Document
import re
from .skill_extractor import extract_resume_skills


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from PDF file.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text as string
    """
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting PDF: {e}")
    
    return text


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text content from DOCX file.
    
    Args:
        file_path: Path to DOCX file
        
    Returns:
        Extracted text as string
    """
    text = ""
    try:
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
    
    return text


def extract_name(text: str) -> str:
    """
    Extract name from resume text (simple heuristic - first line or first capitalized words).
    
    Args:
        text: Resume text
        
    Returns:
        Extracted name
    """
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if line and len(line) < 50:  # Names are usually short
            # Check if line contains mostly alphabetic characters
            if re.match(r'^[A-Za-z\s\.]+$', line):
                return line
    return "Unknown"


def extract_education(text: str) -> str:
    """
    Extract education information from resume.
    
    Args:
        text: Resume text
        
    Returns:
        Education details
    """
    education_keywords = ["B.Tech", "B.E", "M.Tech", "M.E", "MBA", "BCA", "MCA", 
                         "Bachelor", "Master", "PhD", "B.Sc", "M.Sc", "Diploma"]
    
    text_lower = text.lower()
    found_education = []
    
    for keyword in education_keywords:
        if keyword.lower() in text_lower:
            found_education.append(keyword)
    
    return ", ".join(found_education) if found_education else "Not specified"


def extract_experience(text: str) -> str:
    """
    Extract experience information from resume.
    
    Args:
        text: Resume text
        
    Returns:
        Experience details
    """
    # Look for patterns like "2 years", "3+ years", "5 yrs"
    experience_pattern = r'(\d+)\+?\s*(years?|yrs?)'
    matches = re.findall(experience_pattern, text.lower())
    
    if matches:
        # Return the highest number found
        max_exp = max([int(match[0]) for match in matches])
        return f"{max_exp} years"
    
    return "Not specified"


def extract_projects(text: str) -> list:
    """
    Extract project information from resume.
    
    Args:
        text: Resume text
        
    Returns:
        List of projects
    """
    projects = []
    lines = text.split("\n")
    
    # Look for section headers
    project_section_found = False
    project_keywords = ["project", "projects", "academic projects", "personal projects"]
    
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        
        # Check if we're in projects section
        if any(keyword in line_lower for keyword in project_keywords):
            project_section_found = True
            continue
        
        # If in projects section, extract project names
        if project_section_found:
            # Stop at next major section
            if any(section in line_lower for section in ["experience", "education", "skills", "certification", "achievements", "languages", "hobbies"]):
                break
            
            # Extract project if line has content and isn't too long
            if line.strip() and len(line.strip()) > 5 and len(line.strip()) < 100:
                # Check if it looks like a project title (often starts with bullet or contains key project words)
                if line.strip().startswith(('•', '-', '*', '○')) or ':' in line:
                    project_name = line.strip().lstrip('•-*○ ').strip()
                    if project_name and len(projects) < 5:  # Limit to 5 projects
                        projects.append(project_name)
    
    return projects if projects else ["Not specified"]


def extract_languages(text: str) -> list:
    """
    Extract spoken languages from resume (NOT programming languages).
    
    Args:
        text: Resume text
        
    Returns:
        List of spoken languages
    """
    # Only spoken languages - programming languages are already in skills
    spoken_languages = ["English", "Hindi", "Spanish", "French", "German", "Chinese", 
                       "Japanese", "Korean", "Arabic", "Portuguese", "Russian", 
                       "Italian", "Telugu", "Tamil", "Kannada", "Malayalam", "Bengali", 
                       "Marathi", "Gujarati", "Punjabi", "Urdu", "Odia", "Assamese"]
    
    found_languages = []
    text_lower = text.lower()
    
    for lang in spoken_languages:
        if lang.lower() in text_lower:
            if lang not in found_languages:
                found_languages.append(lang)
    
    return found_languages if found_languages else []


def extract_hobbies(text: str) -> list:
    """
    Extract hobbies and interests from resume.
    
    Args:
        text: Resume text
        
    Returns:
        List of hobbies
    """
    hobbies = []
    lines = text.split("\n")
    
    hobby_section_found = False
    hobby_keywords = ["hobbies", "interests", "personal interests", "activities"]
    
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        
        # Check if we're in hobbies section
        if any(keyword in line_lower for keyword in hobby_keywords):
            hobby_section_found = True
            # Sometimes hobbies are on the same line
            hobby_text = line_lower.split(':')[-1].strip()
            if hobby_text and len(hobby_text) > 3:
                hobbies_on_line = [h.strip() for h in re.split(r'[,;]', hobby_text) if h.strip()]
                hobbies.extend(hobbies_on_line)
            continue
        
        # If in hobbies section, extract hobbies
        if hobby_section_found:
            # Stop at next section or end
            if any(section in line_lower for section in ["references", "declaration", "certification", "----", "___"]):
                break
            
            # Extract hobbies (often comma or bullet separated)
            if line.strip() and len(line.strip()) > 2:
                cleaned_line = line.strip().lstrip('•-*○ ').strip()
                if cleaned_line:
                    # Split by common separators
                    items = [h.strip() for h in re.split(r'[,;]', cleaned_line) if h.strip()]
                    hobbies.extend(items)
            
            if len(hobbies) >= 5:  # Limit to reasonable number
                break
    
    return hobbies[:5] if hobbies else ["Not specified"]


def extract_additional_info(text: str) -> dict:
    """
    Extract additional information like certifications, achievements, links.
    
    Args:
        text: Resume text
        
    Returns:
        Dictionary with additional info
    """
    additional = {
        "certifications": [],
        "achievements": [],
        "linkedin": "",
        "github": "",
        "email": "",
        "phone": ""
    }
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        additional["email"] = emails[0]
    
    # Extract phone
    phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phones = re.findall(phone_pattern, text)
    if phones:
        additional["phone"] = phones[0].strip()
    
    # Extract LinkedIn
    linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
    linkedin = re.search(linkedin_pattern, text.lower())
    if linkedin:
        additional["linkedin"] = linkedin.group(0)
    
    # Extract GitHub
    github_pattern = r'github\.com/[\w\-]+'
    github = re.search(github_pattern, text.lower())
    if github:
        additional["github"] = github.group(0)
    
    # Extract certifications
    lines = text.split("\n")
    cert_section_found = False
    for line in lines:
        line_lower = line.lower().strip()
        if "certification" in line_lower or "certificate" in line_lower:
            cert_section_found = True
            continue
        if cert_section_found:
            if any(section in line_lower for section in ["experience", "education", "projects", "skills"]):
                break
            if line.strip() and len(line.strip()) > 5:
                cert = line.strip().lstrip('•-*○ ').strip()
                if cert and len(additional["certifications"]) < 3:
                    additional["certifications"].append(cert)
    
    return additional


def parse_resume(file_path: str, file_type: str) -> dict:
    """
    Parse resume and extract structured data.
    
    Args:
        file_path: Path to resume file
        file_type: Type of file ('pdf' or 'docx')
        
    Returns:
        Dictionary containing extracted resume data
    """
    # Extract text based on file type
    if file_type == "pdf":
        text = extract_text_from_pdf(file_path)
    elif file_type == "docx":
        text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file type"}
    
    # Extract structured information
    name = extract_name(text)
    skills = extract_resume_skills(text)
    education = extract_education(text)
    experience = extract_experience(text)
    projects = extract_projects(text)
    languages = extract_languages(text)
    hobbies = extract_hobbies(text)
    additional_info = extract_additional_info(text)
    
    resume_data = {
        "name": name,
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "languages": languages,
        "hobbies": hobbies,
        "additional_info": additional_info,
        "raw_text": text[:500]  # First 500 characters for preview
    }
    
    return resume_data
