from fastapi import APIRouter, Depends
from services.ats_service import calculate_ats
from dependencies import get_current_user
from limiter import limiter

router = APIRouter(prefix="/ats", tags=["ATS Scoring"])


@router.post("/")
def ats_score(resume_data: dict, current_user: dict = Depends(get_current_user)):
    return calculate_ats(resume_data)