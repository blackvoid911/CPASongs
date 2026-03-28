"""
Import Urdu Bible from C:\\xampp\\htdocs\\cpa\\cache\\bible\\ (root HTML files)
into app/src/main/assets/bible/urdu/

Root HTML files use the same span format: id="GEN.1.1" but text is Urdu.
Urdu JSON filenames use no underscores: 1chronicles.json, songofsolomon.json etc.
"""
import re
import json
import os
from bs4 import BeautifulSoup

CACHE_DIR  = r"C:\xampp\htdocs\cpa\cache\bible"          # root = Urdu
ASSETS_DIR = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"
OUT_FILE   = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\urdu_import_log.txt"

log = open(OUT_FILE, "w", encoding="utf-8")
def p(s=""): log.write(s + "\n"); log.flush()

# Map: book code (upper) -> Urdu JSON filename (no .json, no underscores)
BOOK_MAP = {
    "GEN": "genesis",         "EXO": "exodus",         "LEV": "leviticus",
    "NUM": "numbers",         "DEU": "deuteronomy",     "JOS": "joshua",
    "JDG": "judges",          "RUT": "ruth",            "1SA": "1samuel",
    "2SA": "2samuel",         "1KI": "1kings",          "2KI": "2kings",
    "1CH": "1chronicles",     "2CH": "2chronicles",     "EZR": "ezra",
    "NEH": "nehemiah",        "EST": "esther",          "JOB": "job",
    "PSA": "psalms",          "PRO": "proverbs",        "ECC": "ecclesiastes",
    "SNG": "songofsolomon",   "ISA": "isaiah",          "JER": "jeremiah",
    "LAM": "lamentations",    "EZK": "ezekiel",         "DAN": "daniel",
    "HOS": "hosea",           "JOL": "joel",            "AMO": "amos",
    "OBA": "obadiah",         "JON": "jonah",           "MIC": "micah",
    "NAM": "nahum",           "HAB": "habakkuk",        "ZEP": "zephaniah",
    "HAG": "haggai",          "ZEC": "zechariah",       "MAL": "malachi",
    "MAT": "matthew",         "MRK": "mark",            "LUK": "luke",
    "JHN": "john",            "ACT": "acts",            "ROM": "romans",
    "1CO": "1corinthians",    "2CO": "2corinthians",    "GAL": "galatians",
    "EPH": "ephesians",       "PHP": "philippians",     "COL": "colossians",
    "1TH": "1thessalonians",  "2TH": "2thessalonians",  "1TI": "1timothy",
    "2TI": "2timothy",        "TIT": "titus",           "PHM": "philemon",
    "HEB": "hebrews",         "JAS": "james",           "1PE": "1peter",
    "2PE": "2peter",          "1JN": "1john",           "2JN": "2john",
    "3JN": "3john",           "JUD": "jude",            "REV": "revelation",
}

# Urdu book names
URDU_NAMES = {
    "genesis": "پیدائش",           "exodus": "خروج",
    "leviticus": "احبار",          "numbers": "گنتی",
    "deuteronomy": "استثنا",       "joshua": "یشوع",
    "judges": "قضاۃ",              "ruth": "روت",
    "1samuel": "1۔سموئیل",         "2samuel": "2۔سموئیل",
    "1kings": "1۔سلاطین",          "2kings": "2۔سلاطین",
    "1chronicles": "1۔تواریخ",     "2chronicles": "2۔تواریخ",
    "ezra": "عزرا",                "nehemiah": "نحمیاہ",
    "esther": "آستر",              "job": "ایوب",
    "psalms": "زبور",              "proverbs": "امثال",
    "ecclesiastes": "واعظ",        "songofsolomon": "غزل الغزلات",
    "isaiah": "یسعیاہ",            "jeremiah": "یرمیاہ",
    "lamentations": "نوحہ",        "ezekiel": "حزقی ایل",
    "daniel": "دانی ایل",          "hosea": "ہوسیع",
    "joel": "یوایل",               "amos": "عاموس",
    "obadiah": "عبدیاہ",           "jonah": "یوناہ",
    "micah": "میکاہ",              "nahum": "ناحوم",
    "habakkuk": "حبقوق",           "zephaniah": "صفنیاہ",
    "haggai": "حجی",               "zechariah": "زکریاہ",
    "malachi": "ملاکی",
    "matthew": "متی",              "mark": "مرقس",
    "luke": "لوقا",                "john": "یوحنا",
    "acts": "اعمال",               "romans": "رومیوں",
    "1corinthians": "1۔کرنتھیوں", "2corinthians": "2۔کرنتھیوں",
    "galatians": "گلتیوں",        "ephesians": "افسیوں",
    "philippians": "فلپیوں",      "colossians": "کلسیوں",
    "1thessalonians": "1۔تھسلنیکیوں", "2thessalonians": "2۔تھسلنیکیوں",
    "1timothy": "1۔تیمتھیس",      "2timothy": "2۔تیمتھیس",
    "titus": "ططس",                "philemon": "فلیمون",
    "hebrews": "عبرانیوں",         "james": "یعقوب",
    "1peter": "1۔پطرس",           "2peter": "2۔پطرس",
    "1john": "1۔یوحنا",           "2john": "2۔یوحنا",
    "3john": "3۔یوحنا",           "jude": "یہوداہ",
    "revelation": "مکاشفہ",
}

