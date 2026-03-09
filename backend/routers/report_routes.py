from fastapi import APIRouter
from backend.services.recommendation_service import generate_report

router = APIRouter(prefix="/report", tags=["Report"])

@router.post("/generate")
def create_report(data: dict):

    report_path = generate_report(data)

    return {
        "message": "Report generated",
        "report_path": report_path
    }