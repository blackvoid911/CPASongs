"""
Fetch complete Urdu Bible from CPA Pakistan website (https://cpa-pk.org/bible/)
Each book page contains ALL chapters on one page.
"""
import urllib.request
import json
import os
import re
import time
import ssl

# SSL context
ctx = ssl.create_default_context()

OUTPUT_DIR = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"

# Book mappings: (url_slug, book_id, english_name, urdu_name, file_name, chapters)
BOOKS = [
    ("gen", "GEN", "Genesis", "پیدائش", "genesis.json", 50),
    ("exod", "EXOD", "Exodus", "خُروج", "exodus.json", 40),
    ("lev", "LEV", "Leviticus", "احبار", "leviticus.json", 27),
    ("num", "NUM", "Numbers", "گنتی", "numbers.json", 36),
    ("deut", "DEUT", "Deuteronomy", "اِستِثنا", "deuteronomy.json", 34),
    ("josh", "JOSH", "Joshua", "یشُوع", "joshua.json", 24),
    ("judg", "JUDG", "Judges", "قُضاۃ", "judges.json", 21),
    ("ruth", "RUTH", "Ruth", "رُوت", "ruth.json", 4),
    ("1sam", "1SAM", "1 Samuel", "۱-سموئیل", "1samuel.json", 31),
    ("2sam", "2SAM", "2 Samuel", "۲-سموئیل", "2samuel.json", 24),
    ("1kgs", "1KGS", "1 Kings", "۱-سلاطین", "1kings.json", 22),
    ("2kgs", "2KGS", "2 Kings", "۲-سلاطین", "2kings.json", 25),
    ("1chr", "1CHR", "1 Chronicles", "۱-تواریخ", "1chronicles.json", 29),
    ("2chr", "2CHR", "2 Chronicles", "۲-تواریخ", "2chronicles.json", 36),
    ("ezra", "EZRA", "Ezra", "عزرا", "ezra.json", 10),
    ("neh", "NEH", "Nehemiah", "نحمیاہ", "nehemiah.json", 13),
    ("esth", "ESTH", "Esther", "آستر", "esther.json", 10),
    ("job", "JOB", "Job", "ایّوب", "job.json", 42),
    ("ps", "PS", "Psalms", "زبُور", "psalms.json", 150),
    ("prov", "PROV", "Proverbs", "امثال", "proverbs.json", 31),
    ("eccl", "ECCL", "Ecclesiastes", "واعظ", "ecclesiastes.json", 12),
    ("song", "SONG", "Song of Solomon", "غزل الغزلات", "songofsolomon.json", 8),
    ("isa", "ISA", "Isaiah", "یسعیاہ", "isaiah.json", 66),
    ("jer", "JER", "Jeremiah", "یرمیاہ", "jeremiah.json", 52),
    ("lam", "LAM", "Lamentations", "نوحہ", "lamentations.json", 5),
    ("ezek", "EZEK", "Ezekiel", "حزقی ایل", "ezekiel.json", 48),
    ("dan", "DAN", "Daniel", "دانی ایل", "daniel.json", 12),
    ("hos", "HOS", "Hosea", "ہوسیع", "hosea.json", 14),
    ("joel", "JOEL", "Joel", "یوایل", "joel.json", 3),
    ("amos", "AMOS", "Amos", "عاموس", "amos.json", 9),
    ("obad", "OBAD", "Obadiah", "عبدیاہ", "obadiah.json", 1),
    ("jonah", "JONAH", "Jonah", "یُوناہ", "jonah.json", 4),
    ("mic", "MIC", "Micah", "میکاہ", "micah.json", 7),
    ("nah", "NAH", "Nahum", "ناحُوم", "nahum.json", 3),
    ("hab", "HAB", "Habakkuk", "حبقُّوق", "habakkuk.json", 3),
    ("zeph", "ZEPH", "Zephaniah", "صفنیاہ", "zephaniah.json", 3),
    ("hag", "HAG", "Haggai", "حجّی", "haggai.json", 2),
    ("zech", "ZECH", "Zechariah", "زکریاہ", "zechariah.json", 14),
    ("mal", "MAL", "Malachi", "ملاکی", "malachi.json", 4),
    ("matt", "MATT", "Matthew", "متّی", "matthew.json", 28),
    ("mark", "MARK", "Mark", "مرقس", "mark.json", 16),
    ("luke", "LUKE", "Luke", "لُوقا", "luke.json", 24),
    ("john", "JOHN", "John", "یُوحنّا", "john.json", 21),
    ("acts", "ACTS", "Acts", "اعمال", "acts.json", 28),
    ("rom", "ROM", "Romans", "رومیوں", "romans.json", 16),
    ("1cor", "1COR", "1 Corinthians", "۱-کُرنتھیوں", "1corinthians.json", 16),
    ("2cor", "2COR", "2 Corinthians", "۲-کُرنتھیوں", "2corinthians.json", 13),
    ("gal", "GAL", "Galatians", "گلتیوں", "galatians.json", 6),
    ("eph", "EPH", "Ephesians", "اِفسیوں", "ephesians.json", 6),
    ("phil", "PHIL", "Philippians", "فِلپّیوں", "philippians.json", 4),
    ("col", "COL", "Colossians", "کُلسّیوں", "colossians.json", 4),
    ("1thess", "1THESS", "1 Thessalonians", "۱-تھسّلُنیکیوں", "1thessalonians.json", 5),
    ("2thess", "2THESS", "2 Thessalonians", "۲-تھسّلُنیکیوں", "2thessalonians.json", 3),
    ("1tim", "1TIM", "1 Timothy", "۱-تیمُتھیُس", "1timothy.json", 6),
    ("2tim", "2TIM", "2 Timothy", "۲-تیمُتھیُس", "2timothy.json", 4),
    ("titus", "TITUS", "Titus", "طِطُس", "titus.json", 3),
    ("phlm", "PHLM", "Philemon", "فِلیمون", "philemon.json", 1),
    ("heb", "HEB", "Hebrews", "عبرانیوں", "hebrews.json", 13),
    ("jas", "JAS", "James", "یعقُوب", "james.json", 5),
    ("1pet", "1PET", "1 Peter", "۱-پطرس", "1peter.json", 5),
    ("2pet", "2PET", "2 Peter", "۲-پطرس", "2peter.json", 3),
    ("1john", "1JOHN", "1 John", "۱-یُوحنّا", "1john.json", 5),
    ("2john", "2JOHN", "2 John", "۲-یُوحنّا", "2john.json", 1),
    ("3john", "3JOHN", "3 John", "۳-یُوحنّا", "3john.json", 1),
    ("jude", "JUDE", "Jude", "یہُوداہ", "jude.json", 1),
    ("rev", "REV", "Revelation", "مکاشفہ", "revelation.json", 22),
]


