"""
Download complete Urdu Bible from GetBible.net API with robust handling.
This script downloads all chapters of all books in the Urdu Bible.
"""

import json
import os
import urllib.request
import time
import sys
import ssl

# Force unbuffered output
sys.stdout = sys.stderr = open(sys.stdout.fileno(), mode='w', buffering=1, encoding='utf-8')

# SSL context to bypass certificate issues if needed
ssl_context = ssl.create_default_context()

OUTPUT_DIR = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"

# Book mapping: (book_number, english_name, urdu_name, file_name, chapters)
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

def fetch_chapter(book_num, chapter, retries=3):
    """Fetch a chapter from getbible.net"""
    url = f"https://getbible.net/v2/urdu/{book_num}/{chapter}.json"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
    }

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60, context=ssl_context) as response:
                data = json.loads(response.read().decode('utf-8'))
                verses = []
                if 'verses' in data:
                    for v in data['verses']:
                        verse_num = v.get('verse', 1)
                        verse_text = v.get('text', '').strip()
                        if verse_text:
                            verses.append({
                                "verse": verse_num,
                                "text": verse_text
                            })
                return verses if verses else None
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"  404 for book {book_num} chapter {chapter}")
                return None
            print(f"  HTTP Error {e.code} (attempt {attempt + 1})")
            time.sleep(3)
        except Exception as e:
            print(f"  Error fetching {url}: {e} (attempt {attempt + 1})")
            time.sleep(3)
    return None


def load_existing_book(file_path):
    """Load existing book data if available"""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return None


def count_real_verses(chapters):
    """Count chapters that have real verses (not just placeholders)"""
    count = 0
    for ch in chapters:
        verses = ch.get('verses', [])
        if len(verses) > 1 or (len(verses) == 1 and not verses[0].get('text', '').startswith('باب ')):
            count += 1
    return count


def main():
    print("=" * 60)
    print("Urdu Bible Downloader - GetBible.net API")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_books = len(BOOKS)
    stats = {"success": 0, "partial": 0, "failed": 0}

    # Track progress
    progress_file = os.path.join(OUTPUT_DIR, "download_progress.json")

    for idx, (book_num, eng_name, urdu_name, file_name, num_chapters) in enumerate(BOOKS, 1):
        file_path = os.path.join(OUTPUT_DIR, file_name)

        print(f"\n[{idx}/{total_books}] {eng_name} ({urdu_name}) - {num_chapters} chapters")

        # Check existing data
        existing = load_existing_book(file_path)
        if existing:
            existing_chapters = existing.get('chapters', [])
            real_count = count_real_verses(existing_chapters)
            if real_count == num_chapters:
                print(f"  Already complete ({real_count}/{num_chapters} chapters)")
                stats["success"] += 1
                continue
            else:
                print(f"  Existing has {real_count}/{num_chapters} real chapters, will try to fetch missing")

        chapters = []
        success_count = 0

        for ch in range(1, num_chapters + 1):
            # Check if already have this chapter with real verses
            if existing:
                for ech in existing.get('chapters', []):
                    if ech.get('chapter') == ch:
                        verses = ech.get('verses', [])
                        if len(verses) > 1 or (len(verses) == 1 and not verses[0].get('text', '').startswith('باب ')):
                            chapters.append(ech)
                            success_count += 1
                            print(f"  Chapter {ch}: using existing ({len(verses)} verses)")
                            continue

            # Fetch from API
            verses = fetch_chapter(book_num, ch)

            if verses and len(verses) > 0:
                chapters.append({
                    "chapter": ch,
                    "verses": verses
                })
                success_count += 1
                print(f"  Chapter {ch}: {len(verses)} verses")
            else:
                # Use placeholder
                chapters.append({
                    "chapter": ch,
                    "verses": [{"verse": 1, "text": f"باب {ch}"}]
                })
                print(f"  Chapter {ch}: placeholder")

            time.sleep(0.5)  # Rate limiting

        # Sort chapters
        chapters.sort(key=lambda x: x.get('chapter', 0))

        # Save book
        book_data = {
            "book": urdu_name,
            "bookEnglish": eng_name,
            "chapters": chapters
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(book_data, f, ensure_ascii=False, indent=2)

        if success_count == num_chapters:
            stats["success"] += 1
            print(f"  COMPLETE: {success_count}/{num_chapters} chapters")
        elif success_count > 0:
            stats["partial"] += 1
            print(f"  PARTIAL: {success_count}/{num_chapters} chapters")
        else:
            stats["failed"] += 1
            print(f"  FAILED: no chapters fetched")

        time.sleep(1)  # Rate limiting between books

    print("\n" + "=" * 60)
    print("DOWNLOAD COMPLETE")
    print(f"  Complete: {stats['success']} books")
    print(f"  Partial:  {stats['partial']} books")
    print(f"  Failed:   {stats['failed']} books")
    print("=" * 60)


if __name__ == "__main__":
    main()

