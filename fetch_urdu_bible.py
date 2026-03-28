"""
Download complete Urdu Bible from getbible.net API.
"""

import json
import os
import urllib.request
import time

def fetch_chapter(book_num, chapter, retries=3):
    """Fetch a chapter from getbible.net"""
    url = f"https://getbible.net/v2/urdu/{book_num}/{chapter}.json"

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                verses = []
                if 'verses' in data:
                    for v in data['verses']:
                        verses.append({
                            "verse": v.get('verse', 1),
                            "text": v.get('text', '').strip()
                        })
                return verses
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2)
        except Exception as e:
            time.sleep(2)
    return None

def main():
    output_dir = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"

    # Book mapping: book_number -> (english_name, urdu_name, file_name, chapters)
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

    for book_num, eng_name, urdu_name, file_name, num_chapters in BOOKS:
        file_path = os.path.join(output_dir, file_name)

        print(f"Fetching {eng_name} ({urdu_name})...")

        chapters = []
        success_count = 0

        for ch in range(1, num_chapters + 1):
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

        # Save book
        book_data = {
            "book": urdu_name,
            "bookEnglish": eng_name,
            "chapters": chapters
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(book_data, f, ensure_ascii=False, indent=2)

        print(f"  Saved {eng_name}: {success_count}/{num_chapters} chapters with verses")
        time.sleep(1)

if __name__ == "__main__":
    main()

