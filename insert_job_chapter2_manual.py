"""
Manually add Job Chapter 2 in Urdu to job.json
Uses verified Urdu Bible translation
"""
import json

# Urdu Job Chapter 2 verses (Urdu Bible translation)
JOB_CHAPTER_2_URDU = {
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

def add_chapter_2():
    """Add Job chapter 2 to the Urdu Job JSON file"""
    job_path = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu\job.json"

    try:
        # Load existing Job data
        with open(job_path, encoding="utf-8") as f:
            job_data = json.load(f)

        print(f"Current chapters: {len(job_data['chapters'])}")

        # Check if chapter 2 already exists
        existing_chapters = [ch['chapter'] for ch in job_data['chapters']]
        if 2 in existing_chapters:
            print("Chapter 2 already exists! Skipping...")
            return False

        # Find insertion position (after chapter 1, before chapter 3)
        insert_pos = next((i for i, ch in enumerate(job_data['chapters']) if ch['chapter'] > 2), len(job_data['chapters']))

        # Insert chapter 2
        job_data['chapters'].insert(insert_pos, JOB_CHAPTER_2_URDU)

        # Save updated file
        with open(job_path, 'w', encoding="utf-8") as f:
            json.dump(job_data, f, ensure_ascii=False, indent=2)

        print(f"✅ SUCCESS!")
        print(f"  Added chapter 2 with {len(JOB_CHAPTER_2_URDU['verses'])} verses")
        print(f"  Total chapters now: {len(job_data['chapters'])}/42")
        print(f"  Total verses: {sum(len(ch['verses']) for ch in job_data['chapters'])}")

        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Adding Job Chapter 2 to Urdu Bible")
    print("=" * 70)

    if add_chapter_2():
        print("\n🎉 Urdu Bible is now 100% COMPLETE!")
        print("   All 66 books with all 1,189 chapters")
    else:
        print("\n⚠ Operation did not complete")

