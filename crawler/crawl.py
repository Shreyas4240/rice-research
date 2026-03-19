#!/usr/bin/env python3
"""
Rice University Engineering Faculty Crawler
=================================
Crawls faculty directory pages and individual profile pages to build a
structured research dataset via their Drupal JSON API.

Usage:
  python crawl.py                                  # uses seeds.txt
  python crawl.py <url1> <url2> ...                # CLI seeds (appended to seeds.txt seeds)
  python crawl.py --no-cache                       # clear cache and re-download everything
"""

from __future__ import annotations

import sys
# Force UTF-8 output on Windows (avoids cp1252 UnicodeEncodeError for non-ASCII names)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import argparse
import asyncio
import csv
import hashlib
import json
import os
import re
import shutil
import time
import urllib.request
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

# ---------------------------------------------------------------------------
# Gemini AI setup
# ---------------------------------------------------------------------------

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

_GEMINI_MODEL = None
_GEMINI_DISABLED = False  # Set to True after quota/auth errors to skip all future calls

def _get_gemini_model():
    global _GEMINI_MODEL, _GEMINI_DISABLED
    if _GEMINI_DISABLED:
        return None
    if _GEMINI_MODEL is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            _GEMINI_DISABLED = True
            return None
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            _GEMINI_MODEL = genai.GenerativeModel("gemini-3.1-flash-lite-preview")
        except Exception as exc:
            print(f"  [warn] Could not initialise Gemini: {exc}")
            _GEMINI_DISABLED = True
            return None
    return _GEMINI_MODEL


def generate_ai_review(name: str, department: str, research_summary: str) -> str:
    """Use Gemini to write a comprehensive, readable research review."""
    global _GEMINI_DISABLED
    if _GEMINI_DISABLED:
        return ""
    model = _get_gemini_model()
    if model is None:
        return ""
    # Skip stub/empty summaries
    cleaned = research_summary.replace("|", ",").strip()
    if len(cleaned) < 40:
        return ""
    prompt = (
        f"You are an academic writing assistant. Based on the following scraped research "
        f"information about a professor, write a comprehensive yet concise review (4-6 sentences) "
        f"of their research work that a student could read to quickly understand what this "
        f"professor does and what their lab focuses on. Write in third person. Be specific "
        f"about research topics and methods. Do not fabricate details beyond what is provided.\n\n"
        f"Professor: {name}\n"
        f"Department: {department}\n"
        f"Research information: {cleaned[:1000]}\n\n"
        f"Write the review as a single paragraph with no heading or bullet points."
    )
    try:
        response = model.generate_content(prompt)
        time.sleep(1)  # rate-limit Gemini calls
        return response.text.strip()
    except Exception as exc:
        exc_str = str(exc).lower()
        if "quota" in exc_str or "resource_exhausted" in exc_str or "429" in exc_str:
            print(f"  [warn] Gemini quota exhausted — disabling AI reviews for this run.")
        else:
            print(f"  [warn] Gemini call failed for {name}: {type(exc).__name__}")
        _GEMINI_DISABLED = True
        return ""

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent.resolve()
CACHE_DIR   = BASE_DIR / ".cache"
OUTPUT_JSON = BASE_DIR / "faculty.json"
OUTPUT_CSV  = BASE_DIR / "faculty.csv"
SEEDS_FILE  = BASE_DIR / "seeds.txt"

RATE_LIMIT_SECONDS = 1.5   # polite delay between non-cached requests
MAX_RETRIES        = 3
PAGE_TIMEOUT_MS    = 45_000  # 45 s

CSV_FIELDS = ["id", "name", "title", "department", "email",
              "profile_url", "research_summary", "lab_website",
              "google_scholar", "ai_review", "photo_url", "phone", "office",
              "scholar_interests", "publications"]

# ---------------------------------------------------------------------------
# Disk cache helpers
# ---------------------------------------------------------------------------

def _cache_path(url: str) -> Path:
    key = hashlib.md5(url.encode()).hexdigest()
    return CACHE_DIR / f"{key}.html"


def _load_cache(url: str) -> Optional[str]:
    p = _cache_path(url)
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else None


def _save_cache(url: str, content: str) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    _cache_path(url).write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# URL / slug helpers
# ---------------------------------------------------------------------------

def dept_slug_from_url(url: str) -> str:
    """
    Derive a short department slug from a Rice directory URL.
    e.g. https://chbe.rice.edu/people/faculty -> 'chbe'
    """
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if host.endswith(".rice.edu"):
        slug = host.replace(".rice.edu", "")
        if slug in ("www", "engineering", "profiles", "csweb"):
            # Try to grab it from the path or default
            if "csweb" in slug: return "cs"
            return "engineering"
        return slug
    return "unknown"


