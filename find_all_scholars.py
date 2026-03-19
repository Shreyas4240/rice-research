#!/usr/bin/env python3
"""
Systematically search Google Scholar for Rice faculty and add their profiles
"""
import json
import time
import requests
from bs4 import BeautifulSoup
import re

def search_google_scholar(name):
    """Search Google Scholar for a person's profile"""
    try:
        # Format search query
        query = f"{name} Rice University"
        url = f"https://scholar.google.com/scholar?q={query.replace(' ', '+')}&hl=en&as_sdt=0,5"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for profile links
        profile_links = soup.find_all('a', href=re.compile(r'scholar.google.com/citations\?user='))
        
        if profile_links:
            # Get the first profile link
            profile_url = profile_links[0]['href']
            # Make sure it's a full URL
            if profile_url.startswith('/'):
                profile_url = 'https://scholar.google.com' + profile_url
            return profile_url
        
        return None
        
    except Exception as e:
        print(f"Error searching for {name}: {e}")
        return None

def main():
    # Read faculty data
    with open('ui/public/faculty.json', 'r') as f:
        faculty = json.load(f)
    
    updated_count = 0
    total_missing = 0
    
    for i, prof in enumerate(faculty):
        name = prof.get('name')
        current_scholar = prof.get('google_scholar')
        
        # Skip if already has Google Scholar
        if current_scholar and current_scholar.strip():
            continue
            
        total_missing += 1
        print(f"Searching for {name} ({i+1}/{len(faculty)})...")
        
        # Search Google Scholar
        scholar_url = search_google_scholar(name)
        
        if scholar_url:
            prof['google_scholar'] = scholar_url
            print(f"  ✓ Found: {scholar_url}")
            updated_count += 1
        else:
            print(f"  ✗ Not found")
        
        # Add delay to avoid rate limiting
        time.sleep(2)
        
        # Save progress every 10 updates
        if updated_count > 0 and updated_count % 10 == 0:
            with open('ui/public/faculty.json', 'w') as f:
                json.dump(faculty, f, indent=2, ensure_ascii=False)
            print(f"Progress saved: {updated_count} profiles added")
    
    # Final save
    with open('ui/public/faculty.json', 'w') as f:
        json.dump(faculty, f, indent=2, ensure_ascii=False)
    
    with open('backend/data/faculty.json', 'w') as f:
        json.dump(faculty, f, indent=2, ensure_ascii=False)
    
    print(f"\nComplete! Found Google Scholar for {updated_count} out of {total_missing} missing faculty")

if __name__ == "__main__":
    main()
