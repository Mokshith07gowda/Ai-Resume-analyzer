from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
import sys


class Settings(BaseSettings):
    mongodb_url: str
    database_name: str = "ai_resume_analyzer"
    allowed_origins: List[str] = ["http://localhost:3000"]
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 60
    max_upload_size_mb: int = 5

    @field_validator("jwt_secret")
    @classmethod
    def jwt_secret_must_be_strong(cls, v):
        if len(v) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters long")
        return v

    @field_validator("mongodb_url")
    @classmethod
    def mongodb_url_must_exist(cls, v):
        if not v or not v.startswith("mongodb"):
            raise ValueError("MONGODB_URL is missing or invalid")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


try:
    settings = Settings()
except Exception as e:
    print(f"❌ Configuration error: {e}")
    print("Make sure your .env file exists and has all required variables.")
    sys.exit(1)