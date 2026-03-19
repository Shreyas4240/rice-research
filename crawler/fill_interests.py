import json
import os
import time
import sys
from together import Together

API_KEY = os.getenv("TOGETHER_API_KEY")
if not API_KEY:
    print("Error: TOGETHER_API_KEY not set")
    sys.exit(1)

client = Together()
MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"

FACULTY_JSON = "/Users/shreyas/rice_research/RiceResearchFinder/backend/data/faculty.json"
UI_JSON = "/Users/shreyas/rice_research/RiceResearchFinder/ui/public/faculty.json"

with open(FACULTY_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

updated = 0
for rec in data:
    if not rec.get("scholar_interests") or len(rec.get("scholar_interests", [])) == 0:
        text = rec.get("research_summary") or rec.get("ai_review") or ""
        if len(text) < 20:
            continue
            
        prompt = (
            f"You are an academic parser. Read the following text about Professor {rec.get('name')} "
            f"and extract 3 to 5 very short, distinct research interests or keywords "
            f"(e.g. 'Machine Learning', 'Computer Vision').\n\n"
            f"Text: {text[:1500]}\n\n"
            f"Output EXACTLY a valid JSON array of strings and NOTHING else. No markdown, no filler."
        )
        
        try:
            res = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You output only valid JSON arrays."},
                    {"role": "user", "content": prompt}
                ]
            )
            raw = res.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw
                raw = raw.rsplit("```", 1)[0].strip()
                
            interests = json.loads(raw)
            if isinstance(interests, list):
                rec["scholar_interests"] = interests
                updated += 1
                print(f"[{updated}] {rec['name']} -> {interests}")
            time.sleep(0.5)
        except Exception as e:
            print(f"Failed {rec.get('name')}: {e}")

if updated > 0:
    with open(FACULTY_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    with open(UI_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {updated} new records to JSON.")
    
    db_path = "/Users/shreyas/rice_research/RiceResearchFinder/backend/tamurf.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Deleted tamurf.db to force a reload on backend startup.")
        
print("Done.")
