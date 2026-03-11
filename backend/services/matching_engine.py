def match_resume(resume_data, jd_data):

    resume_skills = set(resume_data.get("skills", []))
    jd_skills = set(jd_data.get("skills", []))

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills

    score = int(len(matched) / len(jd_skills) * 100) if jd_skills else 0

    return {
        "match_score": score,
        "matched_skills": list(matched),
        "missing_skills": list(missing)
    }