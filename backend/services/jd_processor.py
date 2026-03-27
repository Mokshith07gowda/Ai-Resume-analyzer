import re
from typing import List, Dict
from services.skill_extractor import extract_jd_skills


RESPONSIBILITY_KEYWORDS = [
    "you will", "you'll", "responsibilities", "you should", "expected to",
    "duties", "tasks", "role involves", "will be responsible"
]

KEYWORD_STOPWORDS = {
    "experience", "knowledge", "understanding", "ability", "skills",
    "working", "strong", "good", "excellent", "proven", "required",
    "preferred", "plus", "bonus", "years", "year", "proficient",
    "familiarity", "exposure", "hands", "on", "with", "and", "or",
    "the", "a", "an", "in", "of", "to", "for", "is", "are", "be",
    "have", "has", "will", "must", "can", "should", "that", "this",
    "their", "they", "we", "our", "you", "your"
}


def extract_responsibilities(text: str) -> List[str]:
    """Extract job responsibilities from JD text."""
    responsibilities = []
    lines = text.split("\n")
    in_section = False

    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        if any(kw in line_lower for kw in RESPONSIBILITY_KEYWORDS):
            in_section = True
            continue

        if in_section:
            if any(section in line_lower for section in [
                "requirement", "qualification", "skill", "education",
                "benefit", "about us", "what we offer", "salary"
            ]):
                break

            if line_stripped.startswith(("•", "-", "*", "○", "→")) or re.match(r"^\d+\.", line_stripped):
                cleaned = re.sub(r"^[•\-\*○→\d\.]\s*", "", line_stripped).strip()
                if cleaned and len(cleaned) > 10:
                    responsibilities.append(cleaned)

    return responsibilities[:10]


def extract_keywords(text: str) -> List[str]:
    """Extract important non-skill keywords from JD."""
    words = re.findall(r'\b[A-Za-z][a-z]{2,}\b', text)
    freq: Dict[str, int] = {}

    for word in words:
        w = word.lower()
        if w not in KEYWORD_STOPWORDS and len(w) > 3:
            freq[w] = freq.get(w, 0) + 1

    sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_keywords if count >= 2][:15]


def extract_experience_requirement(text: str) -> str:
    """Extract required years of experience from JD."""
    patterns = [
        r'(\d+)\+?\s*(?:to\s*\d+)?\s*years?\s*of\s*(?:relevant\s*)?experience',
        r'(\d+)\+?\s*yrs?\s*(?:of\s*)?experience',
        r'minimum\s*(?:of\s*)?(\d+)\s*years?',
        r'at\s*least\s*(\d+)\s*years?',
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return f"{match.group(1)}+ years"
    return "Not specified"


def extract_education_requirement(text: str) -> str:
    """Extract required education from JD."""
    education_levels = [
        ("phd", "PhD"),
        ("doctorate", "Doctorate"),
        ("master", "Master's degree"),
        ("m.tech", "M.Tech"),
        ("m.e", "M.E"),
        ("mba", "MBA"),
        ("bachelor", "Bachelor's degree"),
        ("b.tech", "B.Tech"),
        ("b.e", "B.E"),
        ("b.sc", "B.Sc"),
        ("degree", "Degree"),
        ("diploma", "Diploma"),
    ]
    text_lower = text.lower()
    for keyword, label in education_levels:
        if keyword in text_lower:
            return label
    return "Not specified"


def process_job_description(jd_text: str) -> Dict:
    """
    Full JD processing pipeline.
    Extracts skills, keywords, responsibilities, experience and education requirements.
    """
    if not jd_text or not jd_text.strip():
        return {"error": "Job description text is empty"}

    required_skills = extract_jd_skills(jd_text)
    responsibilities = extract_responsibilities(jd_text)
    keywords = extract_keywords(jd_text)
    experience_required = extract_experience_requirement(jd_text)
    education_required = extract_education_requirement(jd_text)

    return {
        "required_skills": required_skills,
        "responsibilities": responsibilities,
        "keywords": keywords,
        "experience_required": experience_required,
        "education_required": education_required,
        "word_count": len(jd_text.split()),
    }