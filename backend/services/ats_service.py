from typing import List


ATS_WEIGHTS = {
    "skills": 0.40,
    "experience": 0.25,
    "education": 0.20,
    "projects": 0.10,
    "additional_info": 0.05,
}

EDUCATION_KEYWORDS = [
    "b.tech", "b.e", "m.tech", "m.e", "mba", "bca", "mca",
    "bachelor", "master", "phd", "b.sc", "m.sc", "diploma"
]


def _score_skills(skills: List[str]) -> float:
    if not skills:
        return 0.0
    return min(len(skills) / 15.0, 1.0)


def _score_experience(experience: str) -> float:
    if not experience or experience == "Not specified":
        return 0.0
    try:
        years = int("".join(filter(str.isdigit, experience.split()[0])))
        return min(years / 10.0, 1.0)
    except (ValueError, IndexError):
        return 0.0


def _score_education(education: str) -> float:
    if not education or education == "Not specified":
        return 0.0
    edu_lower = education.lower()
    for keyword in EDUCATION_KEYWORDS:
        if keyword in edu_lower:
            return 1.0
    return 0.3


def _score_projects(projects: List[str]) -> float:
    if not projects or projects == ["Not specified"]:
        return 0.0
    return min(len(projects) / 3.0, 1.0)


def _score_additional_info(additional_info: dict) -> float:
    if not additional_info:
        return 0.0
    score = 0.0
    if additional_info.get("email"):
        score += 0.3
    if additional_info.get("phone"):
        score += 0.3
    if additional_info.get("linkedin"):
        score += 0.2
    if additional_info.get("github"):
        score += 0.2
    return score


def calculate_ats(resume_data: dict) -> dict:
    """
    Calculate ATS score from parsed resume data.
    Returns score out of 100 with section breakdown.
    """
    section_scores = {
        "skills": _score_skills(resume_data.get("skills", [])),
        "experience": _score_experience(resume_data.get("experience", "")),
        "education": _score_education(resume_data.get("education", "")),
        "projects": _score_projects(resume_data.get("projects", [])),
        "additional_info": _score_additional_info(resume_data.get("additional_info", {})),
    }

    weighted_score = sum(
        section_scores[section] * weight
        for section, weight in ATS_WEIGHTS.items()
    )

    ats_score = round(weighted_score * 100, 2)

    feedback = []
    if section_scores["skills"] < 0.5:
        feedback.append("Add more relevant technical skills to improve your ATS score.")
    if section_scores["experience"] == 0.0:
        feedback.append("Include your years of experience clearly.")
    if section_scores["education"] == 0.0:
        feedback.append("Add your educational qualifications.")
    if section_scores["projects"] < 0.5:
        feedback.append("List at least 2-3 projects to strengthen your profile.")
    if section_scores["additional_info"] < 0.5:
        feedback.append("Add contact details, LinkedIn, and GitHub links.")

    return {
        "ats_score": ats_score,
        "breakdown": {k: round(v * 100, 2) for k, v in section_scores.items()},
        "feedback": feedback,
        "grade": (
            "Excellent" if ats_score >= 80 else
            "Good" if ats_score >= 60 else
            "Average" if ats_score >= 40 else
            "Needs Improvement"
        )
    }