r"""
Download complete Urdu Bible from CPA website to cache directory.
Saves HTML files to C:\xampp\htdocs\cpa\cache\bible\ for later processing.
"""
import urllib.request
import os
import time
import ssl
import sys

# Fix console encoding for Urdu text
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ctx = ssl.create_default_context()
CACHE_DIR = r"C:\xampp\htdocs\cpa\cache\bible"

# CPA Bible URL slugs - these match the actual CPA website structure
# Format: (url_slug, english_name, abbr_for_filename)
BOOKS = [
    # Old Testament
    ("gen", "Genesis", "gen"),
    ("exod", "Exodus", "exo"),
    ("lev", "Leviticus", "lev"),
    ("num", "Numbers", "num"),
    ("deut", "Deuteronomy", "deu"),
    ("josh", "Joshua", "jos"),
    ("judg", "Judges", "jdg"),
    ("ruth", "Ruth", "rut"),
    ("1sam", "1 Samuel", "1sa"),
    ("2sam", "2 Samuel", "2sa"),
    ("1kgs", "1 Kings", "1ki"),
    ("2kgs", "2 Kings", "2ki"),
    ("1chr", "1 Chronicles", "1ch"),
    ("2chr", "2 Chronicles", "2ch"),
    ("ezra", "Ezra", "ezr"),
    ("neh", "Nehemiah", "neh"),
    ("esth", "Esther", "est"),
    ("job", "Job", "job"),
    ("ps", "Psalms", "psa"),
    ("prov", "Proverbs", "pro"),
    ("eccl", "Ecclesiastes", "ecc"),
    ("song", "Song of Solomon", "sng"),
    ("isa", "Isaiah", "isa"),
    ("jer", "Jeremiah", "jer"),
    ("lam", "Lamentations", "lam"),
    ("ezek", "Ezekiel", "ezk"),
    ("dan", "Daniel", "dan"),
    ("hos", "Hosea", "hos"),
    ("joel", "Joel", "jol"),
    ("amos", "Amos", "amo"),
    ("obad", "Obadiah", "oba"),
    ("jonah", "Jonah", "jon"),
    ("mic", "Micah", "mic"),
    ("nah", "Nahum", "nam"),
    ("hab", "Habakkuk", "hab"),
    ("zeph", "Zephaniah", "zep"),
    ("hag", "Haggai", "hag"),
    ("zech", "Zechariah", "zec"),
    ("mal", "Malachi", "mal"),
    # New Testament
    ("matt", "Matthew", "mat"),
    ("mark", "Mark", "mrk"),
    ("luke", "Luke", "luk"),
    ("john", "John", "jhn"),
    ("acts", "Acts", "act"),
    ("rom", "Romans", "rom"),
    ("1cor", "1 Corinthians", "1co"),
    ("2cor", "2 Corinthians", "2co"),
    ("gal", "Galatians", "gal"),
    ("eph", "Ephesians", "eph"),
    ("phil", "Philippians", "php"),
    ("col", "Colossians", "col"),
    ("1thess", "1 Thessalonians", "1th"),
    ("2thess", "2 Thessalonians", "2th"),
    ("1tim", "1 Timothy", "1ti"),
    ("2tim", "2 Timothy", "2ti"),
    ("titus", "Titus", "tit"),
    ("phlm", "Philemon", "phm"),
    ("heb", "Hebrews", "heb"),
    ("jas", "James", "jas"),
    ("1pet", "1 Peter", "1pe"),
    ("2pet", "2 Peter", "2pe"),
    ("1john", "1 John", "1jn"),
    ("2john", "2 John", "2jn"),
    ("3john", "3 John", "3jn"),
    ("jude", "Jude", "jud"),
    ("rev", "Revelation", "rev"),
]


def fetch_book(slug, book_name):
    """Fetch entire book HTML from CPA website"""
    url = f"https://cpa-pk.org/bible/{slug}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'en-US,en;q=0.5,ur;q=0.3',
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
            html = resp.read().decode('utf-8')
            print(f"  ✓ Downloaded {len(html):,} bytes")
            return html
    except urllib.error.HTTPError as e:
        print(f"  ✗ HTTP Error {e.code}: {url}")
        return None
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


def main():
    print("=" * 70)
    print("CPA Pakistan Urdu Bible Cache Downloader")
    print("=" * 70)
    print(f"Cache directory: {CACHE_DIR}\n")

    # Create cache directory if it doesn't exist
    os.makedirs(CACHE_DIR, exist_ok=True)

    total_books = len(BOOKS)
    stats = {"success": 0, "failed": 0, "skipped": 0}

    for idx, (slug, english_name, abbr) in enumerate(BOOKS, 1):
        cache_file = os.path.join(CACHE_DIR, f"{abbr}.html")

        print(f"[{idx}/{total_books}] {english_name:25s} ({abbr}.html)", end=" ")

        # Skip if already exists
        if os.path.exists(cache_file):
            file_size = os.path.getsize(cache_file)
            if file_size > 1000:  # Skip if file is substantial
                print(f"⊙ Exists ({file_size:,} bytes) - skipped")
                stats["skipped"] += 1
                continue

        # Fetch the book page
        html = fetch_book(slug, english_name)
        if not html:
            stats["failed"] += 1
            continue

        # Save to cache
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(html)
            stats["success"] += 1
        except Exception as e:
            print(f"  ✗ Failed to save: {e}")
            stats["failed"] += 1

        # Be polite to the server
        time.sleep(1.5)

    # Summary
    print("\n" + "=" * 70)
    print("DOWNLOAD COMPLETE")
    print(f"  Success: {stats['success']} books downloaded")
    print(f"  Skipped: {stats['skipped']} books (already in cache)")
    print(f"  Failed:  {stats['failed']} books")
    print("=" * 70)
    print(f"\nCache location: {CACHE_DIR}")
    print("Next step: Run 'process_complete_urdu_bible.py' to generate JSON files")


if __name__ == "__main__":
    main()


