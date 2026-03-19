from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services import matcher
from data_store import get_faculty_data
from routers.resume_simple import sessions

router = APIRouter()


class MatchRequest(BaseModel):
    session_id: str
    interests: str = ""
    top_n: int = 20


@router.post("")
def run_match(req: MatchRequest):
    # Load session
    session = sessions.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found. Please upload a resume first.")

    # Effective interests: prefer request body (user may have updated them)
    interests = req.interests.strip() or session.get("interests", "")
    resume_profile = session.get("parsed_profile", {})

    # Load faculty from JSON
    faculty_data = get_faculty_data()
    if not faculty_data:
        raise HTTPException(
            status_code=503,
            detail="No faculty data loaded.",
        )

    results = matcher.match_faculty(
        faculty=faculty_data,
        interests=interests,
        resume_profile=resume_profile,
        top_n=min(req.top_n, 50),
    )

    return {
        "session_id": req.session_id,
        "interests": interests,
        "resume_profile": resume_profile,
        "total": len(results),
        "matches": results,
        "mock_mode": matcher.llm.MOCK_MODE,
    }
