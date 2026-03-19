from fastapi import APIRouter, HTTPException
from data_store import get_faculty_data, find_faculty_by_id

router = APIRouter()


@router.get("")
def list_faculty():
    """List all faculty."""
    faculty_data = get_faculty_data()
    return faculty_data


@router.get("/{faculty_id}")
def get_faculty(faculty_id: str):
    """Get a specific faculty member by ID."""
    faculty = find_faculty_by_id(faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty


@router.post("/import")
def import_faculty():
    """Import faculty data (no-op since we're using JSON)."""
    faculty_data = get_faculty_data()
    return {"message": f"Using JSON data with {len(faculty_data)} faculty records"}
