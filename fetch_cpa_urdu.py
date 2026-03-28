"""
Fetch Urdu Bible from CPA Pakistan website (https://cpa-pk.org/bible/)
"""
import urllib.request
import json
import os
import re
import time
import ssl
from html.parser import HTMLParser

# SSL context
ctx = ssl.create_default_context()

OUTPUT_DIR = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"

# Book mappings: (url_slug, english_name, urdu_name, file_name, chapters)
BOOKS = [
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

class VerseParser(HTMLParser):
    """Parse verses from CPA Bible HTML"""
    def __init__(self):
        super().__init__()
        self.verses = []
        self.current_verse = None
        self.current_text = ""
        self.in_verse = False
        self.in_verse_num = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_name = attrs_dict.get('class', '')

        # Look for verse containers
        if 'verse' in class_name.lower() or tag == 'span' and 'v' in class_name:
            self.in_verse = True
        if 'verse-num' in class_name or 'vn' in class_name:
            self.in_verse_num = True

    def handle_endtag(self, tag):
        if self.in_verse_num:
            self.in_verse_num = False
        if tag in ['p', 'div', 'br'] and self.current_text.strip():
            if self.current_verse:
                self.verses.append({
                    "verse": self.current_verse,
                    "text": self.current_text.strip()
                })
            self.current_text = ""

    def handle_data(self, data):
        if self.in_verse_num:
            try:
                self.current_verse = int(data.strip())
            except:
                pass
        elif self.in_verse:
            self.current_text += data


def fetch_chapter(book_slug, chapter):
    """Fetch a chapter from CPA website"""
    # Try different URL patterns
    urls = [
        f"https://cpa-pk.org/bible/{book_slug}/{chapter}/",
        f"https://cpa-pk.org/bible/{book_slug}-{chapter}/",
        f"https://cpa-pk.org/bible/{book_slug}{chapter}/",
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5,ur;q=0.3',
    }

    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                html = resp.read().decode('utf-8')

                # Extract verses using regex patterns
                verses = extract_verses_from_html(html)
                if verses:
                    return verses

        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
            print(f"    HTTP Error {e.code} for {url}")
        except Exception as e:
            print(f"    Error: {e}")

    return None


def extract_verses_from_html(html):
    """Extract verses from HTML using multiple patterns"""
    verses = []

    # Pattern 1: Look for verse spans with class containing verse number
    # <span class="v1">verse text</span>
    pattern1 = re.compile(r'<span[^>]*class=["\'][^"\']*v(\d+)[^"\']*["\'][^>]*>([^<]+)</span>', re.IGNORECASE)

    # Pattern 2: Verse number followed by text
    # <sup>1</sup> verse text
    pattern2 = re.compile(r'<sup[^>]*>(\d+)</sup>\s*([^<]+)', re.IGNORECASE)

    # Pattern 3: Urdu verse format with numbers
    # ۱ verse text (Urdu numerals)
    urdu_nums = {'۰': 0, '۱': 1, '۲': 2, '۳': 3, '۴': 4, '۵': 5, '۶': 6, '۷': 7, '۸': 8, '۹': 9}

    # Pattern 4: Look for paragraph or div with verse content
    pattern4 = re.compile(r'<p[^>]*class=["\'][^"\']*verse[^"\']*["\'][^>]*>.*?</p>', re.IGNORECASE | re.DOTALL)

    # Try pattern 1
    for match in pattern1.finditer(html):
        verse_num = int(match.group(1))
        verse_text = match.group(2).strip()
        if verse_text and not verse_text.isdigit():
            verses.append({"verse": verse_num, "text": clean_text(verse_text)})

    if verses:
        return sorted(verses, key=lambda x: x["verse"])

    # Try pattern 2
    for match in pattern2.finditer(html):
        verse_num = int(match.group(1))
        verse_text = match.group(2).strip()
        if verse_text and not verse_text.isdigit():
            verses.append({"verse": verse_num, "text": clean_text(verse_text)})

    if verses:
        return sorted(verses, key=lambda x: x["verse"])

    # Try to find content div and extract text
    content_match = re.search(r'<div[^>]*class=["\'][^"\']*content[^"\']*["\'][^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
    if content_match:
        content = content_match.group(1)
        # Look for numbered verses
        lines = re.split(r'<br\s*/?>|</p>|</div>', content)
        verse_num = 1
        for line in lines:
            text = re.sub(r'<[^>]+>', '', line).strip()
            if text:
                # Check if line starts with a number
                num_match = re.match(r'^(\d+)\s*[\.:\s]\s*(.+)', text)
                if num_match:
                    verse_num = int(num_match.group(1))
                    text = num_match.group(2)
                verses.append({"verse": verse_num, "text": clean_text(text)})
                verse_num += 1

    return verses if verses else None


def clean_text(text):
    """Clean up verse text"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove verse numbers at start
    text = re.sub(r'^\d+[\.:]\s*', '', text)
    return text.strip()


def main():
    print("=" * 60)
    print("CPA Pakistan Urdu Bible Downloader")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # First, test fetch one chapter to see the HTML structure
    print("\nTesting connection to cpa-pk.org...")
    test_url = "https://cpa-pk.org/bible/gen/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
    }

    try:
        req = urllib.request.Request(test_url, headers=headers)
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            html = resp.read().decode('utf-8')
            print(f"SUCCESS! Got {len(html)} bytes")

            # Save sample HTML for analysis
            with open(os.path.join(OUTPUT_DIR, "..", "cpa_sample.html"), "w", encoding="utf-8") as f:
                f.write(html)
            print("Saved sample HTML to cpa_sample.html")

            # Try to extract verses
            verses = extract_verses_from_html(html)
            if verses:
                print(f"Found {len(verses)} verses!")
                print(f"First verse: {verses[0]}")
            else:
                print("Could not extract verses from HTML")
                # Print a snippet for debugging
                print("\nHTML snippet (first 2000 chars):")
                print(html[:2000])

    except Exception as e:
        print(f"Error connecting: {e}")
        return

    # Continue with full download if test successful
    total_books = len(BOOKS)
    stats = {"success": 0, "partial": 0, "failed": 0}

    for idx, (slug, eng_name, urdu_name, file_name, num_chapters) in enumerate(BOOKS, 1):
        file_path = os.path.join(OUTPUT_DIR, file_name)
        print(f"\n[{idx}/{total_books}] {eng_name} ({urdu_name}) - {num_chapters} chapters")

        chapters = []
        success_count = 0

        for ch in range(1, num_chapters + 1):
            verses = fetch_chapter(slug, ch)

            if verses and len(verses) > 0:
                chapters.append({
                    "chapter": ch,
                    "verses": verses
                })
                success_count += 1
                print(f"  Ch {ch}: {len(verses)} verses")
            else:
                chapters.append({
                    "chapter": ch,
                    "verses": [{"verse": 1, "text": f"باب {ch}"}]
                })
                print(f"  Ch {ch}: placeholder")

            time.sleep(0.5)

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
        elif success_count > 0:
            stats["partial"] += 1
        else:
            stats["failed"] += 1

        print(f"  Saved: {success_count}/{num_chapters} chapters")
        time.sleep(1)

    print("\n" + "=" * 60)
    print("COMPLETE")
    print(f"  Success: {stats['success']}")
    print(f"  Partial: {stats['partial']}")
    print(f"  Failed:  {stats['failed']}")
    print("=" * 60)


if __name__ == "__main__":
    main()

