from typing import List


def _normalize(skills: List[str]) -> set:
    return {s.strip().lower() for s in skills if s.strip()}


def match_resume(resume_data: dict, jd_data: dict) -> dict:
    """
    Match resume skills against a job description.
    Returns match score, matched/missing skills, and recommendations.
    """
    resume_skills = _normalize(resume_data.get("skills", []))
    jd_skills = _normalize(jd_data.get("required_skills", []))

    if not jd_skills:
        return {
            "match_score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "recommendations": ["No required skills found in the job description."],
            "grade": "N/A"
        }

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    match_score = round((len(matched) / len(jd_skills)) * 100, 2)

    recommendations = []
    if missing:
        top_missing = sorted(missing)[:5]
        recommendations.append(
            f"Consider adding these skills: {', '.join(top_missing)}."
        )
    if match_score >= 80:
        recommendations.append("Strong match! Your profile aligns well with this role.")
    elif match_score >= 50:
        recommendations.append("Decent match. Upskilling in missing areas will improve your chances.")
    else:
        recommendations.append("Low match. Focus on acquiring the required skills for this role.")

    return {
        "match_score": match_score,
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "recommendations": recommendations,
        "grade": (
            "Excellent" if match_score >= 80 else
            "Good" if match_score >= 60 else
            "Average" if match_score >= 40 else
            "Needs Improvement"
        )
    }