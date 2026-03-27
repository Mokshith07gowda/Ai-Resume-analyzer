from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from services.jd_processor import process_job_description
from dependencies import get_current_user
from limiter import limiter

router = APIRouter()


class JDInput(BaseModel):
    title: str
    company: str | None = None
    description: str


class JDResponse(BaseModel):
    title: str
    company: str | None = None
    required_skills: list
    responsibilities: list
    keywords: list
    experience_required: str
    education_required: str
    word_count: int


@router.post("/process_jd", response_model=JDResponse, status_code=status.HTTP_200_OK)
async def process_jd(jd_input: JDInput, current_user: dict = Depends(get_current_user)):
    if not jd_input.description.strip():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Job description cannot be empty")

    if len(jd_input.description) < 50:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Job description is too short")

    result = process_job_description(jd_input.description)

    if "error" in result:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, result["error"])

    return JDResponse(title=jd_input.title, company=jd_input.company, **result)