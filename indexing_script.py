import json
import requests
import xml.etree.ElementTree as ET
from oauth2client.service_account import ServiceAccountCredentials

# --- إعدادات Google Indexing API ---
SCOPE = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
# الرابط الصحيح بدون أي إضافات
SITEMAP_URL = "https://pasuk-old.dicta.org.il/sitemap.xml"

def get_links_from_sitemap(url):
    """استخراج كافة الروابط من ملف السايت ماب"""
    try:
        print(f"📡 جاري محاولة قراءة السايت ماب من: {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        links = []
        for url_tag in root.findall('ns:url', namespace):
            loc = url_tag.find('ns:loc', namespace)
            if loc is not None:
                links.append(loc.text)
        
        if not links:
            links = [loc.text for loc in root.iter('loc') if loc.text and loc.text.startswith('http')]
            
        return list(set(links))
    except Exception as e:
        print(f"❌ خطأ في قراءة السايت ماب: {e}")
        return []

def index_urls():
    """إرسال طلبات الأرشفة لجوجل"""
    try:
        with open('service_account.json', 'r') as f:
            service_account_info = json.load(f)
            
        creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, SCOPE)
        # استخدام التخويل الصحيح للمكتبة
        http_auth = creds.authorize(creds._http.__class__())

        links = get_links_from_sitemap(SITEMAP_URL)
        print(f"🔗 تم العثور على {len(links)} رابط.")

        for url in links:
            body = json.dumps({"url": url, "type": "URL_UPDATED"})
            
            # تم تعديل ترتيب المتغيرات هنا لحل خطأ 'multiple values for argument method'
            response, content = http_auth.request(
                uri=ENDPOINT,
                method="POST",
                body=body,
                headers={'Content-Type': 'application/json'}
            )
            
            status_code = response.status
            
            if status_code == 200:
                print(f"✅ تم الإرسال: {url}")
            elif status_code == 429:
                print(f"🛑 تم الوصول للحد اليومي لجوجل (200 رابط).")
                break
            else:
                print(f"⚠️ فشل: {status_code} لـ {url}")

    except Exception as e:
        print(f"❌ حدث خطأ تقني: {e}")

if __name__ == "__main__":
    index_urls()