# ---------------------------------------------------------------------------
# Page fetching (Playwright + cache + retry)
# ---------------------------------------------------------------------------

async def fetch_html(page, url: str, retries: int = MAX_RETRIES) -> Optional[str]:
    """Return rendered HTML for *url*, using cache when available."""
    cached = _load_cache(url)
    if cached is not None:
        return cached

    for attempt in range(retries):
        try:
            await page.goto(url, wait_until="networkidle", timeout=PAGE_TIMEOUT_MS)
            
            # Wait for any .view-content or grid to show up
            try:
                await page.wait_for_selector('.view-content', timeout=5000)
            except PlaywrightTimeout:
                pass
                
                # Keep hitting "Load More" until it's gone for lazy loaded departments
            for _ in range(10):
                try:
                    load_more = await page.query_selector('.pager a:has-text("Load More"), ul.js-pager__items a:has-text("Load More"), .pagination a:has-text("Load More")')
                    if load_more:
                        await load_more.click()
                        await page.wait_for_timeout(1000)
                    else:
                        break
                except Exception:
                    break
                    
            await asyncio.sleep(2)  # Extra settle time
            
            html = await page.content()
            _save_cache(url, html)
            await asyncio.sleep(RATE_LIMIT_SECONDS)
            return html
        except PlaywrightTimeout:
            if attempt < retries - 1:
                wait = 2 ** attempt
                print(f"  [timeout] {url}  — retry in {wait}s …")
                await asyncio.sleep(wait)
            else:
                print(f"  [failed]  {url}  — giving up after {retries} attempts")
        except Exception as exc:
            print(f"  [error]   {url}  — {exc}")
            if attempt >= retries - 1:
                return None
            await asyncio.sleep(2 ** attempt)

    return None

def fetch_json(url: str, retries: int = MAX_RETRIES) -> dict:
    """Fetch JSON from a URL synchronously using urllib, handling typical blockades."""
    cached = _load_cache(url)
    if cached is not None:
        try:
            return json.loads(cached)
        except Exception:
            pass

    req = urllib.request.Request(url, headers={
        'User-Agent': 'curl/7.88.1',
        'Accept': 'application/json'
    })
    
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read().decode('utf-8')
                data = json.loads(content)
                _save_cache(url, content)
                return data
        except Exception as exc:
            if attempt >= retries - 1:
                print(f"  [error] JSON fetch failed for {url}: {exc}")
                return {}
            time.sleep(2 ** attempt)
            
    return {}

# ---------------------------------------------------------------------------
# Profile-link extraction from directory pages
# ---------------------------------------------------------------------------

def extract_profile_links(html: str, base_url: str) -> list[str]:
    """
    Return sorted, deduplicated absolute profile URLs found in Rice directories.
    """
    found: set[str] = set()
    soup = BeautifulSoup(html, "html.parser")
    
    # Just find any link containing the profile path
    for a in soup.find_all("a", href=True):
        href = a["href"]
        
        # Rice uses either direct profiles.rice.edu links or relative /faculty/name links
        if "profiles.rice.edu/faculty/" in href:
            full = href.split("#")[0].split("?")[0]
            found.add(full)
        elif "/faculty/" in href:
            # Extract the slug and force map to profiles.rice.edu
            slug = href.split("/faculty/")[-1].split("#")[0].split("?")[0].strip("/")
            if slug:
                found.add(f"https://profiles.rice.edu/faculty/{slug}")

    return sorted(found)


# ---------------------------------------------------------------------------
# Profile-page field extraction (via Drupal JSON API)
# ---------------------------------------------------------------------------

def extract_profile_fields(profile_json: dict, profile_url: str) -> dict:
    """
    Parse a Rice faculty profile from the Drupal API JSON response.
    """
    if not profile_json:
        return {"name": "", "title": "", "email": "", "research_summary": "", 
                "lab_website": "", "google_scholar": "", "photo_url": "", 
                "phone": "", "office": ""}
    
    def get_val(key, attr='value'):
        items = profile_json.get(key, [])
        if items and len(items) > 0 and attr in items[0]:
            return items[0][attr]
        return ""

    first_name = get_val("field_first_name")
    last_name = get_val("field_last_name")
    # If API lacks first/last, fallback to username or title piece 
    if not first_name and not last_name:
        name = get_val("title")
    else:
        name = f"{first_name} {last_name}".strip()
    
    # Title could have multiple roles
    titles = [item.get("value", "") for item in profile_json.get("field_title", [])]
    title = " | ".join(filter(None, titles))

    email = get_val("field_email")
    phone = get_val("field_phone")
    office = get_val("field_address")
    
    # Research summary
    research_summary = ""
    body_html = get_val("body")
    if body_html:
        soup = BeautifulSoup(body_html, "html.parser")
        research_summary = soup.get_text(" ", strip=True)
    if not research_summary:
        research_summary = get_val("field_research_areas")
    
    photo_url = get_val("field_image", "url")
        
    # Links
    google_scholar = ""
    lab_website = ""
    for link_item in profile_json.get("field_links", []):
        link_title = link_item.get("title", "").lower()
        uri = link_item.get("uri", "")
        if "scholar" in link_title or "scholar.google" in uri:
            google_scholar = uri
        elif any(kw in link_title for kw in ("lab", "website", "group", "research site", "personal")):
            lab_website = uri
            
    return {
        "name":             name,
        "title":            title,
        "email":            email,
        "research_summary": research_summary,
        "lab_website":      lab_website,
        "google_scholar":   google_scholar,
        "photo_url":        photo_url,
        "phone":            phone,
        "office":           office,
    }


