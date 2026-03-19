#!/usr/bin/env python3
"""
merge_results.py — Merge AI reviews and Google Scholar data into a final dataset.

Reads from:
  - faculty.json (contains the latest AI reviews from enrich.py)
  - faculty_scholar.json (contains the latest Scholar data from enrich_scholar_safe.py)

Writes to:
  - faculty_final.json
  - faculty_final.csv
"""

import json
import csv
import sys
from pathlib import Path

DIR = Path(__file__).parent
FILE_MAIN = DIR / "faculty.json"
FILE_SCHOLAR = DIR / "faculty_scholar.json"
FILE_OUT_JSON = DIR / "faculty_final.json"
FILE_OUT_CSV = DIR / "faculty_final.csv"


def build_csv_row(rec):
    """Flattens a record into a dictionary suitable for CSV."""
    def clean(val):
        if not val:
            return ""
        # Remove newlines and pipe characters which might break simple CSVs
        return str(val).replace("\n", " ").replace("\r", " ").replace("|", ",")

    interests = rec.get("scholar_interests", [])
    pubs = rec.get("publications", [])

    return {
        "id": clean(rec.get("id")),
        "name": clean(rec.get("name")),
        "department": clean(rec.get("department")),
        "title": clean(rec.get("title")),
        "email": clean(rec.get("email")),
        "phone": clean(rec.get("phone")),
        "office": clean(rec.get("office")),
        "profile_url": clean(rec.get("profile_url")),
        "lab_website": clean(rec.get("lab_website")),
        "google_scholar": clean(rec.get("google_scholar")),
        "photo_url": clean(rec.get("photo_url")),
        "research_summary": clean(rec.get("research_summary")),
        "ai_review": clean(rec.get("ai_review")),
        "scholar_interests": clean("; ".join(interests)),
        "publications_count": str(len(pubs)),
        "top_publication": clean(pubs[0]["title"] if pubs else "")
    }


def main():
    if not FILE_MAIN.exists():
        print(f"Error: {FILE_MAIN} not found.")
        sys.exit(1)
        
    main_data = json.loads(FILE_MAIN.read_text(encoding="utf-8"))
    print(f"Loaded {len(main_data)} records from {FILE_MAIN.name}")
    
    scholar_data = []
    if FILE_SCHOLAR.exists():
        scholar_data = json.loads(FILE_SCHOLAR.read_text(encoding="utf-8"))
        print(f"Loaded {len(scholar_data)} records from {FILE_SCHOLAR.name}")
    else:
        print(f"Warning: {FILE_SCHOLAR} not found. Merging empty Scholar data.")
        
    # Build lookup by ID
    scholar_lookup = {r["id"]: r for r in scholar_data if "id" in r}
    
    merged_count = 0
    for rec in main_data:
        rec_id = rec.get("id")
        if not rec_id:
            continue
            
        # If we have scholar data for this ID, merge the specific fields over
        if rec_id in scholar_lookup:
            s_rec = scholar_lookup[rec_id]
            # Bring over the new lists if they exist in the scholar dataset
            if "scholar_interests" in s_rec:
                rec["scholar_interests"] = s_rec["scholar_interests"]
                if len(s_rec["scholar_interests"]) > 0:
                    merged_count += 1
            if "publications" in s_rec:
                rec["publications"] = s_rec["publications"]

    # 1. Output JSON
    FILE_OUT_JSON.write_text(json.dumps(main_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(main_data)} merged records to {FILE_OUT_JSON.name} (Updated {merged_count} with Scholar data)")

    # 2. Output CSV
    if main_data:
        fieldnames = [
            "id", "name", "department", "title", "email", "phone", "office",
            "profile_url", "lab_website", "google_scholar", "photo_url",
            "research_summary", "ai_review", "scholar_interests", 
            "publications_count", "top_publication"
        ]
        with FILE_OUT_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for rec in main_data:
                writer.writerow(build_csv_row(rec))
        print(f"Wrote {len(main_data)} merged records to {FILE_OUT_CSV.name}")


if __name__ == "__main__":
    main()
