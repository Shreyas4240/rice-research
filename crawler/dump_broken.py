import json
import re

with open("faculty.json", "r") as f:
    data = json.load(f)

broken = []
for r in data:
    rev = r.get("ai_review", "")
    if "The user wants:" in rev or "Potential answer:" in rev or "Write the review as" in rev or "We need to produce" in rev or "We need to write" in rev:
        broken.append(r)

with open("broken_reviews_dump.txt", "w") as f:
    for r in broken:
        f.write(f"--- {r['name']} ({r['id']}) ---\n")
        f.write(r["ai_review"] + "\n\n")
