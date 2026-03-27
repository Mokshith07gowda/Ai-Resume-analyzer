# models/schemas.py

from pydantic import BaseModel

class JDTextRequest(BaseModel):
    jd_text: str

class JDAnalysisResponse(BaseModel):
    required_skills: list[str]
    keywords: list[str]
    skill_count: int
    keyword_count: int