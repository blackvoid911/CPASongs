"""
Parse all HTML files from C:\\xampp\\htdocs\\cpa\\cache\\bible\\english
and update (or create fresh) the English Bible JSON files in the app assets.

Maps cache filenames → asset JSON filenames using span IDs like MRK.1.1
"""
import re
import json
import os
from bs4 import BeautifulSoup

CACHE_DIR  = r"C:\xampp\htdocs\cpa\cache\bible\english"
ASSETS_DIR = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible"

# Map: 3-letter book code (upper) -> JSON filename (without .json)
BOOK_MAP = {
    "GEN": "genesis",
    "EXO": "exodus",
    "LEV": "leviticus",
    "NUM": "numbers",
    "DEU": "deuteronomy",
    "JOS": "joshua",
    "JDG": "judges",
    "RUT": "ruth",
    "1SA": "1_samuel",
    "2SA": "2_samuel",
    "1KI": "1_kings",
    "2KI": "2_kings",
    "1CH": "1_chronicles",
    "2CH": "2_chronicles",
    "EZR": "ezra",
    "NEH": "nehemiah",
    "EST": "esther",
    "JOB": "job",
    "PSA": "psalms",
    "PRO": "proverbs",
    "ECC": "ecclesiastes",
    "SNG": "song_of_solomon",
    "ISA": "isaiah",
    "JER": "jeremiah",
    "LAM": "lamentations",
    "EZK": "ezekiel",
    "DAN": "daniel",
    "HOS": "hosea",
    "JOL": "joel",
    "AMO": "amos",
    "OBA": "obadiah",
    "JON": "jonah",
    "MIC": "micah",
    "NAM": "nahum",
    "HAB": "habakkuk",
    "ZEP": "zephaniah",
    "HAG": "haggai",
    "ZEC": "zechariah",
    "MAL": "malachi",
    "MAT": "matthew",
    "MRK": "mark",
    "LUK": "luke",
    "JHN": "john",
    "ACT": "acts",
    "ROM": "romans",
    "1CO": "1_corinthians",
    "2CO": "2_corinthians",
    "GAL": "galatians",
    "EPH": "ephesians",
    "PHP": "philippians",
    "COL": "colossians",
    "1TH": "1_thessalonians",
    "2TH": "2_thessalonians",
    "1TI": "1_timothy",
    "2TI": "2_timothy",
    "TIT": "titus",
    "PHM": "philemon",
    "HEB": "hebrews",
    "JAS": "james",
    "1PE": "1_peter",
    "2PE": "2_peter",
    "1JN": "1_john",
    "2JN": "2_john",
    "3JN": "3_john",
    "JUD": "jude",
    "REV": "revelation",
}


def parse_html(html_path):
    """
    Parse a CPA HTML cache file.
    Returns dict: {chapter_num (int): {verse_num (int): text}}
    """
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    chapters = {}
    # Every verse span has id="BOOK.CH.V"
    for span in soup.find_all("span", id=re.compile(r"^[A-Z0-9]+\.\d+\.\d+$")):
        parts = span["id"].split(".")
        if len(parts) != 3:
            continue
        ch  = int(parts[1])
        vn  = int(parts[2])
        # The verse text is in the inner <span> without a class attribute
        text_span = span.find("span", class_=False)
        if text_span is None:
            # fallback: grab all text, strip verse number
            raw = span.get_text(separator=" ", strip=True)
            # remove leading digit(s)
            raw = re.sub(r"^\d+\s*", "", raw)
            text = raw.strip()
        else:
            text = text_span.get_text(strip=True)
        if not text:
            continue
        chapters.setdefault(ch, {})[vn] = text

    return chapters


def build_json(book_name, chapters_dict):
    """Build the standard {book, chapters:[{chapter, verses:[{verse,text}]}]} structure."""
    result = {"book": book_name, "chapters": []}
    for ch_num in sorted(chapters_dict.keys()):
        verses = []
        for v_num in sorted(chapters_dict[ch_num].keys()):
            verses.append({"verse": v_num, "text": chapters_dict[ch_num][v_num]})
        result["chapters"].append({"chapter": ch_num, "verses": verses})
    return result


def existing_verse_count(json_path):
    if not os.path.exists(json_path):
        return 0
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    return sum(len(ch.get("verses", [])) for ch in data.get("chapters", []))


def main():
    html_files = sorted(f for f in os.listdir(CACHE_DIR) if f.endswith(".html"))
    print(f"Found {len(html_files)} HTML files in cache.\n")

    updated  = []
    skipped  = []
    no_match = []

    for html_file in html_files:
        html_path = os.path.join(CACHE_DIR, html_file)

        # Parse verses from HTML
        try:
            chapters_dict = parse_html(html_path)
        except Exception as e:
            print(f"  [ERR] {html_file}: parse failed -- {e}")
            continue

        if not chapters_dict:
            print(f"  [SKIP] {html_file}: no verses found")
            skipped.append(html_file)
            continue

        # Detect book code from span IDs
        # Reopen to find the first span id
        with open(html_path, encoding="utf-8") as f:
            raw = f.read()
        m = re.search(r'id="([A-Z0-9]{2,3})\.\d+\.\d+"', raw)
        if not m:
            print(f"  [SKIP] {html_file}: could not detect book code")
            no_match.append(html_file)
            continue

        book_code = m.group(1)
        json_name = BOOK_MAP.get(book_code)
        if not json_name:
            print(f"  [SKIP] {html_file}: unknown book code '{book_code}'")
            no_match.append(html_file)
            continue

        json_path    = os.path.join(ASSETS_DIR, json_name + ".json")
        cache_total  = sum(len(v) for v in chapters_dict.values())
        exist_total  = existing_verse_count(json_path)

        ch_count = len(chapters_dict)

        # Always update if cache has more verses, or is a mismatch book
        if cache_total > exist_total or cache_total != exist_total:
            action = "UPDATE" if os.path.exists(json_path) else "CREATE"
            new_data = build_json(json_name.replace("_", " ").title(), chapters_dict)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)
            print(f"  [{action}] {json_name}.json  <- {html_file}  ({ch_count} ch, {cache_total} v)  was:{exist_total}")
            updated.append(json_name)
        else:
            print(f"  [OK]    {json_name}.json  already has {exist_total} v (cache:{cache_total}) -- no change")
            skipped.append(json_name)

    print(f"\n{'='*60}")
    print(f"  Updated : {len(updated)} books")
    print(f"  Skipped : {len(skipped)} books (already complete)")
    if no_match:
        print(f"  No match: {no_match}")
    print(f"{'='*60}")
    if updated:
        print("  Books updated:", ", ".join(updated))


if __name__ == "__main__":
    main()

