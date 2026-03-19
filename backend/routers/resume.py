import uuid
import os
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services import parser

router = APIRouter()

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# In-memory session storage (simple approach)
sessions = {}


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    interests: str = Form(default=""),
):
    # Validate file type
    filename = file.filename or ""
    if not filename.lower().endswith((".pdf", ".docx", ".doc")):
        raise HTTPException(
            status_code=422,
            detail="Only PDF and DOCX files are supported.",
        )

    # Validate file size
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=422,
            detail="File too large. Maximum size is 10MB.",
        )

    # Generate session ID
    session_id = str(uuid.uuid4())

    try:
        # Read file content
        file_content = await file.read()
        file_bytes = file_content
        
        # Extract text from file
        text = parser.extract_text(filename, file_bytes)
        
        # Parse resume text
        parsed_profile = parser.parse_resume(text)
        
        # Store session in memory
        sessions[session_id] = {
            "session_id": session_id,
            "parsed_profile": parsed_profile,
            "interests": interests,
            "filename": filename,
        }

        return {
            "session_id": session_id,
            "parsed_profile": parsed_profile,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")


@router.get("/{session_id}")
def get_session(session_id: str):
    """Get a resume session by ID."""
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
