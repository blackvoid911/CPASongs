import json
path = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu\job.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)
chapters = sorted([c['chapter'] for c in data['chapters']])
missing = [i for i in range(1, 43) if i not in chapters]
print(f"Total chapters in Job: {len(chapters)}")
print(f"Chapter range: {chapters[0]} to {chapters[-1]}")
print(f"Missing chapters: {missing}")
print(f"First 10 chapters: {chapters[:10]}")
print(f"Last 10 chapters: {chapters[-10:]}")