def fetch_book(book_slug):
    """Fetch entire book from CPA website (all chapters on one page)"""
    url = f"https://cpa-pk.org/bible/{book_slug}/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5,ur;q=0.3',
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
            return resp.read().decode('utf-8')
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None


def parse_book_html(html, book_id, num_chapters):
    """Parse all chapters and verses from HTML"""
    chapters = {}

    # First, detect the actual book ID from the HTML
    # Look for pattern like <div id="GEN.1"> or <span id="EXOD.1.1">
    id_match = re.search(r'<(?:div|span)\s+id="([A-Z0-9]+)\.\d+', html)
    if id_match:
        detected_id = id_match.group(1)
        print(f"  Detected book ID: {detected_id}")
        book_id = detected_id

    # Pattern to match verse spans:
    # <span id="GEN.1.1"><span class="vn">1</span><span>verse text</span></span>
    pattern = re.compile(
        rf'<span\s+id="{book_id}\.(\d+)\.(\d+)"[^>]*>\s*'
        rf'<span\s+class="vn">(\d+)</span>\s*'
        rf'<span>([^<]+)</span>',
        re.IGNORECASE | re.DOTALL
    )

    for match in pattern.finditer(html):
        chapter_num = int(match.group(1))
        verse_num = int(match.group(3))
        verse_text = match.group(4).strip()

        if chapter_num not in chapters:
            chapters[chapter_num] = []

        # Avoid duplicates
        existing = [v for v in chapters[chapter_num] if v["verse"] == verse_num]
        if not existing and verse_text:
            chapters[chapter_num].append({
                "verse": verse_num,
                "text": verse_text
            })

    # Sort verses within each chapter
    for ch in chapters:
        chapters[ch].sort(key=lambda x: x["verse"])

    # Build result list
    result = []
    for ch_num in range(1, num_chapters + 1):
        if ch_num in chapters and chapters[ch_num]:
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
    print("Fetching ALL chapters from each book page")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_books = len(BOOKS)
    stats = {"success": 0, "partial": 0, "failed": 0}
    total_verses = 0

    for idx, (slug, book_id, eng_name, urdu_name, file_name, num_chapters) in enumerate(BOOKS, 1):
        file_path = os.path.join(OUTPUT_DIR, file_name)
        print(f"\n[{idx}/{total_books}] {eng_name} ({urdu_name})")

        html = fetch_book(slug)

        if not html:
            print(f"  FAILED to fetch")
            stats["failed"] += 1
            continue

        print(f"  Got {len(html)} bytes, parsing...")

        chapters = parse_book_html(html, book_id, num_chapters)

        # Count real chapters (with actual verses)
        real_chapters = 0
        book_verses = 0
        for ch in chapters:
            verses = ch["verses"]
            if len(verses) > 1 or (len(verses) == 1 and not verses[0]["text"].startswith("باب ")):
                real_chapters += 1
                book_verses += len(verses)

        total_verses += book_verses

        # Save book
        book_data = {
            "book": urdu_name,
            "bookEnglish": eng_name,
            "chapters": chapters
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(book_data, f, ensure_ascii=False, indent=2)

        if real_chapters == num_chapters:
            stats["success"] += 1
            print(f"  COMPLETE: {real_chapters}/{num_chapters} chapters, {book_verses} verses")
        elif real_chapters > 0:
            stats["partial"] += 1
            print(f"  PARTIAL: {real_chapters}/{num_chapters} chapters, {book_verses} verses")
        else:
            stats["failed"] += 1
            print(f"  NO VERSES FOUND")

        time.sleep(1)  # Rate limiting

    print("\n" + "=" * 60)
    print("DOWNLOAD COMPLETE")
    print(f"  Complete: {stats['success']} books")
    print(f"  Partial:  {stats['partial']} books")
    print(f"  Failed:   {stats['failed']} books")
    print(f"  Total verses: {total_verses}")
    print("=" * 60)


if __name__ == "__main__":
    main()


