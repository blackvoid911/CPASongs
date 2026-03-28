"""
Complete Urdu Bible books with all chapters containing key verses.
Uses Urdu Bible translations for key verses.
"""

import json
import os

# Urdu Bible book information with correct chapter counts
URDU_BOOKS = [
    {"name": "Genesis", "nameUrdu": "پیدائش", "file": "genesis.json", "chapters": 50},
    {"name": "Exodus", "nameUrdu": "خُروج", "file": "exodus.json", "chapters": 40},
    {"name": "Leviticus", "nameUrdu": "احبار", "file": "leviticus.json", "chapters": 27},
    {"name": "Numbers", "nameUrdu": "گنتی", "file": "numbers.json", "chapters": 36},
    {"name": "Deuteronomy", "nameUrdu": "اِستِثنا", "file": "deuteronomy.json", "chapters": 34},
    {"name": "Joshua", "nameUrdu": "یشُوع", "file": "joshua.json", "chapters": 24},
    {"name": "Judges", "nameUrdu": "قُضاۃ", "file": "judges.json", "chapters": 21},
    {"name": "Ruth", "nameUrdu": "رُوت", "file": "ruth.json", "chapters": 4},
    {"name": "1 Samuel", "nameUrdu": "۱-سموئیل", "file": "1samuel.json", "chapters": 31},
    {"name": "2 Samuel", "nameUrdu": "۲-سموئیل", "file": "2samuel.json", "chapters": 24},
    {"name": "1 Kings", "nameUrdu": "۱-سلاطین", "file": "1kings.json", "chapters": 22},
    {"name": "2 Kings", "nameUrdu": "۲-سلاطین", "file": "2kings.json", "chapters": 25},
    {"name": "1 Chronicles", "nameUrdu": "۱-تواریخ", "file": "1chronicles.json", "chapters": 29},
    {"name": "2 Chronicles", "nameUrdu": "۲-تواریخ", "file": "2chronicles.json", "chapters": 36},
    {"name": "Ezra", "nameUrdu": "عزرا", "file": "ezra.json", "chapters": 10},
    {"name": "Nehemiah", "nameUrdu": "نحمیاہ", "file": "nehemiah.json", "chapters": 13},
    {"name": "Esther", "nameUrdu": "آستر", "file": "esther.json", "chapters": 10},
    {"name": "Job", "nameUrdu": "ایّوب", "file": "job.json", "chapters": 42},
    {"name": "Psalms", "nameUrdu": "زبُور", "file": "psalms.json", "chapters": 150},
    {"name": "Proverbs", "nameUrdu": "امثال", "file": "proverbs.json", "chapters": 31},
    {"name": "Ecclesiastes", "nameUrdu": "واعظ", "file": "ecclesiastes.json", "chapters": 12},
    {"name": "Song of Solomon", "nameUrdu": "غزل الغزلات", "file": "songofsolomon.json", "chapters": 8},
    {"name": "Isaiah", "nameUrdu": "یسعیاہ", "file": "isaiah.json", "chapters": 66},
    {"name": "Jeremiah", "nameUrdu": "یرمیاہ", "file": "jeremiah.json", "chapters": 52},
    {"name": "Lamentations", "nameUrdu": "نوحہ", "file": "lamentations.json", "chapters": 5},
    {"name": "Ezekiel", "nameUrdu": "حزقی ایل", "file": "ezekiel.json", "chapters": 48},
    {"name": "Daniel", "nameUrdu": "دانی ایل", "file": "daniel.json", "chapters": 12},
    {"name": "Hosea", "nameUrdu": "ہوسیع", "file": "hosea.json", "chapters": 14},
    {"name": "Joel", "nameUrdu": "یوایل", "file": "joel.json", "chapters": 3},
    {"name": "Amos", "nameUrdu": "عاموس", "file": "amos.json", "chapters": 9},
    {"name": "Obadiah", "nameUrdu": "عبدیاہ", "file": "obadiah.json", "chapters": 1},
    {"name": "Jonah", "nameUrdu": "یُوناہ", "file": "jonah.json", "chapters": 4},
    {"name": "Micah", "nameUrdu": "میکاہ", "file": "micah.json", "chapters": 7},
    {"name": "Nahum", "nameUrdu": "ناحُوم", "file": "nahum.json", "chapters": 3},
    {"name": "Habakkuk", "nameUrdu": "حبقُّوق", "file": "habakkuk.json", "chapters": 3},
    {"name": "Zephaniah", "nameUrdu": "صفنیاہ", "file": "zephaniah.json", "chapters": 3},
    {"name": "Haggai", "nameUrdu": "حجّی", "file": "haggai.json", "chapters": 2},
    {"name": "Zechariah", "nameUrdu": "زکریاہ", "file": "zechariah.json", "chapters": 14},
    {"name": "Malachi", "nameUrdu": "ملاکی", "file": "malachi.json", "chapters": 4},
    {"name": "Matthew", "nameUrdu": "متّی", "file": "matthew.json", "chapters": 28},
    {"name": "Mark", "nameUrdu": "مرقس", "file": "mark.json", "chapters": 16},
    {"name": "Luke", "nameUrdu": "لُوقا", "file": "luke.json", "chapters": 24},
    {"name": "John", "nameUrdu": "یُوحنّا", "file": "john.json", "chapters": 21},
    {"name": "Acts", "nameUrdu": "اعمال", "file": "acts.json", "chapters": 28},
    {"name": "Romans", "nameUrdu": "رومیوں", "file": "romans.json", "chapters": 16},
    {"name": "1 Corinthians", "nameUrdu": "۱-کُرنتھیوں", "file": "1corinthians.json", "chapters": 16},
    {"name": "2 Corinthians", "nameUrdu": "۲-کُرنتھیوں", "file": "2corinthians.json", "chapters": 13},
    {"name": "Galatians", "nameUrdu": "گلتیوں", "file": "galatians.json", "chapters": 6},
    {"name": "Ephesians", "nameUrdu": "اِفسیوں", "file": "ephesians.json", "chapters": 6},
    {"name": "Philippians", "nameUrdu": "فِلپّیوں", "file": "philippians.json", "chapters": 4},
    {"name": "Colossians", "nameUrdu": "کُلسّیوں", "file": "colossians.json", "chapters": 4},
    {"name": "1 Thessalonians", "nameUrdu": "۱-تھسّلُنیکیوں", "file": "1thessalonians.json", "chapters": 5},
    {"name": "2 Thessalonians", "nameUrdu": "۲-تھسّلُنیکیوں", "file": "2thessalonians.json", "chapters": 3},
    {"name": "1 Timothy", "nameUrdu": "۱-تیمُتھیُس", "file": "1timothy.json", "chapters": 6},
    {"name": "2 Timothy", "nameUrdu": "۲-تیمُتھیُس", "file": "2timothy.json", "chapters": 4},
    {"name": "Titus", "nameUrdu": "طِطُس", "file": "titus.json", "chapters": 3},
    {"name": "Philemon", "nameUrdu": "فِلیمون", "file": "philemon.json", "chapters": 1},
    {"name": "Hebrews", "nameUrdu": "عبرانیوں", "file": "hebrews.json", "chapters": 13},
    {"name": "James", "nameUrdu": "یعقُوب", "file": "james.json", "chapters": 5},
    {"name": "1 Peter", "nameUrdu": "۱-پطرس", "file": "1peter.json", "chapters": 5},
    {"name": "2 Peter", "nameUrdu": "۲-پطرس", "file": "2peter.json", "chapters": 3},
    {"name": "1 John", "nameUrdu": "۱-یُوحنّا", "file": "1john.json", "chapters": 5},
    {"name": "2 John", "nameUrdu": "۲-یُوحنّا", "file": "2john.json", "chapters": 1},
    {"name": "3 John", "nameUrdu": "۳-یُوحنّا", "file": "3john.json", "chapters": 1},
    {"name": "Jude", "nameUrdu": "یہُوداہ", "file": "jude.json", "chapters": 1},
    {"name": "Revelation", "nameUrdu": "مکاشفہ", "file": "revelation.json", "chapters": 22},
]

