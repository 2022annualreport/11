import os

def generate_index():
    base_dir = 'tuaa/video'
    output_file = 'index.html'
    
    # بداية ملف HTML مع التصميم السابق
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dicta - Video Index</title>
    <style>
        body { font-family: sans-serif; padding: 40px; line-height: 1.6; color: #333; }
        h1 { color: #2563eb; text-align: center; }
        .links-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 10px; margin-top: 30px; }
        a { color: #4b5563; text-decoration: none; font-size: 14px; border: 1px solid #eee; padding: 8px; border-radius: 4px; display: block; }
        a:hover { background-color: #f0f7ff; border-color: #2563eb; }
    </style>
</head>
<body>
    <h1>Archive Index</h1>
    <p style="text-align:center">Total indexed pages: {count}</p>
    <div class="links-container">
"""

    # جلب كافة ملفات html من المجلد
    links = []
    if os.path.exists(base_dir):
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.html'):
                    # بناء المسار النسبي للرابط
                    relative_path = os.path.join(root, file)
                    links.append(f'<a href="{relative_path}">{file}</a>')

    # إغلاق ملف HTML
    html_content = html_content.format(count=len(links))
    html_content += "\\n".join(links)
    html_content += """
    </div>
</body>
</html>"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ Done! Generated index.html with {len(links)} links.")

if __name__ == "__main__":
    generate_index()
