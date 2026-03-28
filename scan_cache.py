import os

cache_root = r"C:\xampp\htdocs\cpa\cache\bible"
out = open(r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\cache_structure.txt", "w", encoding="utf-8")

for root, dirs, files in os.walk(cache_root):
    level = root.replace(cache_root, "").count(os.sep)
    indent = "  " * level
    rel = root.replace(cache_root, "").lstrip(os.sep) or "(root)"
    out.write(f"{indent}[{rel}]  ({len(files)} files)\n")
    for f in sorted(files):
        size = os.path.getsize(os.path.join(root, f))
        out.write(f"{indent}  {f}  ({size:,} bytes)\n")

out.close()
print("done")

