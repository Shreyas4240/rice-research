import json
import os
from rake_nltk import Rake

FACULTY_JSON = "/Users/shreyas/rice_research/RiceResearchFinder/backend/data/faculty.json"
UI_JSON = "/Users/shreyas/rice_research/RiceResearchFinder/ui/public/faculty.json"

with open(FACULTY_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

r = Rake(min_length=1, max_length=3)

updated = 0
for rec in data:
    if not rec.get("scholar_interests") or len(rec.get("scholar_interests", [])) == 0:
        raw = rec.get("research_summary") or rec.get("ai_review") or ""
        if not raw:
            continue
            
        r.extract_keywords_from_text(raw)
        phrases = r.get_ranked_phrases()
        
        clean_phrases = []
        for p in phrases[:15]:
            if p.replace(" ", "").isalpha() and len(p) > 4:
                # Basic capitalize
                clean_phrases.append(p.title())
            if len(clean_phrases) == 5:
                break
                
        if clean_phrases:
            rec["scholar_interests"] = clean_phrases
            updated += 1
            print(f"[{updated}] {rec['name']} -> {clean_phrases}")

if updated > 0:
    with open(FACULTY_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    with open(UI_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {updated} new records with NLTK interests to JSON.")
    
    db_path = "/Users/shreyas/rice_research/RiceResearchFinder/backend/tamurf.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Deleted tamurf.db to reload on backend.")
print("Done.")
