"""
Discover all CPA Bible book URL slugs from the index page
"""
import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
headers = {'User-Agent': 'Mozilla/5.0'}

# Get the Bible index page
url = 'https://cpa-pk.org/bible/'
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=30, context=ctx)
html = resp.read().decode('utf-8')

# Save the index page
with open('cpa_index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Find all book links
pattern = re.compile(r'href=["\'](?:https://cpa-pk\.org)?/bible/([a-z0-9]+)/?["\']', re.IGNORECASE)
slugs = list(set(pattern.findall(html)))
slugs.sort()

with open('cpa_slugs.txt', 'w') as f:
    f.write('\n'.join(slugs))

print(f'Found {len(slugs)} book slugs:')
for s in slugs:
    print(f'  {s}')

