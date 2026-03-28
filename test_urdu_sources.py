import urllib.request
import json
import time

print("Testing different Urdu Bible sources...")

# Test 1: Check bible-api.com translations
try:
    print("\n1. Testing bible-api.com translations endpoint...")
    req = urllib.request.Request(
        'https://bible-api.com/translations.json',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        urdu = [t for t in data if 'urdu' in str(t).lower() or 'urd' in str(t).lower()]
        print(f"   Found translations: {urdu if urdu else 'None'}")
except Exception as e:
    print(f"   Error: {e}")

time.sleep(3)

# Test 2: Specific Urdu test
try:
    print("\n2. Testing Urdu translations (urv, urd, urdu)...")
    for code in ['urv', 'urd', 'urdu', 'UrdB']:
        try:
            req = urllib.request.Request(
                f'https://bible-api.com/genesis+1:1?translation={code}',
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if 'verses' in data:
                    print(f"   {code}: SUCCESS - {data['verses'][0]['text'][:50]}...")
                elif 'error' in data:
                    print(f"   {code}: ERROR - {data['error']}")
        except urllib.error.HTTPError as e:
            print(f"   {code}: HTTP {e.code}")
        except Exception as e:
            print(f"   {code}: Error - {e}")
        time.sleep(2)
except Exception as e:
    print(f"   Error: {e}")

print("\n3. Checking available translations list...")
try:
    req = urllib.request.Request(
        'https://bible-api.com/translations.json',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(f"   Total translations: {len(data)}")
        print(f"   First 10: {[t['identifier'] for t in data[:10]]}")
except Exception as e:
    print(f"   Error: {e}")

