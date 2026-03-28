import os
cache = r"C:\xampp\htdocs\cpa\cache\bible\english"
files = sorted(os.listdir(cache))
print(f"Total files: {len(files)}")
for f in files:
    size = os.path.getsize(os.path.join(cache, f))
    print(f"  {f}  ({size} bytes)")