# Key Urdu Bible verses for important chapters
URDU_KEY_VERSES = {
    "Genesis": {
        1: [{"verse": 1, "text": "ابتدا میں خُدا نے آسمان اور زمین کو پیدا کیا۔"},
            {"verse": 27, "text": "اور خُدا نے انسان کو اپنی صُورت پر پیدا کیا۔ خُدا کی صُورت پر اُس کو پیدا کیا۔ نر و ناری اُن کو پیدا کیا۔"},
            {"verse": 31, "text": "اور خُدا نے سب کچھ جو اُس نے بنایا تھا دیکھا اور دیکھو وہ بہت اچھا تھا۔"}],
        2: [{"verse": 7, "text": "اور خُداوند خُدا نے آدم کو زمین کی مٹی سے بنایا اور اُس کے نتھنوں میں زندگی کا دم پھونکا۔ تب آدم جیتی جان ہُوا۔"},
            {"verse": 18, "text": "پھر خُداوند خُدا نے کہا کہ آدم کا اکیلا رہنا اچھا نہیں۔ میں اُس کے لیے ایک مددگار بناؤں گا۔"}],
        3: [{"verse": 15, "text": "اور میں تیرے اور عورت کے درمیان اور تیری نسل اور اُس کی نسل کے درمیان عداوت ڈالوں گا۔ وہ تیرے سر کو کُچلے گا اور تُو اُس کی ایڑی پر کاٹے گا۔"}],
    },
    "Psalms": {
        1: [{"verse": 1, "text": "مُبارک ہے وہ آدمی جو شریروں کی صلاح پر نہیں چلتا اور نہ گنہگاروں کی راہ میں کھڑا ہوتا ہے اور نہ ٹھٹھا کرنے والوں کی مجلس میں بیٹھتا ہے۔"},
            {"verse": 2, "text": "بلکہ خُداوند کی شریعت میں اُس کی خوشی ہے اور رات دن اُسی کی شریعت پر دھیان کرتا ہے۔"}],
        23: [{"verse": 1, "text": "خُداوند میرا چوپان ہے۔ مجھے کچھ کمی نہ ہوگی۔"},
             {"verse": 2, "text": "وہ مجھے ہری چراگاہوں میں بٹھاتا ہے۔ وہ مجھے سکون کے چشموں کے پاس لے جاتا ہے۔"},
             {"verse": 4, "text": "بلکہ اگر میں موت کے سایہ کی وادی میں سے گزروں بھی تو کسی بلا سے نہ ڈروں گا کیونکہ تُو میرے ساتھ ہے۔"}],
        27: [{"verse": 1, "text": "خُداوند میری روشنی اور میری نجات ہے۔ میں کس سے ڈروں؟ خُداوند میری زندگی کا قلعہ ہے۔ میں کس کا خوف کروں؟"}],
        46: [{"verse": 1, "text": "خُدا ہماری پناہ اور قوت ہے۔ مصیبت میں وہ ہمارا بڑا مددگار ٹھہرا۔"},
             {"verse": 10, "text": "تھم جاؤ اور جان لو کہ میں خُدا ہوں۔"}],
        91: [{"verse": 1, "text": "جو حق تعالیٰ کے پردہ میں رہتا ہے وہ قادرِ مُطلق کے سایہ تلے بسیرا کرے گا۔"},
             {"verse": 2, "text": "میں خُداوند کی بابت کہوں گا کہ وہ میری پناہ گاہ اور میرا قلعہ ہے۔ میرا خُدا ہے جس پر میں توکل کرتا ہوں۔"}],
        103: [{"verse": 1, "text": "اے میری جان! خُداوند کو مُبارک کہہ بلکہ میرا سارا وجود اُس کے نامِ قُدوس کو مُبارک کہے۔"},
              {"verse": 12, "text": "جتنا پُورب پچھم سے دُور ہے اُتنا ہی اُس نے ہماری خطاؤں کو ہم سے دُور کر دیا۔"}],
        119: [{"verse": 105, "text": "تیرا کلام میرے قدموں کے لیے چراغ اور میری راہ کے لیے روشنی ہے۔"}],
        121: [{"verse": 1, "text": "میں پہاڑوں کی طرف اپنی آنکھیں اُٹھاتا ہوں۔ میری مدد کہاں سے آئے گی؟"},
              {"verse": 2, "text": "میری مدد خُداوند کی طرف سے ہے جس نے آسمان اور زمین کو بنایا۔"}],
        139: [{"verse": 14, "text": "میں تیرا شکر کروں گا کیونکہ میں عجیب اور حیرت انگیز طور پر بنایا گیا ہوں۔"}],
        150: [{"verse": 6, "text": "ہر ایک جاندار خُداوند کی حمد کرے۔ ہللویاہ!"}],
    },
    "Proverbs": {
        1: [{"verse": 7, "text": "خُداوند کا خوف حکمت کا شروع ہے لیکن نادان حکمت اور تربیت کو حقیر جانتے ہیں۔"}],
        3: [{"verse": 5, "text": "سارے دل سے خُداوند پر توکل کر اور اپنی سمجھ پر تکیہ نہ کر۔"},
            {"verse": 6, "text": "اپنی سب راہوں میں اُس کو پہچان اور وہ تیری راہنمائی کرے گا۔"}],
    },
    "Isaiah": {
        40: [{"verse": 31, "text": "لیکن جو خُداوند کے منتظر ہیں وہ نئی قوت حاصل کریں گے۔ وہ عُقاب کی مانند پروں سے اُڑیں گے۔ وہ دوڑیں گے اور نہ تھکیں گے۔ وہ چلیں گے اور ماندے نہ ہوں گے۔"}],
        41: [{"verse": 10, "text": "تُو مت ڈر کیونکہ میں تیرے ساتھ ہوں۔ تُو ہراساں نہ ہو کیونکہ میں تیرا خُدا ہوں۔ میں تجھے زور بخشوں گا۔ میں تیری مدد کروں گا۔"}],
        53: [{"verse": 5, "text": "حالانکہ وہ ہماری خطاؤں کے سبب سے گھایل کیا گیا اور ہماری بدکاری کے باعث کُچلا گیا۔ ہماری سلامتی کی تنبیہ اُس پر ہوئی تاکہ اُس کے مار کھانے سے ہم شفا پائیں۔"}],
    },
    "Jeremiah": {
        29: [{"verse": 11, "text": "کیونکہ میں اُن ارادوں کو جانتا ہوں جو میرے دل میں تمہارے لیے ہیں۔ خُداوند فرماتا ہے۔ سلامتی کے ارادے نہ کہ بدی کے تاکہ تمہیں اُمید کا انجام دوں۔"}],
    },
    "Matthew": {
        5: [{"verse": 3, "text": "مُبارک ہیں وہ جو دل کے غریب ہیں کیونکہ آسمان کی بادشاہی اُنہی کی ہے۔"},
            {"verse": 14, "text": "تُم دُنیا کے نور ہو۔ جو شہر پہاڑ پر بسا ہے وہ چھپ نہیں سکتا۔"},
            {"verse": 44, "text": "لیکن میں تم سے کہتا ہوں کہ اپنے دشمنوں سے محبت رکھو۔"}],
        6: [{"verse": 33, "text": "پہلے تُم خُدا کی بادشاہی اور اُس کی راستبازی کی تلاش کرو تو یہ سب چیزیں بھی تمہیں مل جائیں گی۔"}],
        11: [{"verse": 28, "text": "اے تھکے ہارے اور بوجھ سے دبے ہوئے لوگو! میرے پاس آؤ میں تمہیں آرام دوں گا۔"},
             {"verse": 29, "text": "میرا جُوا اپنے اُوپر اُٹھا لو اور مجھ سے سیکھو کیونکہ میں حلیم ہوں اور دل کا فروتن ہوں۔"}],
        28: [{"verse": 19, "text": "پس تُم جاؤ اور سب قوموں کو شاگرد بناؤ اور اُن کو باپ اور بیٹے اور روح القدس کے نام سے بپتسمہ دو۔"},
             {"verse": 20, "text": "اور اُن کو یہ سب باتیں جو میں نے تمہیں حکم دیں ہیں ماننا سکھاؤ۔ دیکھو میں دُنیا کے آخر تک ہمیشہ تمہارے ساتھ ہوں۔"}],
    },
    "John": {
        1: [{"verse": 1, "text": "ابتدا میں کلام تھا اور کلام خُدا کے ساتھ تھا اور کلام خُدا تھا۔"},
            {"verse": 12, "text": "لیکن جتنوں نے اُسے قبول کیا اُس نے اُن کو خُدا کے فرزند بننے کا حق بخشا یعنی اُن کو جو اُس کے نام پر ایمان لاتے ہیں۔"},
            {"verse": 14, "text": "اور کلام مجسم ہُوا اور فضل اور سچائی سے معمور ہو کر ہمارے درمیان رہا۔"}],
        3: [{"verse": 16, "text": "کیونکہ خُدا نے دُنیا سے ایسی محبت رکھی کہ اُس نے اپنا اکلوتا بیٹا بخش دیا تاکہ جو کوئی اُس پر ایمان لائے ہلاک نہ ہو بلکہ ہمیشہ کی زندگی پائے۔"}],
        14: [{"verse": 6, "text": "یسوع نے اُس سے کہا راہ اور حق اور زندگی میں ہوں۔ کوئی میرے وسیلہ کے بغیر باپ کے پاس نہیں آتا۔"},
             {"verse": 27, "text": "میں تمہیں سلامتی دے کر جاتا ہوں۔ اپنی سلامتی تمہیں دیتا ہوں۔ جیسی دُنیا دیتی ہے میں تمہیں اُس طرح نہیں دیتا۔ تمہارا دل نہ گھبرائے اور نہ ڈرے۔"}],
    },
    "Romans": {
        3: [{"verse": 23, "text": "اس لیے کہ سب نے گناہ کیا اور خُدا کے جلال سے محروم ہیں۔"}],
        5: [{"verse": 8, "text": "لیکن خُدا اپنی محبت کی خوبی ہم پر یوں ظاہر کرتا ہے کہ جب ہم گنہگار ہی تھے تو مسیح ہماری خاطر مُوا۔"}],
        6: [{"verse": 23, "text": "کیونکہ گناہ کی مزدوری موت ہے مگر خُدا کی بخشش ہمارے خُداوند مسیح یسوع میں ہمیشہ کی زندگی ہے۔"}],
        8: [{"verse": 1, "text": "پس اب جو مسیح یسوع میں ہیں اُن پر سزا کا حکم نہیں۔"},
            {"verse": 28, "text": "اور ہم کو معلوم ہے کہ سب چیزیں مل کر خُدا سے محبت رکھنے والوں کے لیے بھلائی پیدا کرتی ہیں۔"},
            {"verse": 31, "text": "پس ہم اِن باتوں کی بابت کیا کہیں؟ اگر خُدا ہماری طرف ہے تو کون ہمارا مخالف ہے؟"},
            {"verse": 38, "text": "کیونکہ مجھے یقین ہے کہ نہ موت نہ زندگی نہ فرشتے نہ حکومتیں نہ موجودہ باتیں نہ آنے والی باتیں نہ قدرتیں۔"},
            {"verse": 39, "text": "نہ بلندی نہ پستی نہ کوئی اور مخلوق ہم کو خُدا کی اُس محبت سے جُدا کر سکے گی جو ہمارے خُداوند مسیح یسوع میں ہے۔"}],
    },
    "Philippians": {
        4: [{"verse": 6, "text": "کسی بات کی فکر نہ کرو بلکہ ہر ایک بات میں تمہاری درخواستیں دُعا اور مناجات کے وسیلہ سے شکرگزاری کے ساتھ خُدا کو معلوم ہوں۔"},
            {"verse": 7, "text": "تو خُدا کا اطمینان جو سمجھ سے بالا تر ہے تمہارے دلوں اور خیالوں کو مسیح یسوع میں محفوظ رکھے گا۔"},
            {"verse": 13, "text": "جو مجھے طاقت بخشتا ہے اُس میں میں سب کچھ کر سکتا ہوں۔"}],
    },
    "Hebrews": {
        11: [{"verse": 1, "text": "اب ایمان اُمید کی ہوئی چیزوں کا اعتماد اور اندیکھی چیزوں کی دلیل ہے۔"},
             {"verse": 6, "text": "اور بغیر ایمان کے اُس کو پسند آنا ناممکن ہے کیونکہ خُدا کے پاس آنے والے کو ایمان لانا چاہیے کہ وہ موجود ہے۔"}],
        12: [{"verse": 1, "text": "پس جب گواہوں کا ایسا بڑا بادل ہم کو گھیرے ہوئے ہے تو آؤ ہم بھی ہر طرح کے بوجھ کو اور اُس گناہ کو جو ہمیں آسانی سے اُلجھا لیتا ہے دُور کر کے۔"},
             {"verse": 2, "text": "اور ایمان کے بانی اور کامل کرنے والے یسوع کو دیکھتے ہوئے صبر سے اُس دوڑ میں دوڑیں جو ہمارے آگے ہے۔"}],
    },
    "Revelation": {
        1: [{"verse": 8, "text": "خُداوند خُدا جو ہے اور جو تھا اور جو آنے والا ہے یعنی قادرِ مُطلق فرماتا ہے کہ میں الفا اور اومیگا ہوں۔"}],
        21: [{"verse": 4, "text": "اور وہ اُن کی آنکھوں کے سب آنسو پونچھ دے گا۔ اب نہ موت رہے گی نہ ماتم نہ آہ و نالہ نہ درد۔"}],
        22: [{"verse": 20, "text": "جو اِن باتوں کی گواہی دیتا ہے وہ فرماتا ہے ہاں میں جلد آنے والا ہوں۔ آمین! اے خُداوند یسوع آ۔"}],
    },
}


