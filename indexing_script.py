import json
import requests
import xml.etree.ElementTree as ET
from oauth2client.service_account import ServiceAccountCredentials

# --- إعدادات Google Indexing API ---
SCOPE = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
# رابط السايت ماب الخاص بموقعك (تم العثور على 5368 رابط فيه)
SITEMAP_URL = "https://pasuk-old.dicta.org.il/sitemap.xml"

def get_links_from_sitemap(url):
    """استخراج كافة الروابط من ملف السايت ماب"""
    try:
        print(f"📡 جاري محاولة قراءة السايت ماب من: {url}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # تعامل مع namespaces في ملف XML
        root = ET.fromstring(response.content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        links = []
        for url_tag in root.findall('ns:url', namespace):
            loc = url_tag.find('ns:loc', namespace)
            if loc is not None:
                links.append(loc.text)
        
        # إذا لم يجد روابط بالـ namespace حاول البحث العادي
        if not links:
            links = [loc.text for loc in root.iter('loc') if loc.text and loc.text.startswith('http')]
            
        return list(set(links)) # إزالة التكرار
    except Exception as e:
        print(f"❌ خطأ في قراءة السايت ماب: {e}")
        return []

def index_urls():
    """إرسال طلبات الأرشفة لجوجل باستخدام التنسيق المتوافق"""
    try:
        # تحميل بيانات الاعتماد من ملف service_account.json
        with open('service_account.json', 'r') as f:
            service_account_info = json.load(f)
            
        creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, SCOPE)
        # استخدام httplib2 المخزن داخل creds لتجنب مشاكل التوافق
        http = creds.authorize(requests.Session())

        links = get_links_from_sitemap(SITEMAP_URL)
        print(f"🔗 تم العثور على {len(links)} رابط في السايت ماب.")

        for url in links:
            body = {
                "url": url,
                "type": "URL_UPDATED"
            }
            
            # التعديل الجوهري هنا لضمان التوافق مع GitHub Actions
            # تم استبدال .post بـ .request لضمان عدم حدوث خطأ unexpected keyword argument 'data'
            response = http.request(
                ENDPOINT,
                method="POST",
                body=json.dumps(body),
                headers={'Content-Type': 'application/json'}
            )
            
            # استخراج حالة الاستجابة (الحالة تكون في العنصر الأول من tuple في بعض إصدارات المكتبة)
            status_code = response[0].status if isinstance(response, tuple) else response.status_code
            
            if status_code == 200:
                print(f"✅ تم إرسال طلب الأرشفة بنجاح: {url}")
            elif status_code == 429:
                print(f"🛑 توقف: تم الوصول للحد اليومي (Quota Exceeded) لجوجل.")
                break
            else:
                print(f"⚠️ فشل الطلب لـ {url}: حالة {status_code}")

    except FileNotFoundError:
        print("❌ خطأ: ملف service_account.json غير موجود! تأكد من إعداد Secrets في GitHub.")
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع أثناء المعالجة: {e}")

if __name__ == "__main__":
    index_urls()
