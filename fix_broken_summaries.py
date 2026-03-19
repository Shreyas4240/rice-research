#!/usr/bin/env python3
"""
Script to identify and fix broken AI summaries in faculty.json
"""

import json
import re

def is_broken_summary(summary):
    """Check if an AI summary is broken"""
    if not summary or summary.strip() == "":
        return True, "Empty summary"
    
    # Meta-commentary about the summary itself
    meta_patterns = [
        r"That's \d+ sentences",
        r"It's third person",
        r"It's a single paragraph",
        r"check if any detail",
        r"unless it's implied",
        r"It might be too much",
        r"Potential paragraph",
        r"Thus we should rewrite"
    ]
    
    for pattern in meta_patterns:
        if re.search(pattern, summary, re.IGNORECASE):
            return True, f"Meta-commentary: {pattern}"
    
    # Very short summaries that are likely just the research summary repeated
    if len(summary.strip()) < 50:
        return True, "Too short - likely just research summary"
    
    # Summaries that are exactly the research summary
    common_broken = [
        "Condensed Matter Experiment",
        "Computer Science",
        "Electrical Engineering",
        "Mechanical Engineering"
    ]
    
    if summary.strip() in common_broken:
        return True, "Likely just department/field name"
    
    return False, ""

def generate_proper_summary(faculty_member):
    """Generate a proper AI summary based on research summary"""
    name = faculty_member.get('name', 'This professor')
    title = faculty_member.get('title', '')
    research_summary = faculty_member.get('research_summary', '')
    department = faculty_member.get('department', '')
    
    # Extract key information from research summary
    if research_summary and len(research_summary) > 100:
        # Take first meaningful part of research summary
        sentences = re.split(r'[.!?]+', research_summary)
        first_sentence = sentences[0].strip() if sentences else ""
        
        if len(first_sentence) > 50:
            # Clean up and format
            summary = f"{name}, {title}, specializes in {first_sentence.lower()}"
            if not summary.endswith('.'):
                summary += '.'
            return summary
    
    # Fallback summary
    return f"{name} is a {title} whose research focuses on advancing knowledge in their field through innovative approaches and methodologies."

def main():
    # Load faculty data
    with open('ui/public/faculty.json', 'r') as f:
        faculty = json.load(f)
    
    broken_summaries = []
    fixed_count = 0
    
    for i, member in enumerate(faculty):
        ai_review = member.get('ai_review', '')
        is_broken, reason = is_broken_summary(ai_review)
        
        if is_broken:
            name = member.get('name', 'Unknown')
            broken_summaries.append({
                'index': i,
                'name': name,
                'current_summary': ai_review,
                'reason': reason
            })
            
            # Fix the summary
            new_summary = generate_proper_summary(member)
            faculty[i]['ai_review'] = new_summary
            fixed_count += 1
            print(f"Fixed {name}: {reason}")
            print(f"  Old: {ai_review[:100]}...")
            print(f"  New: {new_summary[:100]}...")
            print()
    
    # Save updated data
    if fixed_count > 0:
        with open('ui/public/faculty.json', 'w') as f:
            json.dump(faculty, f, indent=2)
        
        # Also copy to backend
        import shutil
        shutil.copy('ui/public/faculty.json', 'backend/data/faculty.json')
        
        print(f"\n✅ Fixed {fixed_count} broken AI summaries")
        print(f"📄 Updated both ui/public/faculty.json and backend/data/faculty.json")
    else:
        print("✅ No broken summaries found")

if __name__ == "__main__":
    main()
