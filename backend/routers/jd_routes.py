from fastapi import APIRouter, HTTPException, UploadFile, File
from ..models.jd_model import JDInput, JDProcessResponse, JDData
from ..services.jd_processor import process_job_description
from ..services.resume_parser import extract_text_from_pdf, extract_text_from_docx
import os
import shutil

router = APIRouter()


@router.post("/upload_jd", response_model=JDProcessResponse)
async def upload_jd(jd: JDInput):
    """
    Process job description and extract skills and keywords.
    
    Args:
        jd: Job description input
        
    Returns:
        Processed JD data with skills and keywords
    """
    try:
        if not jd.job_description or len(jd.job_description.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Job description cannot be empty"
            )
        
        # Process job description
        jd_data = process_job_description(jd.job_description)
        
        return JDProcessResponse(
            message="Job description processed successfully",
            jd_data=JDData(**jd_data)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing job description: {str(e)}"
        )


@router.post("/upload_jd_file", response_model=JDProcessResponse)
async def upload_jd_file(file: UploadFile = File(...)):
    """
    Upload and process job description file (PDF, DOCX, or TXT).
    
    Args:
        file: Uploaded job description file
        
    Returns:
        Processed JD data with skills and keywords
    """
    # Validate file type
    allowed_extensions = [".pdf", ".docx", ".txt"]
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only PDF, DOCX, and TXT files are allowed."
        )
    
    # Save uploaded file temporarily
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)
    
    try:
        # Save file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text based on file type
        if file_extension == ".pdf":
            jd_text = extract_text_from_pdf(temp_file_path)
        elif file_extension == ".docx":
            jd_text = extract_text_from_docx(temp_file_path)
        else:  # .txt
            with open(temp_file_path, "r", encoding="utf-8") as f:
                jd_text = f.read()
        
        # Clean up temp file
        os.remove(temp_file_path)
        
        if not jd_text or len(jd_text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the file"
            )
        
        # Process job description
        jd_data = process_job_description(jd_text)
        
        return JDProcessResponse(
            message="Job description file processed successfully",
            jd_data=JDData(**jd_data)
        )
        
    except Exception as e:
        # Clean up temp file if exists
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing job description file: {str(e)}"
        )
