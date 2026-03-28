"""
Fetch complete Urdu Bible from various APIs.
This script will try multiple sources.
"""

import json
import os
import urllib.request
import time
import sys

# Urdu Bible books mapping
BOOKS = [
    (1, "Genesis", "genesis.json", 50),
    (2, "Exodus", "exodus.json", 40),
    (3, "Leviticus", "leviticus.json", 27),
    (4, "Numbers", "numbers.json", 36),
    (5, "Deuteronomy", "deuteronomy.json", 34),
    (6, "Joshua", "joshua.json", 24),
    (7, "Judges", "judges.json", 21),
    (8, "Ruth", "ruth.json", 4),
    (9, "1 Samuel", "1samuel.json", 31),
    (10, "2 Samuel", "2samuel.json", 24),
    (11, "1 Kings", "1kings.json", 22),
    (12, "2 Kings", "2kings.json", 25),
    (13, "1 Chronicles", "1chronicles.json", 29),
    (14, "2 Chronicles", "2chronicles.json", 36),
    (15, "Ezra", "ezra.json", 10),
    (16, "Nehemiah", "nehemiah.json", 13),
    (17, "Esther", "esther.json", 10),
    (18, "Job", "job.json", 42),
    (19, "Psalms", "psalms.json", 150),
    (20, "Proverbs", "proverbs.json", 31),
    (21, "Ecclesiastes", "ecclesiastes.json", 12),
    (22, "Song of Solomon", "songofsolomon.json", 8),
    (23, "Isaiah", "isaiah.json", 66),
    (24, "Jeremiah", "jeremiah.json", 52),
    (25, "Lamentations", "lamentations.json", 5),
    (26, "Ezekiel", "ezekiel.json", 48),
    (27, "Daniel", "daniel.json", 12),
    (28, "Hosea", "hosea.json", 14),
    (29, "Joel", "joel.json", 3),
    (30, "Amos", "amos.json", 9),
    (31, "Obadiah", "obadiah.json", 1),
    (32, "Jonah", "jonah.json", 4),
    (33, "Micah", "micah.json", 7),
    (34, "Nahum", "nahum.json", 3),
    (35, "Habakkuk", "habakkuk.json", 3),
    (36, "Zephaniah", "zephaniah.json", 3),
    (37, "Haggai", "haggai.json", 2),
    (38, "Zechariah", "zechariah.json", 14),
    (39, "Malachi", "malachi.json", 4),
    (40, "Matthew", "matthew.json", 28),
    (41, "Mark", "mark.json", 16),
    (42, "Luke", "luke.json", 24),
    (43, "John", "john.json", 21),
    (44, "Acts", "acts.json", 28),
    (45, "Romans", "romans.json", 16),
    (46, "1 Corinthians", "1corinthians.json", 16),
    (47, "2 Corinthians", "2corinthians.json", 13),
    (48, "Galatians", "galatians.json", 6),
    (49, "Ephesians", "ephesians.json", 6),
    (50, "Philippians", "philippians.json", 4),
    (51, "Colossians", "colossians.json", 4),
    (52, "1 Thessalonians", "1thessalonians.json", 5),
    (53, "2 Thessalonians", "2thessalonians.json", 3),
    (54, "1 Timothy", "1timothy.json", 6),
    (55, "2 Timothy", "2timothy.json", 4),
    (56, "Titus", "titus.json", 3),
    (57, "Philemon", "philemon.json", 1),
    (58, "Hebrews", "hebrews.json", 13),
    (59, "James", "james.json", 5),
    (60, "1 Peter", "1peter.json", 5),
    (61, "2 Peter", "2peter.json", 3),
    (62, "1 John", "1john.json", 5),
    (63, "2 John", "2john.json", 1),
    (64, "3 John", "3john.json", 1),
    (65, "Jude", "jude.json", 1),
    (66, "Revelation", "revelation.json", 22),
]

