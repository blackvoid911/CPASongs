"""
Copy English Bible files from XAMPP cache to app assets
"""
import os
import shutil
import json
import sys

# Log to file
log_file = open(r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\copy_log.txt", "w", encoding="utf-8")

def log(msg):
    print(msg)
    log_file.write(msg + "\n")
    log_file.flush()

SOURCE_DIR = r"C:\xampp\htdocs\cpa\cache\bible\english"
DEST_DIR = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible"

def main():
    log("=" * 60)
    log("Copying English Bible from XAMPP cache")
    log("=" * 60)

    if not os.path.exists(SOURCE_DIR):
        log(f"ERROR: Source directory not found: {SOURCE_DIR}")
        # List parent directories to debug
        parent = os.path.dirname(SOURCE_DIR)
        if os.path.exists(parent):
            log(f"Parent exists: {parent}")
            log(f"Contents: {os.listdir(parent)}")
        else:
            log(f"Parent not found: {parent}")
            grandparent = os.path.dirname(parent)
            if os.path.exists(grandparent):
                log(f"Grandparent exists: {grandparent}")
                log(f"Contents: {os.listdir(grandparent)}")
        return

    os.makedirs(DEST_DIR, exist_ok=True)

    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.json')]
    log(f"Found {len(files)} JSON files")

    copied = 0
    for filename in files:
        src = os.path.join(SOURCE_DIR, filename)
        dst = os.path.join(DEST_DIR, filename)
        try:
            shutil.copy2(src, dst)
            size = os.path.getsize(dst)
            log(f"  Copied: {filename} ({size:,} bytes)")
            copied += 1
        except Exception as e:
            log(f"  Error copying {filename}: {e}")

    log(f"\nCopied {copied}/{len(files)} files")

    # Verify content of one file
    if copied > 0:
        test_file = os.path.join(DEST_DIR, files[0])
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if 'chapters' in data:
                log(f"Verified: {files[0]} has {len(data['chapters'])} chapters")

    log_file.close()

if __name__ == "__main__":
    main()


