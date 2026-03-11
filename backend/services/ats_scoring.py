def calculate_ats(resume_data):

    skills_count = len(resume_data.get("skills", []))

    score = min(skills_count * 10, 100)

    return {
        "ats_score": score
    }