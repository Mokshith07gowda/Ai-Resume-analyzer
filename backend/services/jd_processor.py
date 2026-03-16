import re
from collections import Counter
from typing import Dict, List

from .skill_extractor import extract_jd_skills as extract_jd_skills_from_engine

try:
    import spacy
except Exception:  # pragma: no cover - optional dependency
    spacy = None


FALLBACK_STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this", "are", "you", "your", "our",
    "will", "have", "has", "not", "but", "all", "any", "can", "job", "role", "work",
    "team", "years", "year", "experience", "required", "preferred", "must", "should",
    "who", "what", "when", "where", "why", "their", "they", "them", "its", "able",
    "skills", "skill", "candidate", "candidates", "responsibilities", "requirements"
}

_NLP = None
if spacy is not None:
    try:
        _NLP = spacy.load("en_core_web_sm")
    except Exception:
        _NLP = None


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def extract_jd_skills(text: str) -> List[str]:
    """Extract required skills using the centralized Week-3 skill engine."""
    return extract_jd_skills_from_engine(text)


def _extract_keywords_with_spacy(text: str) -> List[str]:
    doc = _NLP(text)
    lemmas = []
    for token in doc:
        if token.is_stop or token.is_punct or token.like_num:
            continue
        if token.pos_ not in {"NOUN", "PROPN", "ADJ"}:
            continue

        lemma = token.lemma_.lower().strip()
        if len(lemma) < 3 or not re.search(r"[a-z]", lemma):
            continue
        lemmas.append(lemma)

    counts = Counter(lemmas)
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [word for word, _ in ordered]


def _extract_keywords_fallback(text: str) -> List[str]:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{2,}", text.lower())
    cleaned_tokens = [tok.strip("._-+") for tok in tokens]
    filtered = [tok for tok in cleaned_tokens if tok and tok not in FALLBACK_STOPWORDS]
    counts = Counter(filtered)
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [word for word, _ in ordered]


def extract_keywords(text: str, limit: int = 25) -> List[str]:
    """Extract meaningful keywords using spaCy when available, with safe fallback."""
    normalized = _normalize_text(text)
    if not normalized:
        return []

    if _NLP is not None:
        keywords = _extract_keywords_with_spacy(normalized)
    else:
        keywords = _extract_keywords_fallback(normalized)

    return keywords[:limit]


def _calculate_skill_coverage(required_skills: List[str], baseline_skills: int = 12) -> float:
    if baseline_skills <= 0:
        return 0.0
    coverage = (len(required_skills) / baseline_skills) * 100
    return round(min(100.0, coverage), 1)


def _calculate_top_keyword_density(text: str, keywords: List[str], top_n: int = 5) -> float:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}", text.lower())
    if not tokens:
        return 0.0

    top_keywords = [kw.lower() for kw in keywords[:top_n]]
    if not top_keywords:
        return 0.0

    token_counts = Counter(tokens)
    top_hits = sum(token_counts.get(keyword, 0) for keyword in top_keywords)
    density = (top_hits / len(tokens)) * 100
    return round(density, 2)


def _infer_role_hints(required_skills: List[str], keywords: List[str], text: str) -> List[str]:
    signal_terms = {item.lower() for item in required_skills + keywords}
    signal_terms.update(re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{2,}", text.lower()))

    role_map = {
        "Backend Engineer": {"python", "java", "node.js", "fastapi", "django", "flask", "rest", "api", "sql", "microservices"},
        "Frontend Engineer": {"react", "angular", "vue", "javascript", "typescript", "html", "css", "tailwind", "bootstrap"},
        "Full Stack Engineer": {"react", "node.js", "javascript", "typescript", "sql", "mongodb", "api"},
        "Data Scientist": {"python", "pandas", "numpy", "scikit-learn", "machine", "learning", "tensorflow", "pytorch", "statistics"},
        "ML Engineer": {"machine", "learning", "tensorflow", "pytorch", "mlops", "docker", "kubernetes", "python"},
        "DevOps Engineer": {"docker", "kubernetes", "aws", "azure", "gcp", "terraform", "jenkins", "ci/cd", "linux"},
        "Data Engineer": {"spark", "hadoop", "etl", "sql", "airflow", "data", "pipeline", "warehouse"},
        "QA Engineer": {"selenium", "pytest", "junit", "cypress", "postman", "testing", "automation"}
    }

    hints = []
    for role, terms in role_map.items():
        matched = len(signal_terms.intersection(terms))
        if matched >= 3:
            hints.append(role)

    return hints[:3]


def build_scoring_block(jd_text: str, required_skills: List[str], keywords: List[str]) -> Dict[str, object]:
    return {
        "skill_coverage_pct": _calculate_skill_coverage(required_skills),
        "top_keyword_density_pct": _calculate_top_keyword_density(jd_text, keywords),
        "role_hints": _infer_role_hints(required_skills, keywords, jd_text)
    }


def process_job_description(jd_text: str) -> Dict[str, object]:
    """Process job description text and return structured extraction results."""
    normalized = _normalize_text(jd_text)
    if not normalized:
        return {
            "required_skills": [],
            "keywords": [],
            "text_preview": "",
            "scoring": {
                "skill_coverage_pct": 0.0,
                "top_keyword_density_pct": 0.0,
                "role_hints": []
            }
        }

    required_skills = extract_jd_skills(normalized)
    keywords = extract_keywords(normalized)
    scoring = build_scoring_block(normalized, required_skills, keywords)

    return {
        "required_skills": required_skills,
        "keywords": keywords,
        "text_preview": normalized[:300],
        "scoring": scoring
    }
