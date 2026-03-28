"""
Generate complete Bible using a different public domain source.
This script uses static data to generate complete verses.
"""

import json
import os

# Since the API is rate-limited, we'll use a different approach
# Download from a public domain KJV Bible source

def download_kjv_bible():
    """Download KJV Bible from a public domain GitHub repository"""
    import urllib.request
    import time

    # Using the Bible.json from GitHub
    # This is a public domain KJV Bible in JSON format
    urls = [
        "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/en_kjv.json",
        "https://raw.githubusercontent.com/aruljohn/Bible-kjv/master/Bible-kjv.json",
    ]

    for url in urls:
        try:
            print(f"Trying {url}...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=60) as response:
                data = response.read().decode('utf-8-sig')  # Handle BOM
                print(f"Downloaded {len(data)} bytes")
                return json.loads(data)
        except Exception as e:
            print(f"Failed: {e}")
            time.sleep(2)

    return None

def main():
    print("Downloading KJV Bible...")
    bible_data = download_kjv_bible()

    if not bible_data:
        print("Failed to download Bible data")
        return

    print(f"Downloaded Bible with {len(bible_data)} books")

    # Process and save
    output_dir = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible"

    # Map of Bible book names to file names
    FILE_MAP = {
        "Genesis": "genesis.json",
        "Exodus": "exodus.json",
        "Leviticus": "leviticus.json",
        "Numbers": "numbers.json",
        "Deuteronomy": "deuteronomy.json",
        "Joshua": "joshua.json",
        "Judges": "judges.json",
        "Ruth": "ruth.json",
        "1 Samuel": "1_samuel.json",
        "2 Samuel": "2_samuel.json",
        "1 Kings": "1_kings.json",
        "2 Kings": "2_kings.json",
        "1 Chronicles": "1_chronicles.json",
        "2 Chronicles": "2_chronicles.json",
        "Ezra": "ezra.json",
        "Nehemiah": "nehemiah.json",
        "Esther": "esther.json",
        "Job": "job.json",
        "Psalms": "psalms.json",
        "Proverbs": "proverbs.json",
        "Ecclesiastes": "ecclesiastes.json",
        "Song of Solomon": "song_of_solomon.json",
        "Isaiah": "isaiah.json",
        "Jeremiah": "jeremiah.json",
        "Lamentations": "lamentations.json",
        "Ezekiel": "ezekiel.json",
        "Daniel": "daniel.json",
        "Hosea": "hosea.json",
        "Joel": "joel.json",
        "Amos": "amos.json",
        "Obadiah": "obadiah.json",
        "Jonah": "jonah.json",
        "Micah": "micah.json",
        "Nahum": "nahum.json",
        "Habakkuk": "habakkuk.json",
        "Zephaniah": "zephaniah.json",
        "Haggai": "haggai.json",
        "Zechariah": "zechariah.json",
        "Malachi": "malachi.json",
        "Matthew": "matthew.json",
        "Mark": "mark.json",
        "Luke": "luke.json",
        "John": "john.json",
        "Acts": "acts.json",
        "Romans": "romans.json",
        "1 Corinthians": "1_corinthians.json",
        "2 Corinthians": "2_corinthians.json",
        "Galatians": "galatians.json",
        "Ephesians": "ephesians.json",
        "Philippians": "philippians.json",
        "Colossians": "colossians.json",
        "1 Thessalonians": "1_thessalonians.json",
        "2 Thessalonians": "2_thessalonians.json",
        "1 Timothy": "1_timothy.json",
        "2 Timothy": "2_timothy.json",
        "Titus": "titus.json",
        "Philemon": "philemon.json",
        "Hebrews": "hebrews.json",
        "James": "james.json",
        "1 Peter": "1_peter.json",
        "2 Peter": "2_peter.json",
        "1 John": "1_john.json",
        "2 John": "2_john.json",
        "3 John": "3_john.json",
        "Jude": "jude.json",
        "Revelation": "revelation.json",
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

        file_name = FILE_MAP[normalized_name]
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
            "book": normalized_name,
            "chapters": chapters
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False)

        total_verses = sum(len(ch["verses"]) for ch in chapters)
        print(f"Saved {normalized_name}: {len(chapters)} chapters, {total_verses} verses")

if __name__ == "__main__":
    main()


