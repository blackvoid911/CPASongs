"""
Fetch complete Bible chapters with ALL verses from bible-api.com
Uses proper rate limiting and retry logic to avoid HTTP 429 errors.
"""

import json
import os
import time
import urllib.request
import urllib.error

# Book information with correct chapter counts
BOOKS = [
    {"name": "Genesis", "file": "genesis.json", "chapters": 50},
    {"name": "Exodus", "file": "exodus.json", "chapters": 40},
    {"name": "Leviticus", "file": "leviticus.json", "chapters": 27},
    {"name": "Numbers", "file": "numbers.json", "chapters": 36},
    {"name": "Deuteronomy", "file": "deuteronomy.json", "chapters": 34},
    {"name": "Joshua", "file": "joshua.json", "chapters": 24},
    {"name": "Judges", "file": "judges.json", "chapters": 21},
    {"name": "Ruth", "file": "ruth.json", "chapters": 4},
    {"name": "1 Samuel", "abbrev": "1Samuel", "file": "1_samuel.json", "chapters": 31},
    {"name": "2 Samuel", "abbrev": "2Samuel", "file": "2_samuel.json", "chapters": 24},
    {"name": "1 Kings", "abbrev": "1Kings", "file": "1_kings.json", "chapters": 22},
    {"name": "2 Kings", "abbrev": "2Kings", "file": "2_kings.json", "chapters": 25},
    {"name": "1 Chronicles", "abbrev": "1Chronicles", "file": "1_chronicles.json", "chapters": 29},
    {"name": "2 Chronicles", "abbrev": "2Chronicles", "file": "2_chronicles.json", "chapters": 36},
    {"name": "Ezra", "file": "ezra.json", "chapters": 10},
    {"name": "Nehemiah", "file": "nehemiah.json", "chapters": 13},
    {"name": "Esther", "file": "esther.json", "chapters": 10},
    {"name": "Job", "file": "job.json", "chapters": 42},
    {"name": "Psalms", "file": "psalms.json", "chapters": 150},
    {"name": "Proverbs", "file": "proverbs.json", "chapters": 31},
    {"name": "Ecclesiastes", "file": "ecclesiastes.json", "chapters": 12},
    {"name": "Song of Solomon", "abbrev": "SongofSolomon", "file": "song_of_solomon.json", "chapters": 8},
    {"name": "Isaiah", "file": "isaiah.json", "chapters": 66},
    {"name": "Jeremiah", "file": "jeremiah.json", "chapters": 52},
    {"name": "Lamentations", "file": "lamentations.json", "chapters": 5},
    {"name": "Ezekiel", "file": "ezekiel.json", "chapters": 48},
    {"name": "Daniel", "file": "daniel.json", "chapters": 12},
    {"name": "Hosea", "file": "hosea.json", "chapters": 14},
    {"name": "Joel", "file": "joel.json", "chapters": 3},
    {"name": "Amos", "file": "amos.json", "chapters": 9},
    {"name": "Obadiah", "file": "obadiah.json", "chapters": 1},
    {"name": "Jonah", "file": "jonah.json", "chapters": 4},
    {"name": "Micah", "file": "micah.json", "chapters": 7},
    {"name": "Nahum", "file": "nahum.json", "chapters": 3},
    {"name": "Habakkuk", "file": "habakkuk.json", "chapters": 3},
    {"name": "Zephaniah", "file": "zephaniah.json", "chapters": 3},
    {"name": "Haggai", "file": "haggai.json", "chapters": 2},
    {"name": "Zechariah", "file": "zechariah.json", "chapters": 14},
    {"name": "Malachi", "file": "malachi.json", "chapters": 4},
    {"name": "Matthew", "file": "matthew.json", "chapters": 28},
    {"name": "Mark", "file": "mark.json", "chapters": 16},
    {"name": "Luke", "file": "luke.json", "chapters": 24},
    {"name": "John", "file": "john.json", "chapters": 21},
    {"name": "Acts", "file": "acts.json", "chapters": 28},
    {"name": "Romans", "file": "romans.json", "chapters": 16},
    {"name": "1 Corinthians", "abbrev": "1Corinthians", "file": "1_corinthians.json", "chapters": 16},
    {"name": "2 Corinthians", "abbrev": "2Corinthians", "file": "2_corinthians.json", "chapters": 13},
    {"name": "Galatians", "file": "galatians.json", "chapters": 6},
    {"name": "Ephesians", "file": "ephesians.json", "chapters": 6},
    {"name": "Philippians", "file": "philippians.json", "chapters": 4},
    {"name": "Colossians", "file": "colossians.json", "chapters": 4},
    {"name": "1 Thessalonians", "abbrev": "1Thessalonians", "file": "1_thessalonians.json", "chapters": 5},
    {"name": "2 Thessalonians", "abbrev": "2Thessalonians", "file": "2_thessalonians.json", "chapters": 3},
    {"name": "1 Timothy", "abbrev": "1Timothy", "file": "1_timothy.json", "chapters": 6},
    {"name": "2 Timothy", "abbrev": "2Timothy", "file": "2_timothy.json", "chapters": 4},
    {"name": "Titus", "file": "titus.json", "chapters": 3},
    {"name": "Philemon", "file": "philemon.json", "chapters": 1},
    {"name": "Hebrews", "file": "hebrews.json", "chapters": 13},
    {"name": "James", "file": "james.json", "chapters": 5},
    {"name": "1 Peter", "abbrev": "1Peter", "file": "1_peter.json", "chapters": 5},
    {"name": "2 Peter", "abbrev": "2Peter", "file": "2_peter.json", "chapters": 3},
    {"name": "1 John", "abbrev": "1John", "file": "1_john.json", "chapters": 5},
    {"name": "2 John", "abbrev": "2John", "file": "2_john.json", "chapters": 1},
    {"name": "3 John", "abbrev": "3John", "file": "3_john.json", "chapters": 1},
    {"name": "Jude", "file": "jude.json", "chapters": 1},
    {"name": "Revelation", "file": "revelation.json", "chapters": 22},
]

