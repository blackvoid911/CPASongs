import json, os

urdu_dir = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"
out = open(r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\urdu_spot_check.txt", "w", encoding="utf-8")

def check(fn):
    path = os.path.join(urdu_dir, fn)
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    chapters = d.get("chapters", [])
    verse_counts = [len(ch.get("verses", [])) for ch in chapters]
    total = sum(verse_counts)
    max_vc = max(verse_counts) if verse_counts else 0
    # show first 10 chapter counts
    out.write(f"\n{fn}: {len(chapters)} chapters, {total} total verses, max_per_ch={max_vc}\n")
    out.write(f"  Per-chapter (first 10): {verse_counts[:10]}\n")
    if total > 0 and max_vc > 1:
        # show a sample verse from first chapter with >1 verse
        for i, ch in enumerate(chapters):
            vv = ch.get("verses", [])
            if len(vv) > 1:
                out.write(f"  ch{i+1} sample v1: {vv[0]['text'][:80]}\n")
                break

for fn in ["isaiah.json", "psalms.json", "proverbs.json", "ecclesiastes.json",
           "esther.json", "songofsolomon.json"]:
    check(fn)

out.close()
print("done")

