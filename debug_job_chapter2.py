"""
Debug: Check what's in job.html for chapter 2
"""
import re
from bs4 import BeautifulSoup

CACHE_FILE = r"C:\xampp\htdocs\cpa\cache\bible\job.html"

with open(CACHE_FILE, encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Look for chapter 2 verses
ch2_pattern = re.compile(r"^JOB\.2\.\d+$", re.IGNORECASE)
ch2_verses = soup.find_all("span", id=ch2_pattern)

print(f"Found {len(ch2_verses)} potential chapter 2 verse spans")

if ch2_verses:
    print("\nFirst 3 chapter 2 verses:")
    for i, span in enumerate(ch2_verses[:3], 1):
        verse_id = span.get("id", "")
        text = span.get_text(strip=True)[:100]
        print(f"  {i}. ID: {verse_id}")
        print(f"     Text: {text}...")
        print(f"     Has Urdu: {any('\u0600' <= c <= '\u06ff' for c in text)}")
else:
    print("\nNo chapter 2 verses found with pattern JOB.2.*")

    # Try broader search
    print("\nSearching for any JOB.2. references...")
    all_job = soup.find_all("span", id=re.compile(r"JOB\.", re.IGNORECASE))
    ch2_refs = [s for s in all_job if ".2." in s.get("id", "").upper()]
    print(f"Found {len(ch2_refs)} spans with '.2.' in ID")

    if ch2_refs:
        for span in ch2_refs[:5]:
            print(f"  {span.get('id')}: {span.get_text(strip=True)[:50]}")