# Urdu book names
URDU_NAMES = {
    "Genesis": "پیدائش", "Exodus": "خُروج", "Leviticus": "احبار",
    "Numbers": "گنتی", "Deuteronomy": "اِستِثنا", "Joshua": "یشُوع",
    "Judges": "قُضاۃ", "Ruth": "رُوت", "1 Samuel": "۱-سموئیل",
    "2 Samuel": "۲-سموئیل", "1 Kings": "۱-سلاطین", "2 Kings": "۲-سلاطین",
    "1 Chronicles": "۱-تواریخ", "2 Chronicles": "۲-تواریخ", "Ezra": "عزرا",
    "Nehemiah": "نحمیاہ", "Esther": "آستر", "Job": "ایّوب",
    "Psalms": "زبُور", "Proverbs": "امثال", "Ecclesiastes": "واعظ",
    "Song of Solomon": "غزل الغزلات", "Isaiah": "یسعیاہ", "Jeremiah": "یرمیاہ",
    "Lamentations": "نوحہ", "Ezekiel": "حزقی ایل", "Daniel": "دانی ایل",
    "Hosea": "ہوسیع", "Joel": "یوایل", "Amos": "عاموس", "Obadiah": "عبدیاہ",
    "Jonah": "یُوناہ", "Micah": "میکاہ", "Nahum": "ناحُوم",
    "Habakkuk": "حبقُّوق", "Zephaniah": "صفنیاہ", "Haggai": "حجّی",
    "Zechariah": "زکریاہ", "Malachi": "ملاکی", "Matthew": "متّی",
    "Mark": "مرقس", "Luke": "لُوقا", "John": "یُوحنّا", "Acts": "اعمال",
    "Romans": "رومیوں", "1 Corinthians": "۱-کُرنتھیوں",
    "2 Corinthians": "۲-کُرنتھیوں", "Galatians": "گلتیوں",
    "Ephesians": "اِفسیوں", "Philippians": "فِلپّیوں",
    "Colossians": "کُلسّیوں", "1 Thessalonians": "۱-تھسّلُنیکیوں",
    "2 Thessalonians": "۲-تھسّلُنیکیوں", "1 Timothy": "۱-تیمُتھیُس",
    "2 Timothy": "۲-تیمُتھیُس", "Titus": "طِطُس", "Philemon": "فِلیمون",
    "Hebrews": "عبرانیوں", "James": "یعقُوب", "1 Peter": "۱-پطرس",
    "2 Peter": "۲-پطرس", "1 John": "۱-یُوحنّا", "2 John": "۲-یُوحنّا",
    "3 John": "۳-یُوحنّا", "Jude": "یہُوداہ", "Revelation": "مکاشفہ",
}


def fetch_from_bible_api(book_name, chapter, retries=3):
    """Try to fetch from bible-api.com with various translation codes"""
    # Try different Urdu translation codes
    translations = ['urv']  # Urdu Roman Version

    for trans in translations:
        api_name = book_name.replace(" ", "+")
        url = f"https://bible-api.com/{api_name}+{chapter}?translation={trans}"

        for attempt in range(retries):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    if 'verses' in data and len(data['verses']) > 0:
                        verses = []
                        for v in data['verses']:
                            verses.append({
                                "verse": v['verse'],
                                "text": v['text'].strip()
                            })
                        return verses
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    time.sleep(10)
                    continue
                elif e.code == 404:
                    break  # Translation not found
            except:
                time.sleep(2)

    return None


def main():
    output_dir = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"

    print("Starting Urdu Bible fetch...")
    print("This may take a while due to API rate limiting.")
    sys.stdout.flush()

    for book_num, eng_name, file_name, num_chapters in BOOKS:
        file_path = os.path.join(output_dir, file_name)
        urdu_name = URDU_NAMES.get(eng_name, eng_name)

        print(f"\nProcessing {eng_name} ({urdu_name})...")
        sys.stdout.flush()

        chapters = []

        for ch in range(1, num_chapters + 1):
            # Try to fetch from API
            verses = fetch_from_bible_api(eng_name, ch)

            if verses and len(verses) > 0:
                chapters.append({
                    "chapter": ch,
                    "verses": verses
                })
                print(f"  Ch {ch}: {len(verses)} verses", end=" ")
                sys.stdout.flush()
            else:
                # Use placeholder
                chapters.append({
                    "chapter": ch,
                    "verses": [{"verse": 1, "text": f"باب {ch}"}]
                })
                print(f"  Ch {ch}: placeholder", end=" ")
                sys.stdout.flush()

            # Rate limiting
            time.sleep(2)

        # Save book
        book_data = {
            "book": urdu_name,
            "bookEnglish": eng_name,
            "chapters": chapters
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(book_data, f, ensure_ascii=False, indent=2)

        total_verses = sum(len(ch["verses"]) for ch in chapters)
        print(f"\n  -> Saved: {total_verses} verses")
        sys.stdout.flush()

        time.sleep(3)


if __name__ == "__main__":
    main()

