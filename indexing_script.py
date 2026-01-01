import json
import requests
import xml.etree.ElementTree as ET
from oauth2client.service_account import ServiceAccountCredentials

# --- إعدادات Google Indexing API ---
SCOPE = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
# رابط السايت ماب الخاص بموقعك
SITEMAP_URL = "https://pasuk-old.dicta.org.il/sitemap.xml"

def get_links_from_sitemap(url):
    """استخراج كافة الروابط من ملف السايت ماب"""
    try:
        response = requests.get(url, timeout=20)
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
            links = [loc.text for loc in root.iter('loc')]
            
        return list(set(links)) # إزالة التكرار
    except Exception as e:
        print(f"❌ خطأ في قراءة السايت ماب: {e}")
        return []

def index_urls():
    """إرسال طلبات الأرشفة لجوجل"""
    try:
        # تحميل بيانات الاعتماد من ملف service_account.json
        # ملاحظة: المبرمج يجب أن يرفع هذا الملف أو يضعه في Secrets
        with open('service_account.json', 'r') as f:
            service_account_info = json.load(f)
            
        creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, SCOPE)
        threaded_http = creds.authorize(requests.Session())

        links = get_links_from_sitemap(SITEMAP_URL)
        print(f"🔗 تم العثور على {len(links)} رابط في السايت ماب.")

        for url in links:
            body = {
                "url": url,
                "type": "URL_UPDATED" # تعني أن الرابط جديد أو تم تحديثه
            }
            response = threaded_http.post(ENDPOINT, data=json.dumps(body))
            
            if response.status_code == 200:
                print(f"✅ تم إرسال طلب الأرشفة بنجاح: {url}")
            else:
                print(f"⚠️ فشل الطلب لـ {url}: {response.status_code} - {response.text}")

    except FileNotFoundError:
        print("❌ خطأ: ملف service_account.json غير موجود!")
    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    index_urls()