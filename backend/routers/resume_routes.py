import os
import shutil
import uuid
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Request
from models.resume_model import ResumeUploadResponse, ResumeData
from services.resume_parser import parse_resume
from dependencies import get_current_user
from config import settings
from logger import get_logger
from limiter import limiter

router = APIRouter()
logger = get_logger(__name__)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
TEMP_DIR = "temp_uploads"


@router.post("/upload_resume", response_model=ResumeUploadResponse)
@limiter.limit("20/hour")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Only PDF and DOCX files are allowed.")

    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    contents = await file.read()
    if len(contents) > max_bytes:
        raise HTTPException(413, f"File too large. Max size is {settings.max_upload_size_mb}MB.")
    await file.seek(0)

    os.makedirs(TEMP_DIR, exist_ok=True)
    safe_name = os.path.basename(file.filename)
    temp_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}_{safe_name}")

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_type = "pdf" if ext == ".pdf" else "docx"
        resume_data = parse_resume(temp_path, file_type)
        if "error" in resume_data:
            raise HTTPException(500, resume_data["error"])
        logger.info(f"Resume parsed for user: {current_user['email']}")
        return ResumeUploadResponse(
            message="Resume uploaded and parsed successfully",
            resume_data=ResumeData(**resume_data),
            filename=file.filename,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Resume processing error: {e}")
        raise HTTPException(500, f"Error processing resume: {e}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)