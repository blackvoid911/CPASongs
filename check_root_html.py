import re

# Check the root gen.html to see if it has Urdu content
path = r"C:\xampp\htdocs\cpa\cache\bible\gen.html"
out = open(r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\root_html_check.txt", "w", encoding="utf-8")

with open(path, encoding="utf-8") as f:
    content = f.read()

out.write(f"File size: {len(content):,} chars\n\n")

# Find all span IDs
spans = re.findall(r'id="([A-Z0-9]+\.\d+\.\d+)"', content)
out.write(f"Total verse spans: {len(spans)}\n")
if spans:
    out.write(f"First 5: {spans[:5]}\n")
    out.write(f"Last 5:  {spans[-5:]}\n\n")

# Check for Urdu Unicode characters (U+0600–U+06FF)
urdu_chars = [c for c in content if '\u0600' <= c <= '\u06ff']
out.write(f"Urdu characters found: {len(urdu_chars)}\n\n")

# Print a sample of the HTML around GEN.1.1
idx = content.find('id="GEN.1.1"')
if idx >= 0:
    sample = content[idx:idx+600]
    out.write("=== Sample around GEN.1.1 ===\n")
    out.write(sample + "\n\n")

# Try to find a Urdu-language translation span (different class or lang attribute)
# Look for spans with Urdu text
urdu_spans = re.findall(r'<span[^>]*>([^\u0000-\u05ff\u0700-\uffff]{3,})<\/span>', content)
if urdu_spans:
    out.write(f"Possible Urdu spans: {len(urdu_spans)}\n")
    out.write(f"Sample: {urdu_spans[:3]}\n")

out.close()
print("done")

