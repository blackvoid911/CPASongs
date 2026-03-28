"""
Fix the missing Job chapter by reprocessing job.html from cache.
"""
import re
import json
import os
from bs4 import BeautifulSoup

CACHE_FILE = r"C:\xampp\htdocs\cpa\cache\bible\job.html"
OUTPUT_FILE = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu\job.json"

def is_urdu(text):
    """Check if text contains Urdu characters"""
    return any('\u0600' <= c <= '\u06ff' for c in text)

def process_job():
    """Process Job from HTML cache"""

    if not os.path.exists(CACHE_FILE):
        print(f"ERROR: Cache file not found: {CACHE_FILE}")
        return False

    print(f"Reading: {CACHE_FILE}")
    print(f"Size: {os.path.getsize(CACHE_FILE):,} bytes")

    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")

        chapters = {}
        verse_pattern = re.compile(r"^JOB\.\d+\.\d+$", re.IGNORECASE)

        # Find all verse spans
        verse_count = 0
        for span in soup.find_all("span", id=verse_pattern):
            verse_id = span.get("id", "")
            parts = verse_id.upper().split(".")

            if len(parts) != 3:
                continue

            try:
                ch, vn = int(parts[1]), int(parts[2])
            except ValueError:
                continue

            # Extract text - try nested span first, then direct text
            inner = span.find("span", class_=False)
            if inner:
                text = inner.get_text(strip=True)
            else:
                text = span.get_text(separator=" ", strip=True)
                # Remove leading verse number if present
                text = re.sub(r"^\d+\s*", "", text).strip()

            # Skip empty or non-Urdu text
            if not text or not is_urdu(text):
                continue

            # Store verse (only if not already present)
            chapters.setdefault(ch, {})
            if vn not in chapters[ch]:
                chapters[ch][vn] = text
                verse_count += 1

        # Build JSON structure
        result = {
            "book": "ایّوب",
            "bookEnglish": "Job",
            "chapters": []
        }

        for ch_num in sorted(chapters.keys()):
            verses = [
                {"verse": v, "text": t}
                for v, t in sorted(chapters[ch_num].items())
            ]
            result["chapters"].append({
                "chapter": ch_num,
                "verses": verses
            })

        ch_count = len(chapters)

        print(f"\nExtracted:")
        print(f"  Chapters: {ch_count}/42")
        print(f"  Verses: {verse_count}")

        if ch_count < 42:
            print(f"\n  WARNING: Still missing {42 - ch_count} chapter(s)")
            missing = [i for i in range(1, 43) if i not in chapters]
            print(f"  Missing chapters: {missing}")

        # Show chapter distribution
        print(f"\nChapter distribution:")
        for ch in range(1, 43):
            if ch in chapters:
                v_count = len(chapters[ch])
                print(f"  Ch {ch:2d}: {v_count:3d} verses ✓")
            else:
                print(f"  Ch {ch:2d}: MISSING ❌")

        # Write JSON file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Written to: {OUTPUT_FILE}")
        return ch_count == 42

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Fixing Job (Urdu) - Reprocessing from cache")
    print("=" * 70)

    success = process_job()

    print("=" * 70)
    if success:
        print("SUCCESS: Job is now complete with all 42 chapters!")
    else:
        print("INCOMPLETE: Review the output above for details")

