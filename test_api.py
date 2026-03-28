import urllib.request
import json
import time

# Wait for rate limit
print("Waiting 15 seconds for API rate limit...")
time.sleep(15)

# Test the API
try:
    req = urllib.request.Request(
        'https://bible-api.com/genesis+1?translation=kjv',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        if 'verses' in data:
            print(f"Success! Found {len(data['verses'])} verses")
        elif 'error' in data:
            print(f"Error: {data['error']}")
        else:
            print("Unknown response format")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
except Exception as e:
    print(f"Error: {e}")