def fetch_chapter(book_name, chapter, retries=5):
    """Fetch a single chapter with all verses from bible-api.com"""
    # Use abbreviation if available, otherwise use book name
    api_name = book_name.replace(" ", "%20")
    url = f"https://bible-api.com/{api_name}%20{chapter}?translation=kjv"

    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))

                verses = []
                if 'verses' in data:
                    for v in data['verses']:
                        verses.append({
                            "verse": v['verse'],
                            "text": v['text'].strip()
                        })
                return verses

        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = (attempt + 1) * 10  # Exponential backoff
                print(f"    Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"    HTTP Error {e.code}: {e.reason}")
                return None
        except Exception as e:
            print(f"    Error: {e}")
            time.sleep(2)

    return None

def main():
    output_dir = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible"

    # Track progress
    total_chapters = sum(b["chapters"] for b in BOOKS)
    completed_chapters = 0

    for book in BOOKS:
        book_name = book["name"]
        file_name = book["file"]
        num_chapters = book["chapters"]
        api_name = book.get("abbrev", book_name)

        file_path = os.path.join(output_dir, file_name)

        # Check if book already has complete verses
        existing_data = None
        existing_complete = False
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                    # Check if first chapter has more than 5 verses (indicating it's complete)
                    if existing_data.get("chapters") and len(existing_data["chapters"]) > 0:
                        first_ch = existing_data["chapters"][0]
                        if len(first_ch.get("verses", [])) > 10:
                            existing_complete = True
            except:
                pass

        if existing_complete:
            print(f"[OK] {book_name}: Already complete")
            completed_chapters += num_chapters
            continue

        print(f"[>>] Fetching {book_name} ({num_chapters} chapters)...")

        chapters = []
        for ch in range(1, num_chapters + 1):
            print(f"  Chapter {ch}/{num_chapters}...", end=" ", flush=True)

            verses = fetch_chapter(api_name, ch)

            if verses and len(verses) > 0:
                chapters.append({
                    "chapter": ch,
                    "verses": verses
                })
                print(f"OK {len(verses)} verses")
            else:
                print("FAILED")
                # Use placeholder
                chapters.append({
                    "chapter": ch,
                    "verses": [{"verse": 1, "text": f"Chapter {ch}"}]
                })

            # Rate limiting - wait between requests
            time.sleep(1.5)

        # Save the book
        book_data = {
            "book": book_name,
            "chapters": chapters
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(book_data, f, ensure_ascii=False)

        completed_chapters += num_chapters
        print(f"  Saved {book_name} ({completed_chapters}/{total_chapters} total chapters)")

        # Small delay between books
        time.sleep(2)

if __name__ == "__main__":
    main()



