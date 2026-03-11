"""
Authentication Routes for User Registration and Login
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from passlib.context import CryptContext
from ..database import get_users_collection
from ..models.db_models import UserModel

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRegistration(BaseModel):
    """User registration request"""
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response"""
    id: str
    full_name: str
    email: str
    created_at: datetime
    is_active: bool


def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password"""
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegistration):
    """
    Register a new user
    """
    users_collection = get_users_collection()
    
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = UserModel(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )
    
    result = await users_collection.insert_one(user.dict(by_alias=True, exclude={"id"}))
    
    created_user = await users_collection.find_one({"_id": result.inserted_id})
    
    return UserResponse(
        id=str(created_user["_id"]),
        full_name=created_user["full_name"],
        email=created_user["email"],
        created_at=created_user["created_at"],
        is_active=created_user["is_active"]
    )


@router.post("/login")
async def login_user(credentials: UserLogin):
    """
    Login user and return user info
    """
    users_collection = get_users_collection()
    
    user = await users_collection.find_one({"email": credentials.email})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
    
    return {
        "message": "Login successful",
        "user": {
            "id": str(user["_id"]),
            "full_name": user["full_name"],
            "email": user["email"],
            "created_at": user["created_at"],
            "is_active": user["is_active"]
        }
    }


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """
    Get user by ID
    """
    from bson import ObjectId
    users_collection = get_users_collection()
    
    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=str(user["_id"]),
            full_name=user["full_name"],
            email=user["email"],
            created_at=user["created_at"],
            is_active=user["is_active"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID: {str(e)}"
        )
