"""
Test Bolls.life API for Urdu Bible (UGV - Urdu Geo Version)
"""
import urllib.request
import json
import ssl

ctx = ssl.create_default_context()

# Test bolls.life API
print("Testing Bolls.life Urdu Bible API...")

# Try to get available translations first
url = "https://bolls.life/get-books/UGV/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(f"SUCCESS! Got {len(data)} books")
        print(f"First book: {data[0]}")

        # Save the book list
        with open("bolls_books.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Saved book list to bolls_books.json")

except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
except Exception as e:
    print(f"Error: {e}")

# Now try to get Genesis chapter 1
print("\nTrying Genesis 1...")
url = "https://bolls.life/get-chapter/UGV/Gen/1/"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(f"SUCCESS! Got {len(data)} verses")
        if data:
            print(f"First verse: {data[0]}")

            # Save sample
            with open("bolls_genesis1.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("Saved to bolls_genesis1.json")

except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
except Exception as e:
    print(f"Error: {e}")

print("\nDone!")

