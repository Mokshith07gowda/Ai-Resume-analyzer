"""
MongoDB Models for Database Collections
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserModel(BaseModel):
    """User model for MongoDB"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    full_name: str
    email: EmailStr
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ResumeDocument(BaseModel):
    """Resume document model for MongoDB"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: Optional[str] = None
    file_name: str
    file_type: str
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    
    education: Optional[List[dict]] = []
    experience: Optional[List[dict]] = []
    projects: Optional[List[dict]] = []
    skills: Optional[List[str]] = []
    languages: Optional[List[str]] = []
    hobbies: Optional[List[str]] = []
    certifications: Optional[List[str]] = []
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class JobDescriptionDocument(BaseModel):
    """Job description document model for MongoDB"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: Optional[str] = None
    title: str
    company: Optional[str] = None
    description: str
    required_skills: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class AnalysisResultDocument(BaseModel):
    """Analysis result document model for MongoDB"""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: Optional[str] = None
    resume_id: str
    jd_id: Optional[str] = None
    
    ats_score: Optional[float] = None
    matching_score: Optional[float] = None
    skill_gaps: Optional[List[str]] = []
    recommendations: Optional[List[str]] = []
    predicted_roles: Optional[List[str]] = []
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
