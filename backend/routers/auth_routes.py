from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from bson import ObjectId
from database import get_users_collection
from models.db_models import UserModel
from dependencies import get_current_user
from config import settings
from logger import get_logger
from limiter import limiter

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = get_logger(__name__)


class UserRegistration(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    profile_pic: str | None = None
    created_at: datetime
    is_active: bool


class UserProfileUpdate(BaseModel):
    full_name: str
    email: EmailStr
    profile_pic: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: str) -> str:
    expiry = datetime.utcnow() + timedelta(minutes=settings.jwt_expiry_minutes)
    return jwt.encode(
        {"sub": user_id, "exp": expiry},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )


def _format_user(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "full_name": user["full_name"],
        "email": user["email"],
        "profile_pic": user.get("profile_pic"),
        "created_at": user["created_at"],
        "is_active": user["is_active"],
    }


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/hour")
async def register_user(request: Request, user_data: UserRegistration):
    users = get_users_collection()
    if await users.find_one({"email": user_data.email}):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")
    user = UserModel(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )
    result = await users.insert_one(user.model_dump(by_alias=True, exclude={"id"}))
    created = await users.find_one({"_id": result.inserted_id})
    logger.info(f"New user registered: {user_data.email}")
    return UserResponse(**_format_user(created))


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
async def login_user(request: Request, credentials: UserLogin):
    users = get_users_collection()
    user = await users.find_one({"email": credentials.email})
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Email not registered. Please sign up.")
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect password.")
    if not user.get("is_active", True):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account disabled. Contact support.")
    token = create_access_token(str(user["_id"]))
    logger.info(f"User logged in: {credentials.email}")
    return TokenResponse(access_token=token, user=_format_user(user))


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(**_format_user(current_user))


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    users = get_users_collection()
    try:
        user = await users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        return UserResponse(**_format_user(user))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Invalid user ID: {e}")


@router.put("/users/{user_id}")
async def update_user_profile(
    user_id: str,
    profile_data: UserProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    if str(current_user["_id"]) != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You can only update your own profile")
    users = get_users_collection()
    try:
        object_id = ObjectId(user_id)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Invalid user ID: {e}")
    existing = await users.find_one({"_id": object_id})
    if not existing:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    if profile_data.email != existing.get("email"):
        duplicate = await users.find_one({"email": profile_data.email})
        if duplicate and str(duplicate["_id"]) != user_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already in use")
    await users.update_one(
        {"_id": object_id},
        {"$set": {
            "full_name": profile_data.full_name.strip(),
            "email": profile_data.email,
            "profile_pic": profile_data.profile_pic,
            "updated_at": datetime.utcnow(),
        }},
    )
    updated = await users.find_one({"_id": object_id})
    logger.info(f"User profile updated: {user_id}")
    return {"message": "Profile updated successfully", "user": _format_user(updated)}