def generate_urdu_chapter(book_name, chapter_num):
    """Generate a placeholder verse for chapters without specific verses"""
    return [{"verse": 1, "text": f"باب {chapter_num}"}]


def main():
    output_dir = r"C:\Users\WelCome\AndroidStudioProjects\CPASongs\app\src\main\assets\bible\urdu"

    for book in URDU_BOOKS:
        book_name = book["name"]
        book_name_urdu = book["nameUrdu"]
        file_name = book["file"]
        total_chapters = book["chapters"]

        file_path = os.path.join(output_dir, file_name)

        # Read existing file to preserve any existing verses
        existing_chapters = {}
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for ch in data.get("chapters", []):
                        existing_chapters[ch["chapter"]] = ch["verses"]
            except Exception as e:
                print(f"Error reading {file_name}: {e}")

        # Generate all chapters
        chapters = []
        for ch_num in range(1, total_chapters + 1):
            if book_name in URDU_KEY_VERSES and ch_num in URDU_KEY_VERSES[book_name]:
                # Use our defined key verses
                verses = URDU_KEY_VERSES[book_name][ch_num]
            elif ch_num in existing_chapters and len(existing_chapters[ch_num]) > 0:
                # Preserve existing verses from the file
                verses = existing_chapters[ch_num]
            else:
                # Generate placeholder
                verses = generate_urdu_chapter(book_name, ch_num)

            chapters.append({
                "chapter": ch_num,
                "verses": verses
            })

        # Prepare book data
        book_data = {
            "book": book_name_urdu,
            "bookEnglish": book_name,
            "chapters": chapters
        }

        # Write to file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(book_data, f, ensure_ascii=False, indent=2)

        current_count = len(existing_chapters)
        if current_count >= total_chapters:
            print(f"✓ {book_name} ({book_name_urdu}): {current_count}/{total_chapters} chapters - OK")
        else:
            print(f"→ {book_name} ({book_name_urdu}): {current_count}/{total_chapters} chapters - Completed")

if __name__ == "__main__":
    main()

