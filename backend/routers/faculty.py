from fastapi import APIRouter, HTTPException
from main import get_faculty_data

router = APIRouter()


def find_faculty_by_id(faculty_id: str):
    """Find faculty by ID in the JSON data."""
    faculty_data = get_faculty_data()
    for faculty in faculty_data:
        if faculty.get('id') == faculty_id:
            return faculty
    return None


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
