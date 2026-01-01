import os
import random

BASE_DIR = "tuaa/video"
INDEX_FILE = os.path.join(BASE_DIR, "index.html")

# اجلب كل ملفات html (بدون index.html)
files = [
    f for f in os.listdir(BASE_DIR)
    if f.endswith(".html") and f != "index.html"
]

# ===== 1) إنشاء index.html =====
with open(INDEX_FILE, "w", encoding="utf-8") as index:
    index.write("""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>نيك مقاطع سكس مصري افلام سكس زباوي سكس كس العرب سكس العرب سكس شراميط سكس عرب xnxx</title>
<meta name="robots" content="index,follow">
</head>
<body>
<h1>سكس مصري افلام سكس عربي xnxx porn مشاهدة سكس فيديو سكس</h1>
<ul>
""")

    for f in files:
        index.write(f'<li><a href="{f}">{f.replace("-", " ").replace(".html","")}</a></li>\n')

    index.write("""
</ul>
</body>
</html>
""")

# ===== 2) إضافة ربط داخلي لكل ملف =====
for f in files:
    path = os.path.join(BASE_DIR, f)

    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    # تجاهل إذا الربط موجود مسبقًا
    if "مواضيع مشابهة" in content:
        continue

    related = random.sample([x for x in files if x != f], min(3, len(files)-1))

    links_html = "<hr><h3>سكس مصري سكس عراقي سكس مترجم افلام سكس مترجم سكس نيك كس سكس طيز سكس محارم</h3><ul>"
    for r in related:
        links_html += f'<li><a href="{r}">{r.replace("-", " ").replace(".html","")}</a></li>'
    links_html += "</ul>"

    # أضف قبل </body>
    if "</body>" in content:
        content = content.replace("</body>", links_html + "\n</body>")
    else:
        content += links_html

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

print("✔ تم إنشاء index.html وربط جميع المنشورات")
