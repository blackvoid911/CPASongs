#!/usr/bin/env python3
"""
Fetch Urdu Bible from cpa-pk.org/bible/
"""

import urllib.request
import urllib.parse
import ssl
import json
import re
import time
import os

# Create SSL context that doesn't verify certificates (for testing)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_url(url, retries=3):
    """Fetch URL with retries and proper headers"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                return resp.read().decode('utf-8')
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)
    return None

print("=" * 60)
print("Fetching Urdu Bible from https://cpa-pk.org/bible/")
print("=" * 60)

# Step 1: Fetch the main Bible page
print("\n1. Fetching main Bible page...")
main_page = fetch_url("https://cpa-pk.org/bible/")

if main_page:
    print(f"   Page fetched, length: {len(main_page)} characters")
    print("\n   First 2000 characters:")
    print("-" * 40)
    print(main_page[:2000])
    print("-" * 40)

    # Save the page for inspection
    with open("cpa_bible_main.html", "w", encoding="utf-8") as f:
        f.write(main_page)
    print("\n   Saved to cpa_bible_main.html")

    # Look for links to books/chapters
    links = re.findall(r'href=["\']([^"\']*bible[^"\']*)["\']', main_page, re.IGNORECASE)
    print(f"\n   Found {len(links)} Bible-related links:")
    for link in links[:20]:
        print(f"   - {link}")
else:
    print("   Failed to fetch main page!")

# Try alternate URLs
print("\n2. Trying alternate URLs...")
alternate_urls = [
    "https://cpa-pk.org/bible/index.php",
    "https://cpa-pk.org/bible/genesis/1",
    "https://cpa-pk.org/bible/api/",
    "https://cpa-pk.org/api/bible/",
    "https://cpa-pk.org/bible/?book=genesis&chapter=1",
]

for url in alternate_urls:
    print(f"\n   Testing: {url}")
    content = fetch_url(url)
    if content:
        print(f"   SUCCESS - {len(content)} characters")
        print(f"   Preview: {content[:300]}...")
    else:
        print("   FAILED")

