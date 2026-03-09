from fastapi import APIRouter, UploadFile, File
from backend.services.resume_parser_service import parse_resume

router = APIRouter(prefix="/resume", tags=["Resume"])

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    
    content = await file.read()

    parsed_data = parse_resume(content)

    return {
        "message": "Resume processed",
        "data": parsed_data
    }