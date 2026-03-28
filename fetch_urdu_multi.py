"""
Fetch Urdu Bible from multiple sources.
Tries getbible.net and bible.com APIs.
"""

import json
import os
import urllib.request
import urllib.parse
import time
import ssl

# Output settings
OUTPUT_DIR = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"
LOG_FILE = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\fetch_log.txt"

# SSL context
ctx = ssl.create_default_context()

# All 66 books with their info
BOOKS = [
    (1, "Genesis", "پیدائش", "genesis.json", 50),
    (2, "Exodus", "خُروج", "exodus.json", 40),
    (3, "Leviticus", "احبار", "leviticus.json", 27),
    (4, "Numbers", "گنتی", "numbers.json", 36),
    (5, "Deuteronomy", "اِستِثنا", "deuteronomy.json", 34),
    (6, "Joshua", "یشُوع", "joshua.json", 24),
    (7, "Judges", "قُضاۃ", "judges.json", 21),
    (8, "Ruth", "رُوت", "ruth.json", 4),
    (9, "1 Samuel", "۱-سموئیل", "1samuel.json", 31),
    (10, "2 Samuel", "۲-سموئیل", "2samuel.json", 24),
    (11, "1 Kings", "۱-سلاطین", "1kings.json", 22),
    (12, "2 Kings", "۲-سلاطین", "2kings.json", 25),
    (13, "1 Chronicles", "۱-تواریخ", "1chronicles.json", 29),
    (14, "2 Chronicles", "۲-تواریخ", "2chronicles.json", 36),
    (15, "Ezra", "عزرا", "ezra.json", 10),
    (16, "Nehemiah", "نحمیاہ", "nehemiah.json", 13),
    (17, "Esther", "آستر", "esther.json", 10),
    (18, "Job", "ایّوب", "job.json", 42),
    (19, "Psalms", "زبُور", "psalms.json", 150),
    (20, "Proverbs", "امثال", "proverbs.json", 31),
    (21, "Ecclesiastes", "واعظ", "ecclesiastes.json", 12),
    (22, "Song of Solomon", "غزل الغزلات", "songofsolomon.json", 8),
    (23, "Isaiah", "یسعیاہ", "isaiah.json", 66),
    (24, "Jeremiah", "یرمیاہ", "jeremiah.json", 52),
    (25, "Lamentations", "نوحہ", "lamentations.json", 5),
    (26, "Ezekiel", "حزقی ایل", "ezekiel.json", 48),
    (27, "Daniel", "دانی ایل", "daniel.json", 12),
    (28, "Hosea", "ہوسیع", "hosea.json", 14),
    (29, "Joel", "یوایل", "joel.json", 3),
    (30, "Amos", "عاموس", "amos.json", 9),
    (31, "Obadiah", "عبدیاہ", "obadiah.json", 1),
    (32, "Jonah", "یُوناہ", "jonah.json", 4),
    (33, "Micah", "میکاہ", "micah.json", 7),
    (34, "Nahum", "ناحُوم", "nahum.json", 3),
    (35, "Habakkuk", "حبقُّوق", "habakkuk.json", 3),
    (36, "Zephaniah", "صفنیاہ", "zephaniah.json", 3),
    (37, "Haggai", "حجّی", "haggai.json", 2),
    (38, "Zechariah", "زکریاہ", "zechariah.json", 14),
    (39, "Malachi", "ملاکی", "malachi.json", 4),
    (40, "Matthew", "متّی", "matthew.json", 28),
    (41, "Mark", "مرقس", "mark.json", 16),
    (42, "Luke", "لُوقا", "luke.json", 24),
    (43, "John", "یُوحنّا", "john.json", 21),
    (44, "Acts", "اعمال", "acts.json", 28),
    (45, "Romans", "رومیوں", "romans.json", 16),
    (46, "1 Corinthians", "۱-کُرنتھیوں", "1corinthians.json", 16),
    (47, "2 Corinthians", "۲-کُرنتھیوں", "2corinthians.json", 13),
    (48, "Galatians", "گلتیوں", "galatians.json", 6),
    (49, "Ephesians", "اِفسیوں", "ephesians.json", 6),
    (50, "Philippians", "فِلپّیوں", "philippians.json", 4),
    (51, "Colossians", "کُلسّیوں", "colossians.json", 4),
    (52, "1 Thessalonians", "۱-تھسّلُنیکیوں", "1thessalonians.json", 5),
    (53, "2 Thessalonians", "۲-تھسّلُنیکیوں", "2thessalonians.json", 3),
    (54, "1 Timothy", "۱-تیمُتھیُس", "1timothy.json", 6),
    (55, "2 Timothy", "۲-تیمُتھیُس", "2timothy.json", 4),
    (56, "Titus", "طِطُس", "titus.json", 3),
    (57, "Philemon", "فِلیمون", "philemon.json", 1),
    (58, "Hebrews", "عبرانیوں", "hebrews.json", 13),
    (59, "James", "یعقُوب", "james.json", 5),
    (60, "1 Peter", "۱-پطرس", "1peter.json", 5),
    (61, "2 Peter", "۲-پطرس", "2peter.json", 3),
    (62, "1 John", "۱-یُوحنّا", "1john.json", 5),
    (63, "2 John", "۲-یُوحنّا", "2john.json", 1),
    (64, "3 John", "۳-یُوحنّا", "3john.json", 1),
    (65, "Jude", "یہُوداہ", "jude.json", 1),
    (66, "Revelation", "مکاشفہ", "revelation.json", 22),
]

