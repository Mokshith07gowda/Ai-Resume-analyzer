from pydantic import BaseModel
from typing import List, Optional


class JDInput(BaseModel):
    """Model for job description input"""
    job_description: str


class JDData(BaseModel):
    """Model for processed job description data"""
    required_skills: List[str]
    keywords: List[str]
    text_preview: Optional[str] = None


class JDProcessResponse(BaseModel):
    """Model for JD processing response"""
    message: str
    jd_data: Optional[JDData] = None
