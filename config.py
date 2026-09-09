import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """إعدادات الأداة"""
    
    # إعدادات API
    INSTAGRAM_API_URL = "https://i.instagram.com/api/v1/"
    INSTAGRAM_GRAPHQL = "https://www.instagram.com/graphql/query/"
    
    # إعدادات الجلسة
    SESSION_DIR = "data/sessions/"
    DOWNLOAD_DIR = "data/downloads/"
    REPORT_DIR = "data/reports/"
    
    # إعدادات الطلبات
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    DELAY_MIN = 2
    DELAY_MAX = 5
    
    # إعدادات الوكلاء
    PROXY_LIST = [
        "http://proxy1:8080",
        "http://proxy2:8080",
        "socks5://proxy3:1080",
    ]
    
    # إعدادات الكابتشا
    CAPTCHA_SERVICE = "2captcha"  # أو "anti-captcha"
    CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY", "")
    
    # إعدادات الحساب الوهمي
    FAKE_ACCOUNTS = [
        {"username": "fake_user_1", "password": "pass123"},
        {"username": "fake_user_2", "password": "pass456"},
    ]
    
    # رؤوس الطلبات
    HEADERS = {
        "User-Agent": "Instagram 275.0.0.27.98 Android (33/13; 420dpi; 1080x2400; samsung; SM-G998B; o1s; exynos2100; en_US; 458229258)",
        "Accept": "*/*",
        "Accept-Language": "en-US",
        "Accept-Encoding": "gzip, deflate",
        "X-IG-Capabilities": "3brTv10=",
        "X-IG-Connection-Type": "WIFI",
        "X-IG-App-ID": "567067343352427",
        "X-IG-Device-ID": "android-3f8e5c2d9a1b4f6e",
        "X-IG-Android-ID": "android-7a8b9c0d1e2f3a4b",
        "X-IG-Timezone": "Asia/Riyadh",
        "X-IG-Locale": "en_US",
    }
    
    # ثوابت الثغرات
    EXPLOITS = {
        "email_leak": True,
        "phone_leak": True,
        "story_viewer": True,
        "graphql_likes": True,
        "inbox_leak": True,
    }
