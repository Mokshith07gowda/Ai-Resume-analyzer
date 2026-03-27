from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler):
        from pydantic_core import core_schema
        return core_schema.no_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")


class UserModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    full_name: str
    email: EmailStr
    profile_pic: Optional[str] = None
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


class ResumeDocument(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

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


class JobDescriptionDocument(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: Optional[str] = None
    title: str
    company: Optional[str] = None
    description: str
    required_skills: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AnalysisResultDocument(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

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