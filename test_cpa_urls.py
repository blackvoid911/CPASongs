"""
Test CPA Bible URLs to discover the correct patterns
"""
import urllib.request
import ssl
import re

ctx = ssl.create_default_context()

# Test different URL patterns
test_urls = [
    ("Genesis", "https://cpa-pk.org/bible/gen/"),
    ("Exodus", "https://cpa-pk.org/bible/exod/"),
    ("Exodus2", "https://cpa-pk.org/bible/ex/"),
    ("Exodus3", "https://cpa-pk.org/bible/exodus/"),
    ("Matthew", "https://cpa-pk.org/bible/matt/"),
    ("Matthew2", "https://cpa-pk.org/bible/mt/"),
    ("Psalms", "https://cpa-pk.org/bible/ps/"),
    ("Psalms2", "https://cpa-pk.org/bible/psalm/"),
    ("John", "https://cpa-pk.org/bible/john/"),
    ("John2", "https://cpa-pk.org/bible/jn/"),
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

results = []

for name, url in test_urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            html = resp.read().decode('utf-8')
            # Check if it has verse content
            has_verses = '<span class="vn">' in html
            # Find book ID
            id_match = re.search(r'<span\s+id="([A-Z0-9]+)\.\d+\.\d+"', html)
            book_id = id_match.group(1) if id_match else "UNKNOWN"
            results.append(f"OK: {name} -> {url} (ID: {book_id}, Verses: {has_verses})")
    except urllib.error.HTTPError as e:
        results.append(f"ERR {e.code}: {name} -> {url}")
    except Exception as e:
        results.append(f"ERR: {name} -> {url} ({e})")

# Write results to file
with open("cpa_url_test.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))

print("\n".join(results))
print("\nResults saved to cpa_url_test.txt")

