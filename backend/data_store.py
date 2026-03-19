"""
Central data store for faculty data to avoid circular imports.
"""

import json
from pathlib import Path

# Global faculty data
_faculty_data = []

def load_faculty_data():
    """Load faculty data from JSON file."""
    global _faculty_data
    if _faculty_data:
        return _faculty_data
    
    candidates = [
        Path(__file__).parent.parent / "ui" / "public" / "faculty.json",
        Path(__file__).parent / "data" / "faculty.json",
    ]
    
    for path in candidates:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                _faculty_data = json.load(f)
            print(f"✓ Loaded {len(_faculty_data)} faculty records from {path}")
            return _faculty_data
    
    print("⚠ No faculty.json found")
    _faculty_data = []
    return _faculty_data

def get_faculty_data():
    """Get faculty data - used by routers"""
    if not _faculty_data:
        load_faculty_data()
    return _faculty_data

def find_faculty_by_id(faculty_id: str):
    """Find faculty by ID in the JSON data."""
    faculty_data = get_faculty_data()
    for faculty in faculty_data:
        if faculty.get("id") == faculty_id:
            return faculty
    return None
