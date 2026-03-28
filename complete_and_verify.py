"""
Complete the Urdu Bible by fixing Job chapter 2 and verifying all books.
"""
import json
import os

URDU_DIR = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"

# Job Chapter 2 in Urdu
JOB_CH2 = {
    "chapter": 2,
    "verses": [
        {"verse": 1, "text": "پھر ایک دِن خُدا کے بیٹے آئے کہ خُداوند کے حضُور حاضِر ہوں اور اُن کے درمِیان شَیطان بھی آیا کہ خُداوند کے حضُور حاضِر ہو۔"},
        {"verse": 2, "text": "خُداوند نے شَیطان سے کہا تُو کہاں سے آتا ہے؟ شَیطان نے خُداوند کو جواب دِیا کہ زمِین میں اِدھر اُدھر پھِرتے اور اُس میں چلتے پھرتے آیا ہُوں۔"},
        {"verse": 3, "text": "خُداوند نے شَیطان سے کہا کیا تُو نے میرے بندہ ایُّوبؔ کے حال پر بھی کُچھ غَور کِیا؟ کیونکہ زمِین پر اُس کی طرح کامِل اور راست باز آدمی جو خُدا سے ڈرتا اور بدی سے دُور رہتا ہو کوئی نہیں اور اگرچہ تُو نے مُجھے اُبھارا کہ بے سبب اُسے تباہ کرُوں توبھی وہ اپنی راست بازی پر قائِم ہے۔"},
        {"verse": 4, "text": "شَیطان نے خُداوند کو جواب دِیا کہ کھال کے بدلے کھال اور سب کُچھ جو آدمی کا ہے وہ اپنی جان کے بدلے دے گا۔"},
        {"verse": 5, "text": "لیکن ذرا اپنا ہاتھ بڑھا کر اُس کی ہڈی اور گوشت کو چُھو تو کیا وہ تیرے مُنہ پر تیری تکفِیر نہ کرے گا؟"},
        {"verse": 6, "text": "خُداوند نے شَیطان سے کہا دیکھ وہ تیرے اِختیار میں ہے لیکِن اُس کی جان بچائے رکھنا۔"},
        {"verse": 7, "text": "تب شَیطان خُداوند کے حضُور سے نِکلا اور ایُّوبؔ کو پاؤں کے تلووں سے لے کر چانِدی تک دُکھتے پھوڑوں سے دُکھی کِیا۔"},
        {"verse": 8, "text": "اور اُس نے ایک ٹھِیکرا لِیا کہ اُس سے اپنے آپ کو کُھرچے اور راکھ میں جا بَیٹھا۔"},
        {"verse": 9, "text": "تب اُس کی بِیوی نے اُس سے کہا تُو اب بھی اپنی راست بازی پر قائِم ہے؟ خُدا کی تکفِیر کر اور مر جا۔"},
        {"verse": 10, "text": "اُس نے اُس سے کہا تُو بےوقُوف عَورتوں کی طرح کی باتیں کرتی ہے۔ کیا ہم جو خُدا کے ہاتھ سے اچھّا پاتے ہیں بُرا نہ پائیں؟ اِن سب باتوں میں ایُّوبؔ نے اپنے ہونٹوں سے گُناہ نہیں کِیا۔"},
        {"verse": 11, "text": "جب ایُّوبؔ کے تِین دوستوں نے یعنی تیمانی اِلی فزؔ اور سُوخی بِلددؔ اور نعماتی ضُوفرؔ نے اُس کی یہ ساری مُصِیبت سُنی تو ہر ایک اپنی جگہ سے آیا اور اُنہوں نے آپس میں صلاح کی کہ ہم اُس سے تعزِیَت کرنے اور اُسے تسلّی دینے جائیں۔"},
        {"verse": 12, "text": "اور جب اُنہوں نے دُور سے نظر اُٹھا کر اُسے دیکھا اور پہچانا نہیں تو اُنہوں نے چِلّا کر رونا شُرُوع کِیا اور ہر ایک نے اپنا چوغہ چاک کِیا اور آسمان کی طرف خاک اُڑائی اور اُسے اپنے سِروں پر ڈالا۔"},
        {"verse": 13, "text": "اور سات دِن اور سات رات اُس کے ساتھ زمِین پر بَیٹھے رہے اور کِسی نے اُس سے ایک بات بھی نہ کہی کیونکہ اُنہوں نے دیکھا کہ اُس کا دُکھ بُہت بڑا ہے۔"}
    ]
}

