import os
import re

def update_html_files():
    # الرابط المستهدف والسكربت الجديد
    target_url = "https://www.effectivegatecpm.com/t042njps?key=0c4edd35ee2f3ea75d89d5b3cbf7cf96"
    
    new_script = f"""
<script>
    // تحويل آمن بعد 6 ثوانٍ لضمان الأرشفة الكاملة من قبل جوجل
    setTimeout(function(){{
        window.location.href = "{target_url}";
    }}, 6000);
</script>
"""

    # النمط المستخدم للبحث عن وسم الصورة الضار وإزالته
    # يبحث عن <img src="..." onerror=window.location="...">
    img_pattern = re.compile(r'<img[^>]+onerror=window\.location="[^"]+"[^>]*>', re.IGNORECASE)

    count = 0
    print("🚀 بدء عملية تحديث الملفات لتعزيز السيو...")

    # المسح الشامل للمجلد الحالي والمجلدات الفرعية
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # 1. إزالة وسم الصورة الضار إذا وجد
                    updated_content = img_pattern.sub('', content)

                    # 2. التأكد من عدم تكرار السكربت الجديد إذا تم تشغيله مرتين
                    if 'window.location.href =' not in updated_content:
                        # إضافة السكربت قبل إغلاق وسم body مباشرة
                        if '</body>' in updated_content:
                            updated_content = updated_content.replace('</body>', f'{new_script}\n</body>')
                        else:
                            # إذا لم يوجد وسم body (حالة نادرة)، يضاف في نهاية الملف
                            updated_content += new_script

                    # حفظ التعديلات
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    
                    count += 1
                    if count % 100 == 0:
                        print(f"✅ تم معالجة {count} ملف...")

                except Exception as e:
                    print(f"❌ خطأ في معالجة الملف {file_path}: {e}")

    print(f"\n✨ انتهت المهمة بنجاح! تم تحديث {count} ملف بنظام التحويل الآمن (6 ثوانٍ).")

if __name__ == "__main__":
    update_html_files()