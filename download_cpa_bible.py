"""
Fetch complete Urdu Bible from CPA Pakistan website (https://cpa-pk.org/bible/)
Uses correct URL slugs based on CPA website structure.
"""
import urllib.request
import json
import os
import re
import time
import ssl
import sys

# Fix console encoding for Urdu text
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

ctx = ssl.create_default_context()
OUTPUT_DIR = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"

# CPA Bible URL slugs - these match the actual CPA website structure
# Format: (url_slug, english_name, urdu_name, file_name, chapters)
BOOKS = [
    # Old Testament
    ("gen", "Genesis", "پیدائش", "genesis.json", 50),
    ("exod", "Exodus", "خُروج", "exodus.json", 40),
    ("lev", "Leviticus", "احبار", "leviticus.json", 27),
    ("num", "Numbers", "گنتی", "numbers.json", 36),
    ("deut", "Deuteronomy", "اِستِثنا", "deuteronomy.json", 34),
    ("josh", "Joshua", "یشُوع", "joshua.json", 24),
    ("judg", "Judges", "قُضاۃ", "judges.json", 21),
    ("ruth", "Ruth", "رُوت", "ruth.json", 4),
    ("1sam", "1 Samuel", "۱-سموئیل", "1samuel.json", 31),
    ("2sam", "2 Samuel", "۲-سموئیل", "2samuel.json", 24),
    ("1kgs", "1 Kings", "۱-سلاطین", "1kings.json", 22),
    ("2kgs", "2 Kings", "۲-سلاطین", "2kings.json", 25),
    ("1chr", "1 Chronicles", "۱-تواریخ", "1chronicles.json", 29),
    ("2chr", "2 Chronicles", "۲-تواریخ", "2chronicles.json", 36),
    ("ezra", "Ezra", "عزرا", "ezra.json", 10),
    ("neh", "Nehemiah", "نحمیاہ", "nehemiah.json", 13),
    ("esth", "Esther", "آستر", "esther.json", 10),
    ("job", "Job", "ایّوب", "job.json", 42),
    ("ps", "Psalms", "زبُور", "psalms.json", 150),
    ("prov", "Proverbs", "امثال", "proverbs.json", 31),
    ("eccl", "Ecclesiastes", "واعظ", "ecclesiastes.json", 12),
    ("song", "Song of Solomon", "غزل الغزلات", "songofsolomon.json", 8),
    ("isa", "Isaiah", "یسعیاہ", "isaiah.json", 66),
    ("jer", "Jeremiah", "یرمیاہ", "jeremiah.json", 52),
    ("lam", "Lamentations", "نوحہ", "lamentations.json", 5),
    ("ezek", "Ezekiel", "حزقی ایل", "ezekiel.json", 48),
    ("dan", "Daniel", "دانی ایل", "daniel.json", 12),
    ("hos", "Hosea", "ہوسیع", "hosea.json", 14),
    ("joel", "Joel", "یوایل", "joel.json", 3),
    ("amos", "Amos", "عاموس", "amos.json", 9),
    ("obad", "Obadiah", "عبدیاہ", "obadiah.json", 1),
    ("jonah", "Jonah", "یُوناہ", "jonah.json", 4),
    ("mic", "Micah", "میکاہ", "micah.json", 7),
    ("nah", "Nahum", "ناحُوم", "nahum.json", 3),
    ("hab", "Habakkuk", "حبقُّوق", "habakkuk.json", 3),
    ("zeph", "Zephaniah", "صفنیاہ", "zephaniah.json", 3),
    ("hag", "Haggai", "حجّی", "haggai.json", 2),
    ("zech", "Zechariah", "زکریاہ", "zechariah.json", 14),
    ("mal", "Malachi", "ملاکی", "malachi.json", 4),
    # New Testament
    ("matt", "Matthew", "متّی", "matthew.json", 28),
    ("mark", "Mark", "مرقس", "mark.json", 16),
    ("luke", "Luke", "لُوقا", "luke.json", 24),
    ("john", "John", "یُوحنّا", "john.json", 21),
    ("acts", "Acts", "اعمال", "acts.json", 28),
    ("rom", "Romans", "رومیوں", "romans.json", 16),
    ("1cor", "1 Corinthians", "۱-کُرنتھیوں", "1corinthians.json", 16),
    ("2cor", "2 Corinthians", "۲-کُرنتھیوں", "2corinthians.json", 13),
    ("gal", "Galatians", "گلتیوں", "galatians.json", 6),
    ("eph", "Ephesians", "اِفسیوں", "ephesians.json", 6),
    ("phil", "Philippians", "فِلپّیوں", "philippians.json", 4),
    ("col", "Colossians", "کُلسّیوں", "colossians.json", 4),
    ("1thess", "1 Thessalonians", "۱-تھسّلُنیکیوں", "1thessalonians.json", 5),
    ("2thess", "2 Thessalonians", "۲-تھسّلُنیکیوں", "2thessalonians.json", 3),
    ("1tim", "1 Timothy", "۱-تیمُتھیُس", "1timothy.json", 6),
    ("2tim", "2 Timothy", "۲-تیمُتھیُس", "2timothy.json", 4),
    ("titus", "Titus", "طِطُس", "titus.json", 3),
    ("phlm", "Philemon", "فِلیمون", "philemon.json", 1),
    ("heb", "Hebrews", "عبرانیوں", "hebrews.json", 13),
    ("jas", "James", "یعقُوب", "james.json", 5),
    ("1pet", "1 Peter", "۱-پطرس", "1peter.json", 5),
    ("2pet", "2 Peter", "۲-پطرس", "2peter.json", 3),
    ("1john", "1 John", "۱-یُوحنّا", "1john.json", 5),
    ("2john", "2 John", "۲-یُوحنّا", "2john.json", 1),
    ("3john", "3 John", "۳-یُوحنّا", "3john.json", 1),
    ("jude", "Jude", "یہُوداہ", "jude.json", 1),
    ("rev", "Revelation", "مکاشفہ", "revelation.json", 22),
]