def fix_job():
    """Add missing chapter 2 to Job"""
    job_path = os.path.join(URDU_DIR, "job.json")

    if not os.path.exists(job_path):
        print(f"ERROR: Job file not found at {job_path}")
        return False

    with open(job_path, encoding="utf-8") as f:
        data = json.load(f)

    chapters = [ch["chapter"] for ch in data["chapters"]]

    if 2 in chapters:
        print("Job chapter 2 already exists")
        return True

    # Insert chapter 2 in the right position
    insert_pos = next((i for i, ch in enumerate(data["chapters"]) if ch["chapter"] > 2), len(data["chapters"]))
    data["chapters"].insert(insert_pos, JOB_CH2)

    # Save
    with open(job_path, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✓ Added Job chapter 2 (13 verses)")
    return True

def verify_bible():
    """Verify all 66 books"""
    EXPECTED = {
        "genesis": 50, "exodus": 40, "leviticus": 27, "numbers": 36, "deuteronomy": 34,
        "joshua": 24, "judges": 21, "ruth": 4, "1samuel": 31, "2samuel": 24,
        "1kings": 22, "2kings": 25, "1chronicles": 29, "2chronicles": 36, "ezra": 10,
        "nehemiah": 13, "esther": 10, "job": 42, "psalms": 150, "proverbs": 31,
        "ecclesiastes": 12, "songofsolomon": 8, "isaiah": 66, "jeremiah": 52, "lamentations": 5,
        "ezekiel": 48, "daniel": 12, "hosea": 14, "joel": 3, "amos": 9,
        "obadiah": 1, "jonah": 4, "micah": 7, "nahum": 3, "habakkuk": 3,
        "zephaniah": 3, "haggai": 2, "zechariah": 14, "malachi": 4,
        "matthew": 28, "mark": 16, "luke": 24, "john": 21, "acts": 28,
        "romans": 16, "1corinthians": 16, "2corinthians": 13, "galatians": 6, "ephesians": 6,
        "philippians": 4, "colossians": 4, "1thessalonians": 5, "2thessalonians": 3,
        "1timothy": 6, "2timothy": 4, "titus": 3, "philemon": 1, "hebrews": 13,
        "james": 5, "1peter": 5, "2peter": 3, "1john": 5, "2john": 1,
        "3john": 1, "jude": 1, "revelation": 22
    }

    complete = 0
    incomplete = []
    total_verses = 0

    for book, expected in EXPECTED.items():
        path = os.path.join(URDU_DIR, f"{book}.json")

        if not os.path.exists(path):
            incomplete.append(book)
            continue

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        actual = len(data.get("chapters", []))
        verses = sum(len(ch.get("verses", [])) for ch in data.get("chapters", []))
        total_verses += verses

        if actual == expected and verses > 0:
            complete += 1
        else:
            incomplete.append(f"{book} ({actual}/{expected})")

    print(f"\n{'='*70}")
    print(f"VERIFICATION RESULTS")
    print(f"{'='*70}")
    print(f"Complete books: {complete}/66")
    print(f"Total verses: {total_verses:,}")

    if incomplete:
        print(f"\nIncomplete: {', '.join(incomplete)}")
        return False
    else:
        print("\n🎉 ALL 66 BOOKS COMPLETE!")
        return True

if __name__ == "__main__":
    print("="*70)
    print("Completing Urdu Bible")
    print("="*70)

    if fix_job():
        verify_bible()

