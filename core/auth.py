import os
import json
import time
import random
import pickle
from instagrapi import Client
from utils.helpers import *
from utils.proxies import ProxyManager
from utils.captcha import CaptchaSolver

class AuthManager:
    """إدارة تسجيل الدخول والجلسات"""
    
    def __init__(self, config):
        self.config = config
        self.client = None
        self.session_file = None
        self.proxy_manager = ProxyManager(config)
        self.captcha_solver = CaptchaSolver(config)
    
    def login_with_credentials(self, username, password, proxy=None):
        """تسجيل الدخول باستخدام اسم المستخدم وكلمة المرور"""
        try:
            print_status("محاولة تسجيل الدخول...", "info")
            
            self.client = Client()
            
            # تعيين الوكيل إذا وجد
            if proxy:
                self.client.set_proxy(proxy)
            
            # تعيين رؤوس مخصصة
            self.client.set_user_agent(self.config.HEADERS["User-Agent"])
            
            # محاولة تسجيل الدخول
            try:
                self.client.login(username, password)
                print_status(f"تم تسجيل الدخول بنجاح كـ {username}", "success")
                
                # حفظ الجلسة
                self.save_session(username)
                return True
                
            except Exception as e:
                # محاولة تجاوز الكابتشا
                if "challenge_required" in str(e).lower():
                    print_status("تم اكتشاف كابتشا، محاولة التجاوز...", "warning")
                    return self._handle_captcha(username, password, proxy)
                
                print_status(f"فشل تسجيل الدخول: {str(e)}", "error")
                return False
                
        except Exception as e:
            print_status(f"خطأ غير متوقع: {str(e)}", "error")
            return False
    
    def login_with_session(self, session_file):
        """تسجيل الدخول باستخدام جلسة محفوظة"""
        try:
            print_status("محاولة تحميل الجلسة...", "info")
            
            self.client = Client()
            
            # تحميل الجلسة
            session_data = self._load_session(session_file)
            if not session_data:
                return False
            
            # تعيين الجلسة
            self.client.set_settings(session_data)
            
            # التحقق من صلاحية الجلسة
            self.client.account_info()
            
            print_status("تم تحميل الجلسة بنجاح", "success")
            self.session_file = session_file
            return True
            
        except Exception as e:
            print_status(f"فشل تحميل الجلسة: {str(e)}", "error")
            return False
    
    def create_fake_account(self):
        """إنشاء حساب وهمي جديد"""
        try:
            import requests
            
            # بيانات الحساب الوهمي
            import random
            import string
            
            username = "user_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$", k=16))
            email = f"{username}@gmail.com"
            
            print_status(f"إنشاء حساب وهمي: {username}", "info")
            
            # محاولة الإنشاء عبر API
            url = "https://i.instagram.com/api/v1/accounts/create/"
            
            data = {
                "username": username,
                "password": password,
                "email": email,
                "device_id": self._generate_device_id(),
                "guid": self._generate_guid(),
                "waterfall_id": self._generate_waterfall_id(),
            }
            
            headers = self.config.HEADERS.copy()
            
            response = requests.post(url, data=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                print_status("تم إنشاء الحساب الوهمي بنجاح", "success")
                return {"username": username, "password": password, "email": email}
            else:
                print_status(f"فشل إنشاء الحساب: {response.text}", "error")
                return None
                
        except Exception as e:
            print_status(f"خطأ في إنشاء الحساب: {str(e)}", "error")
            return None
    
    def save_session(self, username):
        """حفظ الجلسة الحالية"""
        try:
            os.makedirs(self.config.SESSION_DIR, exist_ok=True)
            
            session_data = self.client.get_settings()
            session_file = os.path.join(self.config.SESSION_DIR, f"{username}_session.json")
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2, default=str)
            
            self.session_file = session_file
            print_status(f"تم حفظ الجلسة في: {session_file}", "success")
            
        except Exception as e:
            print_status(f"فشل حفظ الجلسة: {str(e)}", "error")
    
    def _load_session(self, session_file):
        """تحميل الجلسة من ملف"""
        try:
            if not os.path.exists(session_file):
                print_status("ملف الجلسة غير موجود", "error")
                return None
            
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            return session_data
            
        except Exception as e:
            print_status(f"فشل قراءة ملف الجلسة: {str(e)}", "error")
            return None
    
    def _handle_captcha(self, username, password, proxy=None):
        """معالجة الكابتشا"""
        try:
            # الحصول على معرف التحدي
            challenge_url = self.client.last_response.headers.get("challenge_url")
            if not challenge_url:
                return False
            
            # حل الكابتشا عبر الخدمة
            captcha_solution = self.captcha_solver.solve(challenge_url)
            if not captcha_solution:
                print_status("فشل حل الكابتشا", "error")
                return False
            
            # إعادة المحاولة مع الحل
            self.client.challenge_resolve(captcha_solution)
            
            # تسجيل الدخول مرة أخرى
            self.client.login(username, password)
            
            print_status("تم تجاوز الكابتشا وتسجيل الدخول", "success")
            self.save_session(username)
            return True
            
        except Exception as e:
            print_status(f"فشل معالجة الكابتشا: {str(e)}", "error")
            return False
    
    def _generate_device_id(self):
        """توليد معرف جهاز عشوائي"""
        import uuid
        return f"android-{uuid.uuid4().hex[:16]}"
    
    def _generate_guid(self):
        """توليد GUID عشوائي"""
        import uuid
        return str(uuid.uuid4())
    
    def _generate_waterfall_id(self):
        """توليد Waterfall ID"""
        import uuid
        return str(uuid.uuid4())
