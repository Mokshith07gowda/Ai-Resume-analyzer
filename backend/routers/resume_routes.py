from fastapi import APIRouter, UploadFile, File, HTTPException
from ..models.resume_model import ResumeUploadResponse, ResumeData
from ..services.resume_parser import parse_resume
import os
import shutil
import uuid

router = APIRouter()


@router.post("/upload_resume", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse a resume file (PDF or DOCX).
    
    Args:
        file: Uploaded resume file
        
    Returns:
        Parsed resume data
    """
    # Validate file type
    allowed_extensions = [".pdf", ".docx"]
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only PDF and DOCX files are allowed."
        )
    
    # Save uploaded file temporarily
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    safe_name = os.path.basename(file.filename)
    temp_file_path = os.path.join(temp_dir, f"{uuid.uuid4().hex}_{safe_name}")
    
    try:
        # Save file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Determine file type
        file_type = "pdf" if file_extension == ".pdf" else "docx"
        
        # Parse resume
        resume_data = parse_resume(temp_file_path, file_type)
        
        if "error" in resume_data:
            raise HTTPException(status_code=500, detail=resume_data["error"])
        
        return ResumeUploadResponse(
            message="Resume uploaded and parsed successfully",
            resume_data=ResumeData(**resume_data),
            filename=file.filename
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
