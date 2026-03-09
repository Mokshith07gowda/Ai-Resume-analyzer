from fastapi import APIRouter
from backend.services.matching_service import match_resume

router = APIRouter(prefix="/match", tags=["Matching"])

@router.post("/")
def match(resume_data: dict, jd_data: dict):

    result = match_resume(resume_data, jd_data)

    return result