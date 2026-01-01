import os
import re
import random

BASE_DIR = "tuaa/video"
INDEX_FILE = os.path.join(BASE_DIR, "index.html")
MAIN_DOMAIN = "https://pasuk-old.dicta.org.il/"

# الكلمات المفتاحية لتعزيز قوة الروابط
KEYWORDS = [
    "سكس", "سكس مترجم", "نيك", "افلام سكس", "سكس مصري", 
    "xnxx", "sex", "porn", "شراميط", "نودز", "زباوي"
]

STOP_WORDS = {"مع","في","على","من","إلى","الى","عن","ال","و","او","أو","html"}

def extract_words(filename):
    name = filename.replace(".html", "")
    parts = re.split(r"[-_ ]+", name)
    return set(p for p in parts if p not in STOP_WORDS and len(p) > 2)

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

files = [f for f in os.listdir(BASE_DIR) if f.endswith(".html") and f != "index.html"]
file_words = {f: extract_words(f) for f in files}

with open(INDEX_FILE, "w", encoding="utf-8") as idx:
    idx.write(f"""<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<title>أرشيف فيديوهات السكس 2026</title><style>
body{{font-family:sans-serif;background:#000;color:#ccc;padding:20px}}
a{{color:#f90;text-decoration:none}}li{{margin-bottom:8px}}</style></head>
<body><h1>سكس/h1><ul>""")
    for f in files:
        title = f.replace("-", " ").replace(".html", "")
        idx.write(f'<li><a href="{f}">{title}</a></li>\n')
    idx.write("</ul></body></html>")

for f in files:
    path = os.path.join(BASE_DIR, f)
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read()

        if "" in content:
            continue

        similarities = []
        for other in files:
            if other == f: continue
            common = file_words[f] & file_words[other]
            if len(common) >= 1: similarities.append((other, len(common)))

        similarities.sort(key=lambda x: x[1], reverse=True)
        related = [x[0] for x in similarities[:3]]
        if not related: related = random.sample(files, min(len(files), 3))

        # بناء صندوق الروابط المشابهة + رابط العودة للدومين (Backlink)
        lucky_kw = random.choice(KEYWORDS)
        box = f"""
<hr>
<div class="related-section" style="padding:15px; background:#111; border-radius:5px;">
    <h3>{lucky_kw} مشابه</h3>
    <ul>
"""
        for r in related:
            r_title = r.replace("-", " ").replace(".html", "")
            box += f'        <li><a href="{r}" style="color:#f90;">{r_title}</a></li>\n'
        
        box += f"""
    </ul>
    <div style="margin-top:20px; text-align:center;">
        <a href="{MAIN_DOMAIN}" style="color:#555; font-size:12px;">العودة إلى {lucky_kw} الرئيسي</a>
    </div>
</div>
"""

        if "</body>" in content:
            content = content.replace("</body>", box + "\n</body>")
        else:
            content += box

        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        print(f"Error {f}: {e}")

print(f"✔ تم الربط بنجاح لـ {len(files)} ملف مع إضافة روابط العودة للدومين.")
