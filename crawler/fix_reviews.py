import json
import re

with open("faculty.json", "r") as f:
    data = json.load(f)

count = 0
for r in data:
    rev = r.get("ai_review", "")
    if "The user wants:" in rev or "Potential answer:" in rev or "Write the review as" in rev or "We need to produce" in rev or "We need to write" in rev:
        # It's a broken review
        # Find all quoted blocks longer than 150 chars
        matches = re.findall(r'"([^"]{150,})"', rev)
        if matches:
            # The last match is usually the final selected paragraph
            final_review = matches[-1].strip().replace('\n', ' ')
            r["ai_review"] = final_review
            count += 1
            print(f"Fixed {r['name']}")
        else:
            # fallback if no quotes used
            print(f"COULD NOT FIX: {r['name']}")

with open("faculty_fixed.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Fixed {count} reviews.")
