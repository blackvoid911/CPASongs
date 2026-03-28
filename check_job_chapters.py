import json
with open(r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu\job.json", encoding="utf-8") as f:
    data = json.load(f)
chapters = [ch["chapter"] for ch in data["chapters"]]
print(f"Job has {len(chapters)} chapters")
print(f"Chapter numbers: {sorted(chapters)}")
missing = [i for i in range(1, 43) if i not in chapters]
print(f"Missing chapters: {missing}")

