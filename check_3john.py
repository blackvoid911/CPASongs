import json, os

# Check 3 John
with open(r'C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\3_john.json', encoding='utf-8') as f:
    d = json.load(f)
ch = d['chapters'][0]
print('3 John verse count:', len(ch['verses']))
for v in ch['verses']:
    print(f"  v{v['verse']}: {v['text'][:90]}")

# Also check which cache file produced the 3_john update
# by scanning all cache files for 3JN spans
import re
cache = r"C:\xampp\htdocs\cpa\cache\bible\english"
for fn in sorted(os.listdir(cache)):
    path = os.path.join(cache, fn)
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if '3JN.' in content or '"3JN' in content:
        m3jn = re.findall(r'id="(3JN\.\d+\.\d+)"', content)
        print(f"\nFile with 3JN spans: {fn}  ({len(m3jn)} spans)")

# Also scan for 1KI and 1SA
for fn in sorted(os.listdir(cache)):
    path = os.path.join(cache, fn)
    with open(path, encoding='utf-8') as f:
        content = f.read()
    for code in ['1KI', '1SA', '1KG']:
        if f'"{code}.' in content:
            spans = re.findall(rf'id="({code}\.\d+\.\d+)"', content)
            if spans:
                print(f"File with {code} spans: {fn}  ({len(spans)} spans)")