def log(msg):
    """Log message to console and file"""
    print(msg, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def fetch_getbible(book_num, chapter):
    """Fetch from getbible.net API"""
    url = f"https://getbible.net/v2/urdu/{book_num}/{chapter}.json"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            verses = []
            for v in data.get('verses', []):
                text = v.get('text', '').strip()
                if text:
                    verses.append({"verse": v.get('verse', 1), "text": text})
            return verses if verses else None
    except:
        return None

def fetch_bolls(book_abbr, chapter):
    """Fetch from bolls.life API (Urdu Geo Version)"""
    # Book abbreviations for bolls.life
    url = f"https://bolls.life/get-chapter/UGV/{book_abbr}/{chapter}/"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            verses = []
            for v in data:
                text = v.get('text', '').strip()
                if text:
                    verses.append({"verse": v.get('verse', 1), "text": text})
            return verses if verses else None
    except:
        return None

def load_existing(file_path):
    """Load existing book data"""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return None

def has_real_verses(chapter_data):
    """Check if chapter has real verses (not placeholder)"""
    verses = chapter_data.get('verses', [])
    if len(verses) > 1:
        return True
    if len(verses) == 1:
        text = verses[0].get('text', '')
        return not text.startswith('باب ')
    return False

def main():
    # Clear log file
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("Urdu Bible Download Log\n")
        f.write("=" * 60 + "\n\n")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_books = len(BOOKS)
    stats = {"complete": 0, "partial": 0, "failed": 0, "skipped": 0}

    for idx, (book_num, eng_name, urdu_name, file_name, num_chapters) in enumerate(BOOKS, 1):
        file_path = os.path.join(OUTPUT_DIR, file_name)
        log(f"\n[{idx}/{total_books}] {eng_name} ({urdu_name})")

        # Load existing data
        existing = load_existing(file_path)
        existing_chapters = {}
        if existing:
            for ch in existing.get('chapters', []):
                if has_real_verses(ch):
                    existing_chapters[ch['chapter']] = ch

        # Check if already complete
        if len(existing_chapters) == num_chapters:
            log(f"  Already complete ({num_chapters} chapters)")
            stats["skipped"] += 1
            continue

        log(f"  Have {len(existing_chapters)}/{num_chapters} chapters, fetching rest...")

        chapters = []
        success = 0

        for ch in range(1, num_chapters + 1):
            # Use existing if available
            if ch in existing_chapters:
                chapters.append(existing_chapters[ch])
                success += 1
                continue

            # Try getbible.net first
            verses = fetch_getbible(book_num, ch)

            if verses:
                chapters.append({"chapter": ch, "verses": verses})
                success += 1
                log(f"  Ch {ch}: {len(verses)} verses (getbible)")
            else:
                # Placeholder
                chapters.append({
                    "chapter": ch,
                    "verses": [{"verse": 1, "text": f"باب {ch}"}]
                })
                log(f"  Ch {ch}: placeholder")

            time.sleep(0.3)

        # Sort and save
        chapters.sort(key=lambda x: x['chapter'])
        book_data = {
            "book": urdu_name,
            "bookEnglish": eng_name,
            "chapters": chapters
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(book_data, f, ensure_ascii=False, indent=2)

        if success == num_chapters:
            stats["complete"] += 1
            log(f"  COMPLETE: {success}/{num_chapters}")
        elif success > 0:
            stats["partial"] += 1
            log(f"  PARTIAL: {success}/{num_chapters}")
        else:
            stats["failed"] += 1
            log(f"  FAILED")

        time.sleep(0.5)

    log("\n" + "=" * 60)
    log("DOWNLOAD COMPLETE")
    log(f"  Skipped (already complete): {stats['skipped']}")
    log(f"  Complete: {stats['complete']}")
    log(f"  Partial: {stats['partial']}")
    log(f"  Failed: {stats['failed']}")
    log("=" * 60)

if __name__ == "__main__":
    main()

