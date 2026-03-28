"""
Process complete Urdu Bible from cache directory.
Reads all HTML files and generates JSON files for all 66 books.
"""
import re, json, os
from bs4 import BeautifulSoup

CACHE_DIR = r"C:\xampp\htdocs\cpa\cache\bible"
URDU_DIR  = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"

# Ensure output directory exists
os.makedirs(URDU_DIR, exist_ok=True)

# Complete Bible book mapping with abbreviations, names, and chapter counts
BIBLE_BOOKS = [
    # Old Testament
    ("gen", "پیدائش", "Genesis", 50),
    ("exo", "خُروج", "Exodus", 40),
    ("lev", "احبار", "Leviticus", 27),
    ("num", "گنتی", "Numbers", 36),
    ("deu", "اِستِثنا", "Deuteronomy", 34),
    ("jos", "یشُوع", "Joshua", 24),
    ("jdg", "قُضاۃ", "Judges", 21),
    ("rut", "رُوت", "Ruth", 4),
    ("1sa", "۱-سموئیل", "1 Samuel", 31),
    ("2sa", "۲-سموئیل", "2 Samuel", 24),
    ("1ki", "۱-سلاطین", "1 Kings", 22),
    ("2ki", "۲-سلاطین", "2 Kings", 25),
    ("1ch", "۱-تواریخ", "1 Chronicles", 29),
    ("2ch", "۲-تواریخ", "2 Chronicles", 36),
    ("ezr", "عزرا", "Ezra", 10),
    ("neh", "نحمیاہ", "Nehemiah", 13),
    ("est", "آستر", "Esther", 10),
    ("job", "ایّوب", "Job", 42),
    ("psa", "زبُور", "Psalms", 150),
    ("pro", "امثال", "Proverbs", 31),
    ("ecc", "واعظ", "Ecclesiastes", 12),
    ("sng", "غزل الغزلات", "Song of Solomon", 8),
    ("isa", "یسعیاہ", "Isaiah", 66),
    ("jer", "یرمیاہ", "Jeremiah", 52),
    ("lam", "نوحہ", "Lamentations", 5),
    ("ezk", "حزقی ایل", "Ezekiel", 48),
    ("dan", "دانی ایل", "Daniel", 12),
    ("hos", "ہوسیع", "Hosea", 14),
    ("jol", "یوایل", "Joel", 3),
    ("amo", "عاموس", "Amos", 9),
    ("oba", "عبدیاہ", "Obadiah", 1),
    ("jon", "یُوناہ", "Jonah", 4),
    ("mic", "میکاہ", "Micah", 7),
    ("nam", "ناحُوم", "Nahum", 3),
    ("hab", "حبقُّوق", "Habakkuk", 3),
    ("zep", "صفنیاہ", "Zephaniah", 3),
    ("hag", "حجّی", "Haggai", 2),
    ("zec", "زکریاہ", "Zechariah", 14),
    ("mal", "ملاکی", "Malachi", 4),
    # New Testament
    ("mat", "متّی", "Matthew", 28),
    ("mrk", "مرقُس", "Mark", 16),
    ("luk", "لُوقا", "Luke", 24),
    ("jhn", "یُوحنّا", "John", 21),
    ("act", "اعمال", "Acts", 28),
    ("rom", "رومیوں", "Romans", 16),
    ("1co", "۱-کرنتھیوں", "1 Corinthians", 16),
    ("2co", "۲-کرنتھیوں", "2 Corinthians", 13),
    ("gal", "گلتیوں", "Galatians", 6),
    ("eph", "افسیوں", "Ephesians", 6),
    ("php", "فلپیوں", "Philippians", 4),
    ("col", "کلسیوں", "Colossians", 4),
    ("1th", "۱-تھسلنیکیوں", "1 Thessalonians", 5),
    ("2th", "۲-تھسلنیکیوں", "2 Thessalonians", 3),
    ("1ti", "۱-تیمتھیس", "1 Timothy", 6),
    ("2ti", "۲-تیمتھیس", "2 Timothy", 4),
    ("tit", "ططس", "Titus", 3),
    ("phm", "فلیمون", "Philemon", 1),
    ("heb", "عبرانیوں", "Hebrews", 13),
    ("jas", "یعقوب", "James", 5),
    ("1pe", "۱-پطرس", "1 Peter", 5),
    ("2pe", "۲-پطرس", "2 Peter", 3),
    ("1jn", "۱-یُوحنّا", "1 John", 5),
    ("2jn", "۲-یُوحنّا", "2 John", 1),
    ("3jn", "۳-یُوحنّا", "3 John", 1),
    ("jud", "یہُوداہ", "Jude", 1),
    ("rev", "مکاشفہ", "Revelation", 22),
]

