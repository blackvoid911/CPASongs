"""
Verify completeness of Urdu Bible files and identify which need reprocessing.
"""
import json, os

URDU_DIR = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"

# Expected chapter counts for all 66 books
EXPECTED = {
    "genesis": 50, "exodus": 40, "leviticus": 27, "numbers": 36, "deuteronomy": 34,
    "joshua": 24, "judges": 21, "ruth": 4, "1samuel": 31, "2samuel": 24,
    "1kings": 22, "2kings": 25, "1chronicles": 29, "2chronicles": 36, "ezra": 10,
    "nehemiah": 13, "esther": 10, "job": 42, "psalms": 150, "proverbs": 31,
    "ecclesiastes": 12, "songofsolomon": 8, "isaiah": 66, "jeremiah": 52, "lamentations": 5,
    "ezekiel": 48, "daniel": 12, "hosea": 14, "joel": 3, "amos": 9,
    "obadiah": 1, "jonah": 4, "micah": 7, "nahum": 3, "habakkuk": 3,
    "zephaniah": 3, "haggai": 2, "zechariah": 14, "malachi": 4,
    "matthew": 28, "mark": 16, "luke": 24, "john": 21, "acts": 28,
    "romans": 16, "1corinthians": 16, "2corinthians": 13, "galatians": 6, "ephesians": 6,
    "philippians": 4, "colossians": 4, "1thessalonians": 5, "2thessalonians": 3,
    "1timothy": 6, "2timothy": 4, "titus": 3, "philemon": 1, "hebrews": 13,
    "james": 5, "1peter": 5, "2peter": 3, "1john": 5, "2john": 1,
    "3john": 1, "jude": 1, "revelation": 22
}

complete = []
incomplete = []
missing = []
total_verses = 0
total_chapters = 0

print("Verifying Urdu Bible Completeness")
print("=" * 70)

for book_key, expected_ch in sorted(EXPECTED.items()):
    filepath = os.path.join(URDU_DIR, f"{book_key}.json")

    if not os.path.exists(filepath):
        missing.append(book_key)
        print(f"❌ {book_key:20s} - FILE MISSING")
        continue

    try:
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        actual_ch = len(data.get("chapters", []))
        verses = sum(len(ch.get("verses", [])) for ch in data.get("chapters", []))
        total_verses += verses
        total_chapters += actual_ch

        if actual_ch == expected_ch and verses > 0:
            complete.append(book_key)
            print(f"✓ {book_key:20s} {actual_ch:3d}/{expected_ch:3d} ch, {verses:4d} verses")
        elif actual_ch == 0 or verses == 0:
            incomplete.append(book_key)
            print(f"❌ {book_key:20s} {actual_ch:3d}/{expected_ch:3d} ch, {verses:4d} verses - EMPTY")
        else:
            incomplete.append(book_key)
            print(f"⚠ {book_key:20s} {actual_ch:3d}/{expected_ch:3d} ch, {verses:4d} verses - INCOMPLETE")

    except Exception as e:
        incomplete.append(book_key)
        print(f"❌ {book_key:20s} - ERROR: {e}")

print("=" * 70)
print(f"Complete:   {len(complete):2d} books")
print(f"Incomplete: {len(incomplete):2d} books")
print(f"Missing:    {len(missing):2d} books")
print(f"Total:      {total_chapters} chapters, {total_verses:,} verses")

if incomplete or missing:
    print("\nBooks needing reprocessing:")
    for book in sorted(incomplete + missing):
        print(f"  - {book}")

