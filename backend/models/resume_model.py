from pydantic import BaseModel
from typing import List, Optional


class AdditionalInfo(BaseModel):
    certifications: List[str] = []
    achievements: List[str] = []
    linkedin: str = ""
    github: str = ""
    email: str = ""
    phone: str = ""


class ResumeData(BaseModel):
    name: str
    skills: List[str]
    education: str
    experience: str
    projects: List[str] = []
    languages: List[str] = []
    hobbies: List[str] = []
    additional_info: Optional[AdditionalInfo] = None
    raw_text: Optional[str] = None


class ResumeUploadResponse(BaseModel):
    message: str
    resume_data: Optional[ResumeData] = None
    filename: str