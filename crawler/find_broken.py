import json

with open("faculty.json", "r") as f:
    data = json.load(f)

broken = []
for r in data:
    rev = r.get("ai_review", "")
    if "The user wants:" in rev or "Potential answer:" in rev or "Write the review as" in rev:
        broken.append(r)

print(f"Found {len(broken)} broken reviews.")
for r in broken:
    print(f"\n--- {r['name']} ({r['id']}) ---")
    print(r["ai_review"][:150] + " ... " + r["ai_review"][-150:])