def is_urdu(text):
    """Check if text contains Urdu characters"""
    return any('\u0600' <= c <= '\u06ff' for c in text)

def process_book(abbr, urdu_name, english_name, expected_chapters):
    """Process a single Bible book from HTML cache"""
    html_path = os.path.join(CACHE_DIR, f"{abbr}.html")

    if not os.path.exists(html_path):
        print(f"❌ {english_name}: HTML file not found")
        return False

    try:
        with open(html_path, encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        chapters = {}
        verse_pattern = re.compile(rf"^{abbr.upper()}\.\d+\.\d+$", re.IGNORECASE)

        # Find all verse spans
        for span in soup.find_all("span", id=verse_pattern):
            verse_id = span.get("id", "")
            parts = verse_id.upper().split(".")

            if len(parts) != 3:
                continue

            try:
                ch, vn = int(parts[1]), int(parts[2])
            except ValueError:
                continue

            # Extract text - try nested span first, then direct text
            inner = span.find("span", class_=False)
            if inner:
                text = inner.get_text(strip=True)
            else:
                text = span.get_text(separator=" ", strip=True)
                # Remove leading verse number if present
                text = re.sub(r"^\d+\s*", "", text).strip()

            # Skip empty or non-Urdu text
            if not text or not is_urdu(text):
                continue

            # Store verse (only if not already present)
            chapters.setdefault(ch, {})
            if vn not in chapters[ch]:
                chapters[ch][vn] = text

        # Calculate statistics
        total_verses = sum(len(v) for v in chapters.values())
        ch_count = len(chapters)

        if total_verses == 0:
            print(f"❌ {english_name}: No Urdu verses found")
            return False

        # Build JSON structure
        result = {
            "book": urdu_name,
            "bookEnglish": english_name,
            "chapters": []
        }

        for ch_num in sorted(chapters.keys()):
            verses = [
                {"verse": v, "text": t}
                for v, t in sorted(chapters[ch_num].items())
            ]
            result["chapters"].append({
                "chapter": ch_num,
                "verses": verses
            })

        # Determine output filename
        filename = english_name.lower().replace(" ", "").replace("-", "") + ".json"
        output_path = os.path.join(URDU_DIR, filename)

        # Write JSON file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # Report status
        status = "✓" if ch_count == expected_chapters else f"⚠ ({ch_count}/{expected_chapters} ch)"
        print(f"{status} {english_name:25s} {ch_count:3d} chapters, {total_verses:4d} verses")

        return True

    except Exception as e:
        print(f"❌ {english_name}: ERROR - {e}")
        return False

def main():
    print("Processing Complete Urdu Bible from Cache")
    print("=" * 60)

    success_count = 0
    fail_count = 0

    for abbr, urdu_name, english_name, expected_ch in BIBLE_BOOKS:
        if process_book(abbr, urdu_name, english_name, expected_ch):
            success_count += 1
        else:
            fail_count += 1

    print("=" * 60)
    print(f"Completed: {success_count} books successfully processed")
    if fail_count > 0:
        print(f"Failed: {fail_count} books had errors")

    print(f"\nOutput directory: {URDU_DIR}")

if __name__ == "__main__":
    main()

