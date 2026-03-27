from fastapi import APIRouter, Depends
from services.matching_engine import match_resume
from dependencies import get_current_user
from limiter import limiter

router = APIRouter(prefix="/match", tags=["Matching"])


@router.post("/")
def match(resume_data: dict, jd_data: dict, current_user: dict = Depends(get_current_user)):
    return match_resume(resume_data, jd_data)