"""Quick check and fix for Urdu Bible completion"""
import json
import os

URDU = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"

print("Checking Job...")
job_file = os.path.join(URDU, "job.json")

if os.path.exists(job_file):
    with open(job_file, 'r', encoding='utf-8') as f:
        job = json.load(f)

    chapters = [c['chapter'] for c in job['chapters']]
    print(f"  Current chapters: {len(chapters)}")
    print(f"  Has chapter 2: {2 in chapters}")

    if 2 not in chapters:
        print("  -> Adding chapter 2...")

        ch2 = {
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

        # Find position
        pos = next((i for i, c in enumerate(job['chapters']) if c['chapter'] > 2), len(job['chapters']))
        job['chapters'].insert(pos, ch2)

        # Save
        with open(job_file, 'w', encoding='utf-8') as f:
            json.dump(job, f, ensure_ascii=False, indent=2)

        print("  ✓ Chapter 2 added!")
        print(f"  -> Now has {len(job['chapters'])} chapters")
    else:
        print("  ✓ Chapter 2 already exists")

    # Final count
    total_verses = sum(len(c['verses']) for c in job['chapters'])
    print(f"  -> Total: {len(job['chapters'])} chapters, {total_verses} verses")

    # Write report
    with open("urdu_bible_status.txt", 'w', encoding='utf-8') as f:
        f.write(f"Urdu Bible Status Report\n")
        f.write(f"========================\n\n")
        f.write(f"Job: {len(job['chapters'])}/42 chapters, {total_verses} verses\n")
        f.write(f"Chapter 2 present: {2 in [c['chapter'] for c in job['chapters']]}\n")
        f.write(f"\nCache location: C:\\xampp\\htdocs\\cpa\\cache\\bible\n")
        f.write(f"Output location: {URDU}\n")

    print("\n✓ Report saved to: urdu_bible_status.txt")

else:
    print(f"ERROR: Job file not found at {job_file}")

print("\nDone!")

