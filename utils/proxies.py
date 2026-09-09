import random
import requests
from utils.helpers import *

class ProxyManager:
    """إدارة الوكلاء"""
    
    def __init__(self, config):
        self.config = config
        self.proxies = config.PROXY_LIST
        self.current_proxy = None
    
    def get_random_proxy(self):
        """الحصول على وكيل عشوائي"""
        if not self.proxies:
            return None
        
        self.current_proxy = random.choice(self.proxies)
        return self.current_proxy
    
    def test_proxy(self, proxy):
        """اختبار صلاحية الوكيل"""
        try:
            proxies = {
                "http": proxy,
                "https": proxy,
            }
            
            response = requests.get(
                "https://api.ipify.org?format=json",
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                return True
            return False
            
        except:
            return False
    
    def get_working_proxy(self):
        """الحصول على وكيل صالح"""
        for _ in range(5):
            proxy = self.get_random_proxy()
            
            if proxy and self.test_proxy(proxy):
                return proxy
        
        return None
