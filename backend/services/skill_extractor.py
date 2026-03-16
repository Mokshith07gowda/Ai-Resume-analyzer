import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
SKILLS_PATH = DATA_DIR / "skills.json"
SYNONYMS_PATH = DATA_DIR / "synonyms.json"


def _load_skills(path: Path) -> List[str]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []

    if not isinstance(raw, list):
        return []

    cleaned = []
    seen = set()
    for item in raw:
        if not isinstance(item, str):
            continue
        skill = item.strip()
        if not skill:
            continue
        key = skill.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(skill)

    return cleaned


def _load_synonyms(path: Path) -> Dict[str, str]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

    if not isinstance(raw, dict):
        return {}

    cleaned = {}
    for alias, canonical in raw.items():
        if not isinstance(alias, str) or not isinstance(canonical, str):
            continue
        alias_clean = alias.strip()
        canonical_clean = canonical.strip()
        if alias_clean and canonical_clean:
            cleaned[alias_clean.lower()] = canonical_clean

    return cleaned


def _compile_pattern(term: str) -> re.Pattern:
    escaped = re.escape(term.lower())
    escaped = escaped.replace(r"\ ", r"\s+")
    return re.compile(r"(?<![A-Za-z0-9])" + escaped + r"(?![A-Za-z0-9])")


SKILLS_LIST = _load_skills(SKILLS_PATH)
_SKILL_INDEX = {skill.lower(): skill for skill in SKILLS_LIST}
_SYNONYMS = _load_synonyms(SYNONYMS_PATH)


def normalize_skill_name(skill_name: str) -> str:
    """Normalize a skill name using canonical list and synonym mapping."""
    cleaned = (skill_name or "").strip()
    if not cleaned:
        return ""

    lower = cleaned.lower()
    canonical = _SYNONYMS.get(lower, cleaned)
    canonical_lower = canonical.lower()

    if canonical_lower in _SKILL_INDEX:
        return _SKILL_INDEX[canonical_lower]

    return canonical


def _build_alias_map() -> Dict[str, str]:
    alias_to_canonical = {}

    for skill in SKILLS_LIST:
        alias_to_canonical[skill.lower()] = skill

    for alias, canonical in _SYNONYMS.items():
        normalized_canonical = normalize_skill_name(canonical)
        if normalized_canonical:
            alias_to_canonical[alias] = normalized_canonical

    return alias_to_canonical


_ALIAS_TO_CANONICAL = _build_alias_map()
_ALIASES_SORTED = sorted(_ALIAS_TO_CANONICAL.keys(), key=len, reverse=True)
_ALIAS_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (_compile_pattern(alias), _ALIAS_TO_CANONICAL[alias])
    for alias in _ALIASES_SORTED
]


def extract_skills(text: str) -> List[str]:
    """Extract and normalize skills from free-form text."""
    normalized_text = re.sub(r"\s+", " ", (text or "")).strip().lower()
    if not normalized_text:
        return []

    first_positions: Dict[str, int] = {}

    for pattern, canonical in _ALIAS_PATTERNS:
        match = pattern.search(normalized_text)
        if not match:
            continue
        pos = match.start()
        prev = first_positions.get(canonical)
        if prev is None or pos < prev:
            first_positions[canonical] = pos

    ordered = sorted(first_positions.items(), key=lambda item: (item[1], item[0].lower()))
    return [skill for skill, _ in ordered]


def extract_resume_skills(text: str) -> List[str]:
    """Wrapper used by resume parsing pipeline."""
    return extract_skills(text)


def extract_jd_skills(text: str) -> List[str]:
    """Wrapper used by JD processing pipeline."""
    return extract_skills(text)


def extract_skill_lists(resume_text: str, jd_text: str) -> Dict[str, List[str]]:
    """Return Week-3 output shape for downstream matching integration."""
    return {
        "resume_skills": extract_resume_skills(resume_text),
        "jd_skills": extract_jd_skills(jd_text)
    }


def get_all_skills() -> List[str]:
    """Return the complete canonical skills list."""
    return SKILLS_LIST
