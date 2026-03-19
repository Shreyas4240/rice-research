#!/usr/bin/env python3
import json
import os
import sys

# Import the local NLP extraction function from enrich_local.py
from enrich_local import clean_summary

FACULTY_JSON = "/Users/shreyas/rice_research/RiceResearchFinder/backend/data/faculty.json"
UI_JSON = "/Users/shreyas/rice_research/RiceResearchFinder/ui/public/faculty.json"

with open(FACULTY_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

updated = 0
for rec in data:
    if not rec.get("scholar_interests") or len(rec.get("scholar_interests", [])) == 0:
        raw = rec.get("research_summary") or ""
        if not raw:
            continue
            
        # The clean_summary function extracts clean topics from pipeline-delimited raw strings
        topics = clean_summary(raw)
        
        # Take up to 5 clean topics and capitalize them properly
        valid_topics = [t.capitalize() for t in topics if len(t.split()) <= 4]
        if not valid_topics:
            valid_topics = [t.capitalize() for t in topics]
            
        interests = valid_topics[:5]
        
        if interests:
            rec["scholar_interests"] = interests
            updated += 1
            print(f"[{updated}] {rec['name']} -> {interests}")

if updated > 0:
    with open(FACULTY_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    with open(UI_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {updated} new records with heuristic interests to JSON.")
    
    db_path = "/Users/shreyas/rice_research/RiceResearchFinder/backend/tamurf.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Deleted tamurf.db to force a fresh DB reload on backend startup.")
        
print("Done.")
