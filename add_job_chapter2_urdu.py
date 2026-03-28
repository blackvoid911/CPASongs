"""
Fetch Job Chapter 2 in Urdu from GetBible.net API and add to existing job.json
"""
import json
import urllib.request
import ssl

# Book 18 = Job in GetBible API
API_URL = "https://getbible.net/json?passage=job+2&version=urdu"

def fetch_job_chapter_2():
    try:
        # Bypass SSL verification if needed
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(API_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            data = response.read().decode('utf-8-sig')
            print(f"Downloaded: {len(data)} bytes")

            # Parse JSON (GetBible returns JSONP, strip callback)
            if data.startswith('('):
                data = data[1:-2]  # Remove leading ( and trailing );

            bible_data = json.loads(data)
            print(f"Keys: {bible_data.keys()}")

            # Extract chapter 2 verses
            book_data = bible_data.get('book', [])
            if book_data:
                for chapter in book_data:
                    if chapter.get('chapter_nr') == '2':
                        verses = []
                        for verse_key, verse_data in chapter.get('chapter', {}).items():
                            if verse_key.isdigit():
                                verses.append({
                                    'verse': int(verse_key),
                                    'text': verse_data.get('verse', '')
                                })

                        verses.sort(key=lambda v: v['verse'])
                        print(f"Found {len(verses)} verses in chapter 2")
                        return verses

            return None

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def add_to_job_json(chapter_2_verses):
    job_path = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu\job.json"

    # Load existing Job data
    with open(job_path, encoding="utf-8") as f:
        job_data = json.load(f)

    # Find position to insert chapter 2 (after chapter 1)
    chapters = job_data['chapters']
    insert_pos = 1  # After chapter 1

    # Insert chapter 2
    ch2_data = {
        'chapter': 2,
        'verses': chapter_2_verses
    }

    chapters.insert(insert_pos, ch2_data)

    # Save updated file
    with open(job_path, 'w', encoding="utf-8") as f:
        json.dump(job_data, f, ensure_ascii=False, indent=2)

    print(f"✓ Added chapter 2 with {len(chapter_2_verses)} verses to job.json")
    print(f"  Total chapters now: {len(chapters)}")

if __name__ == "__main__":
    print("Fetching Job Chapter 2 in Urdu...")
    verses = fetch_job_chapter_2()

    if verses:
        print(f"\nSample verse: {verses[0]}")
        add_to_job_json(verses)
        print("\n✅ SUCCESS: Job is now complete!")
    else:
        print("\n❌ Failed to fetch chapter 2")

