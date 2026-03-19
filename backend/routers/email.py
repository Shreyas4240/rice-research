from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import FacultyRecord, ResumeSession
from services import emailer
from data_store import find_faculty_by_id
from routers.resume import sessions

router = APIRouter()


class DraftRequest(BaseModel):
    faculty_id: str
    tone: Literal["professional", "warm", "concise"] = "professional"
    session_id: Optional[str] = None
    interests: str = ""


@router.post("/draft")
def draft_email(req: DraftRequest):
    # Find faculty by ID
    prof = find_faculty_by_id(req.faculty_id)
    
    if not prof:
        raise HTTPException(status_code=404, detail="Faculty not found.")

    # Load resume context if session provided
    resume_profile = {}
    interests = req.interests
    
    if req.session_id:
        session = sessions.get(req.session_id)
        if session:
            resume_profile = session.get("parsed_profile", {})
            # Use session interests if not provided in request
            if not interests:
                interests = session.get("interests", "")

    # Generate email draft
    draft = emailer.generate_draft(
        prof=prof,
        resume_profile=resume_profile,
        interests=interests,
        tone=req.tone,
    )

    return {
        "faculty_id": req.faculty_id,
        "session_id": req.session_id,
        **draft,
    }