def is_urdu(text):
    return any('\u0600' <= c <= '\u06ff' for c in text)

def parse_html(html_path):
    """Parse Urdu verse content from CPA root HTML file."""
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    chapters = {}
    for span in soup.find_all("span", id=re.compile(r"^[A-Z0-9]+\.\d+\.\d+$")):
        parts = span["id"].split(".")
        if len(parts) != 3:
            continue
        ch  = int(parts[1])
        vn  = int(parts[2])
        # Get inner text span (no class)
        text_span = span.find("span", class_=False)
        if text_span:
            text = text_span.get_text(strip=True)
        else:
            raw = span.get_text(separator=" ", strip=True)
            text = re.sub(r"^\d+\s*", "", raw).strip()
        if not text:
            continue
        # Skip if not Urdu
        if not is_urdu(text):
            continue
        chapters.setdefault(ch, {})[vn] = text

    return chapters

def build_json(json_name, chapters_dict):
    urdu_name = URDU_NAMES.get(json_name, json_name)
    result = {
        "book": urdu_name,
        "bookEnglish": json_name.replace("1", "1 ").replace("2", "2 ").replace("3", "3 ").title(),
        "chapters": []
    }
    for ch_num in sorted(chapters_dict.keys()):
        verses = [{"verse": v, "text": t}
                  for v, t in sorted(chapters_dict[ch_num].items())]
        result["chapters"].append({"chapter": ch_num, "verses": verses})
    return result

def existing_verse_count(json_path):
    if not os.path.exists(json_path):
        return 0
    try:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
        return sum(len(ch.get("verses", [])) for ch in data.get("chapters", []))
    except:
        return 0

def is_placeholder_json(json_path):
    """Returns True if file only has stub verses like 'باب 1'."""
    if not os.path.exists(json_path):
        return True
    try:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
        chapters = data.get("chapters", [])
        if not chapters:
            return True
        return all(len(ch.get("verses", [])) <= 1 for ch in chapters)
    except:
        return True

def main():
    html_files = sorted([
        f for f in os.listdir(CACHE_DIR)
        if f.endswith(".html") and not f.startswith("build-")
        and not f.startswith("fix-") and not f.startswith("inject-")
        and not f.startswith("translate-") and not f.startswith("count-")
        and not f.startswith("download-")
    ])
    p(f"Found {len(html_files)} HTML files to process.\n")

    updated   = []
    skipped   = []
    no_urdu   = []
    no_match  = []

    for html_file in html_files:
        html_path = os.path.join(CACHE_DIR, html_file)

        # Detect book code from first span ID
        try:
            with open(html_path, encoding="utf-8") as f:
                raw = f.read()
        except Exception as e:
            p(f"  [ERR] {html_file}: read error -- {e}")
            continue

        m = re.search(r'id="([A-Z0-9]{2,3})\.\d+\.\d+"', raw)
        if not m:
            p(f"  [SKIP] {html_file}: no verse spans found")
            no_match.append(html_file)
            continue

        book_code = m.group(1)
        json_name = BOOK_MAP.get(book_code)
        if not json_name:
            p(f"  [SKIP] {html_file}: unknown book code '{book_code}'")
            no_match.append(html_file)
            continue

        json_path   = os.path.join(ASSETS_DIR, json_name + ".json")
        exist_total = existing_verse_count(json_path)
        is_stub     = is_placeholder_json(json_path)

        # Parse Urdu verses
        try:
            chapters_dict = parse_html(html_path)
        except Exception as e:
            p(f"  [ERR] {html_file}: parse error -- {e}")
            continue

        if not chapters_dict:
            p(f"  [NO_URDU] {html_file} ({book_code}): no Urdu verses found")
            no_urdu.append(html_file)
            continue

        cache_total = sum(len(v) for v in chapters_dict.values())
        ch_count    = len(chapters_dict)

        # Update if:
        #  - file is a stub/placeholder, OR
        #  - cache has more verses than existing, OR
        #  - cache count differs from existing
        if is_stub or cache_total != exist_total:
            action   = "CREATE" if not os.path.exists(json_path) else "UPDATE"
            new_data = build_json(json_name, chapters_dict)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(new_data, f, ensure_ascii=False, indent=2)
            p(f"  [{action}] {json_name}.json  <- {html_file}  "
              f"({ch_count} ch, {cache_total} v)  was:{exist_total}")
            updated.append((json_name, ch_count, cache_total))
        else:
            p(f"  [OK]    {json_name}.json  already complete ({exist_total} v, cache:{cache_total})")
            skipped.append(json_name)

    p(f"\n{'='*65}")
    p(f"  Updated  : {len(updated)} books")
    p(f"  Skipped  : {len(skipped)} books (already up-to-date)")
    p(f"  No Urdu  : {len(no_urdu)} files (English-only or non-book)")
    p(f"  No match : {len(no_match)} files (non-book HTML)")
    p(f"{'='*65}")
    if updated:
        p("\n  Books updated:")
        total_v = 0
        for name, ch, v in updated:
            p(f"    {name:<25} {ch:>3} ch  {v:>5} verses")
            total_v += v
        p(f"\n  Total new Urdu verses written: {total_v:,}")
    log.close()

if __name__ == "__main__":
    main()

