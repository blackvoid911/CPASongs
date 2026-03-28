"""
Extract per-chapter verse counts from English Bible JSON files
to fix the canonical reference in check_bible_verses.py.
Also prints the grand total verse count.
"""
import json, os, sys

ASSETS_DIR = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible"
OUT = open(r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\counts_out.txt", "w", encoding="utf-8")
def p(s=""): OUT.write(s + "\n"); OUT.flush()

books_to_check = [
    "matthew.json", "isaiah.json", "ezekiel.json",
    "proverbs.json", "psalms.json", "3_john.json", "romans.json"
]

grand_total = 0
for fn in sorted(os.listdir(ASSETS_DIR)):
    if not fn.endswith(".json") or fn in ("index.json",):
        continue
    path = os.path.join(ASSETS_DIR, fn)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    chapters = data.get("chapters", [])
    v = sum(len(ch.get("verses", [])) for ch in chapters)
    grand_total += v
    if fn in books_to_check:
        counts = [len(ch.get("verses", [])) for ch in chapters]
        p(f"\n{fn}: {len(chapters)} chapters, {v} total verses")
        p(f"  Per-chapter: {counts}")

p(f"\n{'='*50}")
p(f"  ENGLISH BIBLE TOTAL VERSES: {grand_total:,}")
p(f"  KJV FULL BIBLE TARGET:       31,102")
p(f"  DIFFERENCE:                  {grand_total - 31102:+d}")
p(f"{'='*50}")
OUT.close()