# ---------------------------------------------------------------------------
# Main crawl routine
# ---------------------------------------------------------------------------

async def crawl(seed_urls: list[str]) -> list[dict]:
    all_records: list[dict] = []
    seen_profile_urls: set[str] = set()

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)

        for seed_url in seed_urls:
            # Using a clean context per directory to avoid Rice WAF rate-limiting across sequential navigations
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
                ignore_https_errors=True
            )
            page = await context.new_page()

            print(f"\n[directory] {seed_url}")
            html = await fetch_html(page, seed_url)
            
            await context.close()
            await asyncio.sleep(2) # Give WAF time to cool off
            
            if html is None:
                print("  Skipping — could not load directory page.")
                continue


            profile_links = extract_profile_links(html, seed_url)
            dept_slug = dept_slug_from_url(seed_url)
            print(f"  Found {len(profile_links)} profile link(s)  dept={dept_slug!r}")

            for profile_url in profile_links:
                if profile_url in seen_profile_urls:
                    print(f"  [dup]     {profile_url}")
                    continue
                seen_profile_urls.add(profile_url)

                print(f"  [profile] {profile_url}")
                
                # Fetch profile data from API
                json_url = profile_url + "?_format=json"
                profile_json = await asyncio.to_thread(fetch_json, json_url)
                
                if not profile_json:
                    print(f"    [warn]  No JSON data returned. Skipping.")
                    continue
                    
                fields = extract_profile_fields(profile_json, profile_url)
                
                # If name extraction fails drastically, skip 
                if not fields.get("name"):
                    fields["name"] = profile_url.split("/")[-1].replace("-", " ").title()

                # Generate AI review
                ai_review = generate_ai_review(
                    fields["name"], dept_slug, fields["research_summary"]
                )

                record = {
                    "id":          hashlib.md5(profile_url.encode()).hexdigest()[:12],
                    "profile_url": profile_url,
                    "department":  dept_slug,
                    **fields,
                    "ai_review":         ai_review,
                    "scholar_interests": [],
                    "publications":      [],
                }
                all_records.append(record)
                print(f"    name={record['name']!r} | title={record['title'][:30]!r}")
                
                await asyncio.sleep(RATE_LIMIT_SECONDS)

            # Write after each department so results are available incrementally
            if all_records:
                save_outputs(all_records)

        await browser.close()

    return all_records


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def save_outputs(records: list[dict]) -> None:
    OUTPUT_JSON.write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nWrote {len(records)} records → {OUTPUT_JSON}")

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    print(f"Wrote {len(records)} records → {OUTPUT_CSV}")


# ---------------------------------------------------------------------------
# Seeds loading
# ---------------------------------------------------------------------------

def load_seeds() -> list[str]:
    urls: list[str] = []
    if SEEDS_FILE.exists():
        for line in SEEDS_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rice University Engineering Faculty Crawler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "urls",
        nargs="*",
        metavar="URL",
        help="Extra seed directory URL(s) (appended to seeds.txt seeds)",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Delete disk cache and re-download all pages",
    )
    args = parser.parse_args()

    if args.no_cache and CACHE_DIR.exists():
        shutil.rmtree(CACHE_DIR)
        print("Cache cleared.")

    seeds = load_seeds() + list(args.urls)

    # Deduplicate, preserve order
    seen: set[str] = set()
    unique_seeds: list[str] = []
    for s in seeds:
        if s not in seen:
            seen.add(s)
            unique_seeds.append(s)

    if not unique_seeds:
        parser.error(
            "No seed URLs found. Add them to seeds.txt or pass as CLI arguments."
        )

    print(f"Crawling {len(unique_seeds)} seed URL(s) …")
    records = asyncio.run(crawl(unique_seeds))

    if records:
        save_outputs(records)
    else:
        print("No records collected.")


if __name__ == "__main__":
    main()