def fetch_book(slug):
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
            return resp.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print(f"  HTTP Error {e.code}: {url}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None


def parse_verses(html, num_chapters):
    """Parse all verses from HTML page"""
    chapters = {}

    # Auto-detect the book ID from HTML (e.g., GEN, EXOD, etc.)
    id_match = re.search(r'<span\s+id="([A-Z0-9]+)\.\d+\.\d+"', html)
    if not id_match:
        print("  Could not detect book ID")
        return None

    book_id = id_match.group(1)
    print(f"  Book ID: {book_id}")

    # Pattern: <span id="GEN.1.1"><span class="vn">1</span><span>verse text</span></span>
    pattern = re.compile(
        rf'<span\s+id="{book_id}\.(\d+)\.(\d+)"[^>]*>\s*'
        rf'<span\s+class="vn">(\d+)</span>\s*'
        rf'<span>([^<]+)</span>',
        re.IGNORECASE | re.DOTALL
    )

    for match in pattern.finditer(html):
        ch_num = int(match.group(1))
        verse_num = int(match.group(3))
        verse_text = match.group(4).strip()

        if ch_num not in chapters:
            chapters[ch_num] = []

        # Avoid duplicates
        if verse_text and not any(v["verse"] == verse_num for v in chapters[ch_num]):
            chapters[ch_num].append({
                "verse": verse_num,
                "text": verse_text
            })

    # Sort verses and build result
    result = []
    for ch_num in range(1, num_chapters + 1):
        if ch_num in chapters and chapters[ch_num]:
            chapters[ch_num].sort(key=lambda x: x["verse"])
            result.append({
                "chapter": ch_num,
                "verses": chapters[ch_num]
            })
        else:
            result.append({
                "chapter": ch_num,
                "verses": [{"verse": 1, "text": f"باب {ch_num}"}]
            })

    return result


def main():
    print("=" * 60)
    print("CPA Pakistan Urdu Bible Downloader")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_books = len(BOOKS)
    stats = {"complete": 0, "partial": 0, "failed": 0}
    total_verses = 0

    for idx, (slug, eng_name, urdu_name, file_name, num_chapters) in enumerate(BOOKS, 1):
        file_path = os.path.join(OUTPUT_DIR, file_name)
        print(f"\n[{idx}/{total_books}] {eng_name} - {num_chapters} chapters")

        # Fetch the book page
        html = fetch_book(slug)
        if not html:
            stats["failed"] += 1
            # Keep existing file if present
            continue

        print(f"  Downloaded {len(html):,} bytes")

        # Parse verses
        chapters = parse_verses(html, num_chapters)
        if not chapters:
            stats["failed"] += 1
            continue

        # Count real chapters
        real_chapters = 0
        book_verses = 0
        for ch in chapters:
            if len(ch["verses"]) > 1 or not ch["verses"][0]["text"].startswith("باب "):
                real_chapters += 1
                book_verses += len(ch["verses"])

        total_verses += book_verses

        # Save
        book_data = {
            "book": urdu_name,
            "bookEnglish": eng_name,
            "chapters": chapters
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(book_data, f, ensure_ascii=False, indent=2)

        if real_chapters == num_chapters:
            stats["complete"] += 1
            print(f"  COMPLETE: {real_chapters}/{num_chapters} chapters, {book_verses} verses")
        elif real_chapters > 0:
            stats["partial"] += 1
            print(f"  PARTIAL: {real_chapters}/{num_chapters} chapters, {book_verses} verses")
        else:
            stats["failed"] += 1
            print(f"  NO VERSES FOUND")

        time.sleep(1.5)  # Be polite to the server

    # Summary
    print("\n" + "=" * 60)
    print("DOWNLOAD COMPLETE")
    print(f"  Complete: {stats['complete']} books")
    print(f"  Partial:  {stats['partial']} books")
    print(f"  Failed:   {stats['failed']} books")
    print(f"  Total verses: {total_verses:,}")
    print("=" * 60)

    # Save summary
    summary = {
        "stats": stats,
        "total_verses": total_verses,
        "books": len(BOOKS)
    }
    with open(os.path.join(OUTPUT_DIR, "download_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()



