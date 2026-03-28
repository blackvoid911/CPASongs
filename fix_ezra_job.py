"""
Fix specific Urdu books:
1. Ezra  - re-parse with detailed debug to find why stub content persists
2. Job   - chapter 2 is missing; fix chapter numbering
3. 3 John - 15 verses is correct for Urdu Kitab-e-Muqaddas; update canonical
"""
import re, json, os
from bs4 import BeautifulSoup

CACHE_DIR = r"C:\xampp\htdocs\cpa\cache\bible"
URDU_DIR  = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"
out = open(r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\fix_log.txt", "w", encoding="utf-8")
def p(s=""): out.write(s+"\n"); out.flush()

def is_urdu(text):
    return any('\u0600' <= c <= '\u06ff' for c in text)

# ============================================================
# FIX EZRA
# ============================================================
p("=== FIXING EZRA ===")
ezr_html = os.path.join(CACHE_DIR, "ezr.html")
with open(ezr_html, encoding="utf-8") as f:
    raw = f.read()

p(f"HTML file size: {len(raw):,} chars")
p(f"Urdu chars in file: {sum(1 for c in raw if chr(0x600)<=c<=chr(0x6ff)):,}")

soup = BeautifulSoup(raw, "html.parser")
chapters = {}
skipped_empty = 0
skipped_noturdu = 0

for span in soup.find_all("span", id=re.compile(r"^EZR\.\d+\.\d+$")):
    parts = span["id"].split(".")
    ch, vn = int(parts[1]), int(parts[2])

    # Try direct text extraction
    inner = span.find("span", class_=False)
    if inner:
        text = inner.get_text(strip=True)
    else:
        # Sometimes text is directly in the span, not in a nested span
        text = span.get_text(separator=" ", strip=True)
        text = re.sub(r"^\d+\s*", "", text).strip()

    if not text:
        skipped_empty += 1
        continue
    if not is_urdu(text):
        skipped_noturdu += 1
        continue

    # Only store if not already stored (first wins)
    chapters.setdefault(ch, {})
    if vn not in chapters[ch]:
        chapters[ch][vn] = text

total = sum(len(v) for v in chapters.values())
p(f"Parsed: {len(chapters)} chapters, {total} verses")
p(f"Skipped empty: {skipped_empty}, non-Urdu: {skipped_noturdu}")
for ch_num in sorted(chapters.keys())[:3]:
    vv = chapters[ch_num]
    p(f"  ch{ch_num}: {len(vv)} verses")
    for vn in sorted(vv.keys())[:2]:
        p(f"    v{vn}: {vv[vn][:70]}")

if total > 10:
    # Write the file
    result = {
        "book": "عزرا",
        "bookEnglish": "Ezra",
        "chapters": []
    }
    for ch_num in sorted(chapters.keys()):
        verses = [{"verse": v, "text": t} for v, t in sorted(chapters[ch_num].items())]
        result["chapters"].append({"chapter": ch_num, "verses": verses})

    out_path = os.path.join(URDU_DIR, "ezra.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    p(f"\nWrote ezra.json: {len(result['chapters'])} ch, {total} verses")
else:
    p("WARNING: Not enough verses found, skipping write")
    # Debug: show what spans ARE in the file
    all_spans = soup.find_all("span", id=re.compile(r"^[A-Z]+\.\d+\.\d+$"))
    p(f"All verse spans in file: {len(all_spans)}")
    for sp in all_spans[:5]:
        inner = sp.find("span", class_=False)
        t = inner.get_text(strip=True) if inner else sp.get_text(strip=True)
        p(f"  {sp['id']}: is_urdu={is_urdu(t)} text={t[:60]}")

p("")

# ============================================================
# FIX JOB — chapter 2 is missing (chapters jump from 1 to 3)
# ============================================================
p("=== FIXING JOB ===")
job_html = os.path.join(CACHE_DIR, "job.html")
with open(job_html, encoding="utf-8") as f:
    soup2 = BeautifulSoup(f.read(), "html.parser")

chapters2 = {}
for span in soup2.find_all("span", id=re.compile(r"^JOB\.\d+\.\d+$")):
    parts = span["id"].split(".")
    ch, vn = int(parts[1]), int(parts[2])
    inner = span.find("span", class_=False)
    text = inner.get_text(strip=True) if inner else ""
    if not text or not is_urdu(text):
        continue
    chapters2.setdefault(ch, {})
    if vn not in chapters2[ch]:
        chapters2[ch][vn] = text

total2 = sum(len(v) for v in chapters2.values())
ch_nums = sorted(chapters2.keys())
p(f"Parsed: {len(chapters2)} chapters, {total2} verses")
p(f"Chapter numbers present: {ch_nums}")
p(f"Missing chapters: {[n for n in range(1,43) if n not in ch_nums]}")

if len(chapters2) > 0:
    result2 = {
        "book": "ایوب",
        "bookEnglish": "Job",
        "chapters": []
    }
    for ch_num in sorted(chapters2.keys()):
        verses = [{"verse": v, "text": t} for v, t in sorted(chapters2[ch_num].items())]
        result2["chapters"].append({"chapter": ch_num, "verses": verses})
    out_path2 = os.path.join(URDU_DIR, "job.json")
    with open(out_path2, "w", encoding="utf-8") as f:
        json.dump(result2, f, ensure_ascii=False, indent=2)
    p(f"Wrote job.json: {len(result2['chapters'])} ch, {total2} verses")

out.close()
print("done")

