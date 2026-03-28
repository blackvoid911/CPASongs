import json, os, re
from bs4 import BeautifulSoup

out = open(r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\fix_investigation.txt", "w", encoding="utf-8")
def p(s=""): out.write(s+"\n"); out.flush()

urdu_dir = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"

# --- Check Ezra ---
ezra_path = os.path.join(urdu_dir, "ezra.json")
with open(ezra_path, encoding="utf-8") as f:
    d = json.load(f)
chapters = d.get("chapters", [])
total = sum(len(ch.get("verses",[])) for ch in chapters)
p(f"EZRA: {len(chapters)} chapters, {total} total verses")
for i, ch in enumerate(chapters[:3]):
    vv = ch.get("verses",[])
    p(f"  ch{ch['chapter']}: {len(vv)} verses")
    for v in vv[:2]:
        p(f"    v{v['verse']}: {v['text'][:80]}")

p("")

# --- Check Job ---
job_path = os.path.join(urdu_dir, "job.json")
with open(job_path, encoding="utf-8") as f:
    d = json.load(f)
chapters = d.get("chapters", [])
total = sum(len(ch.get("verses",[])) for ch in chapters)
p(f"JOB: {len(chapters)} chapters, {total} total verses")
# Show chapter numbers present
ch_nums = [ch["chapter"] for ch in chapters]
p(f"  Chapter numbers: {ch_nums}")
p(f"  Missing: {[n for n in range(1,43) if n not in ch_nums]}")

p("")

# --- Verify 3 John ---
jn3_path = os.path.join(urdu_dir, "3john.json")
with open(jn3_path, encoding="utf-8") as f:
    d = json.load(f)
ch = d["chapters"][0]
p(f"3 JOHN: {len(ch['verses'])} verses")
for v in ch["verses"]:
    p(f"  v{v['verse']}: {v['text'][:80]}")

p("")

# --- Re-check Ezra from cache HTML ---
ezr_html = r"C:\xampp\htdocs\cpa\cache\bible\ezr.html"
with open(ezr_html, encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")
spans = soup.find_all("span", id=re.compile(r"^[A-Z0-9]+\.\d+\.\d+$"))
p(f"EZRA HTML spans: {len(spans)}")
for sp in spans[:3]:
    ts = sp.find("span", class_=False)
    text = ts.get_text(strip=True) if ts else ""
    p(f"  {sp['id']}: {text[:80]}")
# Check if Urdu
urdu_count = sum(1 for sp in spans
    if any('\u0600'<=c<='\u06ff' for c in (sp.find("span",class_=False) or sp).get_text()))
p(f"  Spans with Urdu text: {urdu_count}")

out.close()
print("done")

