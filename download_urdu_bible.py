"""
Download complete Urdu Bible from public domain sources.
"""

import json
import os
import urllib.request
import time

def download_urdu_bible():
    """Download Urdu Bible from public domain sources"""

    # Try different Urdu Bible sources
    urls = [
        "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/json/t_urdu.json",
        "https://raw.githubusercontent.com/prabhu/Bible-Data/master/urdu.json",
    ]

    for url in urls:
        try:
            print(f"Trying {url}...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=120) as response:
                data = response.read().decode('utf-8-sig')
                print(f"Downloaded {len(data)} bytes")
                return json.loads(data)
        except Exception as e:
            print(f"Failed: {e}")
            time.sleep(2)

    return None

def main():
    print("Downloading Urdu Bible...")
    bible_data = download_urdu_bible()

    if not bible_data:
        print("Failed to download Urdu Bible data")
        return

    print(f"Downloaded Bible with {len(bible_data)} books")

    # Process and save
    output_dir = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"

    # Map of Bible book names to file names and Urdu names
    FILE_MAP = {
        "Genesis": {"file": "genesis.json", "urdu": "پیدائش"},
        "Exodus": {"file": "exodus.json", "urdu": "خُروج"},
        "Leviticus": {"file": "leviticus.json", "urdu": "احبار"},
        "Numbers": {"file": "numbers.json", "urdu": "گنتی"},
        "Deuteronomy": {"file": "deuteronomy.json", "urdu": "اِستِثنا"},
        "Joshua": {"file": "joshua.json", "urdu": "یشُوع"},
        "Judges": {"file": "judges.json", "urdu": "قُضاۃ"},
        "Ruth": {"file": "ruth.json", "urdu": "رُوت"},
        "1 Samuel": {"file": "1samuel.json", "urdu": "۱-سموئیل"},
        "2 Samuel": {"file": "2samuel.json", "urdu": "۲-سموئیل"},
        "1 Kings": {"file": "1kings.json", "urdu": "۱-سلاطین"},
        "2 Kings": {"file": "2kings.json", "urdu": "۲-سلاطین"},
        "1 Chronicles": {"file": "1chronicles.json", "urdu": "۱-تواریخ"},
        "2 Chronicles": {"file": "2chronicles.json", "urdu": "۲-تواریخ"},
        "Ezra": {"file": "ezra.json", "urdu": "عزرا"},
        "Nehemiah": {"file": "nehemiah.json", "urdu": "نحمیاہ"},
        "Esther": {"file": "esther.json", "urdu": "آستر"},
        "Job": {"file": "job.json", "urdu": "ایّوب"},
        "Psalms": {"file": "psalms.json", "urdu": "زبُور"},
        "Proverbs": {"file": "proverbs.json", "urdu": "امثال"},
        "Ecclesiastes": {"file": "ecclesiastes.json", "urdu": "واعظ"},
        "Song of Solomon": {"file": "songofsolomon.json", "urdu": "غزل الغزلات"},
        "Isaiah": {"file": "isaiah.json", "urdu": "یسعیاہ"},
        "Jeremiah": {"file": "jeremiah.json", "urdu": "یرمیاہ"},
        "Lamentations": {"file": "lamentations.json", "urdu": "نوحہ"},
        "Ezekiel": {"file": "ezekiel.json", "urdu": "حزقی ایل"},
        "Daniel": {"file": "daniel.json", "urdu": "دانی ایل"},
        "Hosea": {"file": "hosea.json", "urdu": "ہوسیع"},
        "Joel": {"file": "joel.json", "urdu": "یوایل"},
        "Amos": {"file": "amos.json", "urdu": "عاموس"},
        "Obadiah": {"file": "obadiah.json", "urdu": "عبدیاہ"},
        "Jonah": {"file": "jonah.json", "urdu": "یُوناہ"},
        "Micah": {"file": "micah.json", "urdu": "میکاہ"},
        "Nahum": {"file": "nahum.json", "urdu": "ناحُوم"},
        "Habakkuk": {"file": "habakkuk.json", "urdu": "حبقُّوق"},
        "Zephaniah": {"file": "zephaniah.json", "urdu": "صفنیاہ"},
        "Haggai": {"file": "haggai.json", "urdu": "حجّی"},
        "Zechariah": {"file": "zechariah.json", "urdu": "زکریاہ"},
        "Malachi": {"file": "malachi.json", "urdu": "ملاکی"},
        "Matthew": {"file": "matthew.json", "urdu": "متّی"},
        "Mark": {"file": "mark.json", "urdu": "مرقس"},
        "Luke": {"file": "luke.json", "urdu": "لُوقا"},
        "John": {"file": "john.json", "urdu": "یُوحنّا"},
        "Acts": {"file": "acts.json", "urdu": "اعمال"},
        "Romans": {"file": "romans.json", "urdu": "رومیوں"},
        "1 Corinthians": {"file": "1corinthians.json", "urdu": "۱-کُرنتھیوں"},
        "2 Corinthians": {"file": "2corinthians.json", "urdu": "۲-کُرنتھیوں"},
        "Galatians": {"file": "galatians.json", "urdu": "گلتیوں"},
        "Ephesians": {"file": "ephesians.json", "urdu": "اِفسیوں"},
        "Philippians": {"file": "philippians.json", "urdu": "فِلپّیوں"},
        "Colossians": {"file": "colossians.json", "urdu": "کُلسّیوں"},
        "1 Thessalonians": {"file": "1thessalonians.json", "urdu": "۱-تھسّلُنیکیوں"},
        "2 Thessalonians": {"file": "2thessalonians.json", "urdu": "۲-تھسّلُنیکیوں"},
        "1 Timothy": {"file": "1timothy.json", "urdu": "۱-تیمُتھیُس"},
        "2 Timothy": {"file": "2timothy.json", "urdu": "۲-تیمُتھیُس"},
        "Titus": {"file": "titus.json", "urdu": "طِطُس"},
        "Philemon": {"file": "philemon.json", "urdu": "فِلیمون"},
        "Hebrews": {"file": "hebrews.json", "urdu": "عبرانیوں"},
        "James": {"file": "james.json", "urdu": "یعقُوب"},
        "1 Peter": {"file": "1peter.json", "urdu": "۱-پطرس"},
        "2 Peter": {"file": "2peter.json", "urdu": "۲-پطرس"},
        "1 John": {"file": "1john.json", "urdu": "۱-یُوحنّا"},
        "2 John": {"file": "2john.json", "urdu": "۲-یُوحنّا"},
        "3 John": {"file": "3john.json", "urdu": "۳-یُوحنّا"},
        "Jude": {"file": "jude.json", "urdu": "یہُوداہ"},
        "Revelation": {"file": "revelation.json", "urdu": "مکاشفہ"},
    }

    for book_data in bible_data:
        book_name = book_data.get("name", book_data.get("book", ""))

        # Normalize book name
        normalized_name = None
        for key in FILE_MAP:
            if key.lower() == book_name.lower() or key.replace(" ", "").lower() == book_name.replace(" ", "").lower():
                normalized_name = key
                break

        if not normalized_name:
            print(f"Unknown book: {book_name}")
            continue

        info = FILE_MAP[normalized_name]
        file_name = info["file"]
        urdu_name = info["urdu"]
        file_path = os.path.join(output_dir, file_name)

        # Extract chapters
        chapters = []
        chapters_data = book_data.get("chapters", [])

        for ch_idx, chapter_verses in enumerate(chapters_data):
            ch_num = ch_idx + 1
            verses = []

            if isinstance(chapter_verses, list):
                for v_idx, verse_text in enumerate(chapter_verses):
                    verses.append({
                        "verse": v_idx + 1,
                        "text": verse_text.strip() if isinstance(verse_text, str) else str(verse_text)
                    })
            elif isinstance(chapter_verses, dict):
                for v_num, verse_text in chapter_verses.items():
                    verses.append({
                        "verse": int(v_num),
                        "text": verse_text.strip()
                    })

            if verses:
                chapters.append({
                    "chapter": ch_num,
                    "verses": verses
                })

        # Save the book
        output_data = {
            "book": urdu_name,
            "bookEnglish": normalized_name,
            "chapters": chapters
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        total_verses = sum(len(ch["verses"]) for ch in chapters)
        print(f"Saved {normalized_name} ({urdu_name}): {len(chapters)} chapters, {total_verses} verses")

if __name__ == "__main__":
    main()


