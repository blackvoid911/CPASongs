"""
Script to generate complete Bible JSON files for the CPASongs app.
Uses the King James Version (KJV) which is public domain.
"""

import json
import urllib.request
import os
import time

# Bible book info with correct chapter counts
BIBLE_BOOKS = [
    {"name": "Genesis", "file": "genesis.json", "chapters": 50},
    {"name": "Exodus", "file": "exodus.json", "chapters": 40},
    {"name": "Leviticus", "file": "leviticus.json", "chapters": 27},
    {"name": "Numbers", "file": "numbers.json", "chapters": 36},
    {"name": "Deuteronomy", "file": "deuteronomy.json", "chapters": 34},
    {"name": "Joshua", "file": "joshua.json", "chapters": 24},
    {"name": "Judges", "file": "judges.json", "chapters": 21},
    {"name": "Ruth", "file": "ruth.json", "chapters": 4},
    {"name": "1 Samuel", "file": "1_samuel.json", "chapters": 31},
    {"name": "2 Samuel", "file": "2_samuel.json", "chapters": 24},
    {"name": "1 Kings", "file": "1_kings.json", "chapters": 22},
    {"name": "2 Kings", "file": "2_kings.json", "chapters": 25},
    {"name": "1 Chronicles", "file": "1_chronicles.json", "chapters": 29},
    {"name": "2 Chronicles", "file": "2_chronicles.json", "chapters": 36},
    {"name": "Ezra", "file": "ezra.json", "chapters": 10},
    {"name": "Nehemiah", "file": "nehemiah.json", "chapters": 13},
    {"name": "Esther", "file": "esther.json", "chapters": 10},
    {"name": "Job", "file": "job.json", "chapters": 42},
    {"name": "Psalms", "file": "psalms.json", "chapters": 150},
    {"name": "Proverbs", "file": "proverbs.json", "chapters": 31},
    {"name": "Ecclesiastes", "file": "ecclesiastes.json", "chapters": 12},
    {"name": "Song of Solomon", "file": "song_of_solomon.json", "chapters": 8},
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
    {"name": "1 Corinthians", "file": "1_corinthians.json", "chapters": 16},
    {"name": "2 Corinthians", "file": "2_corinthians.json", "chapters": 13},
    {"name": "Galatians", "file": "galatians.json", "chapters": 6},
    {"name": "Ephesians", "file": "ephesians.json", "chapters": 6},
    {"name": "Philippians", "file": "philippians.json", "chapters": 4},
    {"name": "Colossians", "file": "colossians.json", "chapters": 4},
    {"name": "1 Thessalonians", "file": "1_thessalonians.json", "chapters": 5},
    {"name": "2 Thessalonians", "file": "2_thessalonians.json", "chapters": 3},
    {"name": "1 Timothy", "file": "1_timothy.json", "chapters": 6},
    {"name": "2 Timothy", "file": "2_timothy.json", "chapters": 4},
    {"name": "Titus", "file": "titus.json", "chapters": 3},
    {"name": "Philemon", "file": "philemon.json", "chapters": 1},
    {"name": "Hebrews", "file": "hebrews.json", "chapters": 13},
    {"name": "James", "file": "james.json", "chapters": 5},
    {"name": "1 Peter", "file": "1_peter.json", "chapters": 5},
    {"name": "2 Peter", "file": "2_peter.json", "chapters": 3},
    {"name": "1 John", "file": "1_john.json", "chapters": 5},
    {"name": "2 John", "file": "2_john.json", "chapters": 1},
    {"name": "3 John", "file": "3_john.json", "chapters": 1},
    {"name": "Jude", "file": "jude.json", "chapters": 1},
    {"name": "Revelation", "file": "revelation.json", "chapters": 22},
]

# API endpoint for Bible verses (using bible-api.com which provides KJV)
API_BASE = "https://bible-api.com"

def get_api_book_name(book_name):
    """Convert book name to API-compatible format"""
    # bible-api.com uses specific formats
    mapping = {
        "1 Samuel": "1samuel",
        "2 Samuel": "2samuel",
        "1 Kings": "1kings",
        "2 Kings": "2kings",
        "1 Chronicles": "1chronicles",
        "2 Chronicles": "2chronicles",
        "Song of Solomon": "songofsolomon",
        "1 Corinthians": "1corinthians",
        "2 Corinthians": "2corinthians",
        "1 Thessalonians": "1thessalonians",
        "2 Thessalonians": "2thessalonians",
        "1 Timothy": "1timothy",
        "2 Timothy": "2timothy",
        "1 Peter": "1peter",
        "2 Peter": "2peter",
        "1 John": "1john",
        "2 John": "2john",
        "3 John": "3john",
    }
    return mapping.get(book_name, book_name.lower().replace(" ", ""))

def fetch_chapter(book_name, chapter):
    """Fetch a single chapter from the API"""
    api_book = get_api_book_name(book_name)
    url = f"{API_BASE}/{api_book}+{chapter}?translation=kjv"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())

            if "verses" in data:
                return [{"verse": v["verse"], "text": v["text"].strip()} for v in data["verses"]]
            return []
    except Exception as e:
        print(f"  Error fetching {book_name} {chapter}: {e}")
        return []

def generate_book(book_info, output_dir):
    """Generate complete JSON for a single book"""
    book_name = book_info["name"]
    file_name = book_info["file"]
    chapters_count = book_info["chapters"]

    print(f"Processing {book_name} ({chapters_count} chapters)...")

    book_data = {
        "book": book_name,
        "chapters": []
    }

    for chapter_num in range(1, chapters_count + 1):
        verses = fetch_chapter(book_name, chapter_num)
        if verses:
            book_data["chapters"].append({
                "chapter": chapter_num,
                "verses": verses
            })
            print(f"  Chapter {chapter_num}: {len(verses)} verses")
        else:
            print(f"  Chapter {chapter_num}: FAILED")

        # Small delay to be respectful to the API
        time.sleep(0.2)

    # Write to file
    output_path = os.path.join(output_dir, file_name)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(book_data, f, ensure_ascii=False)

    print(f"  Saved to {file_name}")
    return True

def main():
    # Output directory
    output_dir = os.path.join(os.path.dirname(__file__), "app", "src", "main", "assets", "bible")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Output directory: {output_dir}")
    print(f"Total books to process: {len(BIBLE_BOOKS)}")
    print("=" * 50)

    successful = 0
    failed = []

    for book in BIBLE_BOOKS:
        try:
            if generate_book(book, output_dir):
                successful += 1
        except Exception as e:
            print(f"Failed to process {book['name']}: {e}")
            failed.append(book['name'])

    print("=" * 50)
    print(f"Completed: {successful}/{len(BIBLE_BOOKS)} books")
    if failed:
        print(f"Failed: {', '.join(failed)}")

if __name__ == "__main__":
    main()

