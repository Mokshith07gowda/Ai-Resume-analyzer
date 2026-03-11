import spacy
from .skill_extractor import extract_skills

# Load spaCy model (small English model)
# Note: Run 'python -m spacy download en_core_web_sm' before using
try:
    nlp = spacy.load("en_core_web_sm")
except:
    print("Warning: spaCy model not loaded. Run: python -m spacy download en_core_web_sm")
    nlp = None


def extract_jd_skills(text: str) -> list:
    """
    Extract required skills from job description.
    
    Args:
        text: Job description text
        
    Returns:
        List of required skills
    """
    return extract_skills(text)


def extract_keywords(text: str) -> list:
    """
    Extract important keywords from job description using spaCy NLP.
    
    Args:
        text: Job description text
        
    Returns:
        List of important keywords (nouns and proper nouns)
    """
    if nlp is None:
        # Fallback: simple word extraction
        words = text.split()
        return [word.strip('.,!?;:') for word in words if len(word) > 4][:20]
    
    doc = nlp(text)
    keywords = []
    
    # Extract nouns and proper nouns
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 2:
            keywords.append(token.text)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for keyword in keywords:
        if keyword.lower() not in seen:
            seen.add(keyword.lower())
            unique_keywords.append(keyword)
    
    return unique_keywords[:20]  # Return top 20 keywords


def process_job_description(jd_text: str) -> dict:
    """
    Process job description and extract structured information.
    
    Args:
        jd_text: Job description text
        
    Returns:
        Dictionary containing extracted JD data
    """
    required_skills = extract_jd_skills(jd_text)
    keywords = extract_keywords(jd_text)
    
    jd_data = {
        "required_skills": required_skills,
        "keywords": keywords,
        "text_preview": jd_text[:300]  # First 300 characters for preview
    }
    
    return jd_data
