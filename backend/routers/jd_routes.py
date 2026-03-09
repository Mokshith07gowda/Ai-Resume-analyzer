from fastapi import APIRouter
from backend.models.schemas import JDInput
from backend.services.jd_processor_service import process_jd

router = APIRouter(prefix="/job", tags=["Job Description"])

@router.post("/upload")
def upload_jd(jd: JDInput):

    result = process_jd(jd.description)

    return {
        "message": "JD processed",
        "data": result
    }