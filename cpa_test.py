"""
Fetch Urdu Bible from cpa-pk.org/bible/
This script will explore the site structure and download Bible content.
"""

import urllib.request
import urllib.parse
import ssl
import json
import re
import time
import os
import sys

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# Create SSL context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_url(url, retries=3):
    """Fetch URL with retries and proper headers"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5,ur;q=0.3',
    }

    for attempt in range(retries):
        try:
            print(f"  Fetching: {url} (attempt {attempt+1})", flush=True)
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                content = resp.read().decode('utf-8')
                print(f"  Got {len(content)} bytes", flush=True)
                return content
        except urllib.error.HTTPError as e:
            print(f"  HTTP Error {e.code}: {e.reason}", flush=True)
        except Exception as e:
            print(f"  Error: {e}", flush=True)
            if attempt < retries - 1:
                time.sleep(2)
    return None

print("=" * 60, flush=True)
print("CPA-PK.ORG Bible Fetcher", flush=True)
print("=" * 60, flush=True)

# First, check the base URL
base_urls = [
    "https://cpa-pk.org/",
    "https://cpa-pk.org/bible/",
    "http://cpa-pk.org/bible/",
    "https://www.cpa-pk.org/bible/",
]

for url in base_urls:
    print(f"\nTrying: {url}", flush=True)
    content = fetch_url(url)
    if content:
        # Save to file
        safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_")
        filename = f"cpa_{safe_name}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved to: {filename}", flush=True)
        print(f"Preview:\n{content[:1000]}", flush=True)

        # Look for book links
        links = re.findall(r'href=["\']([^"\']*)["\']', content)
        bible_links = [l for l in links if 'bible' in l.lower() or 'book' in l.lower()]
        if bible_links:
            print(f"\nFound Bible-related links: {bible_links[:10]}", flush=True)
        break
else:
    print("\nAll URLs failed!", flush=True)

print("\nDone!", flush=True)

