import requests
import time
from utils.helpers import *

class CaptchaSolver:
    """حل الكابتشا"""
    
    def __init__(self, config):
        self.config = config
        self.api_key = config.CAPTCHA_API_KEY
        self.service = config.CAPTCHA_SERVICE
    
    def solve(self, challenge_url):
        """حل الكابتشا"""
        try:
            if self.service == "2captcha":
                return self._solve_2captcha(challenge_url)
            elif self.service == "anti-captcha":
                return self._solve_anti_captcha(challenge_url)
            else:
                return self._solve_manually(challenge_url)
                
        except Exception as e:
            print_status(f"فشل حل الكابتشا: {str(e)}", "error")
            return None
    
    def _solve_2captcha(self, challenge_url):
        """حل عبر 2Captcha"""
        try:
            # إنشاء مهمة
            create_url = "https://2captcha.com/in.php"
            
            data = {
                "key": self.api_key,
                "method": "userrecaptcha",
                "googlekey": self._extract_site_key(challenge_url),
                "pageurl": challenge_url,
                "json": 1,
            }
            
            response = requests.post(create_url, data=data)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("status") == 1:
                    captcha_id = result.get("request")
                    
                    # انتظار الحل
                    solve_url = "https://2captcha.com/res.php"
                    
                    for _ in range(30):
                        time.sleep(5)
                        
                        solve_data = {
                            "key": self.api_key,
                            "action": "get",
                            "id": captcha_id,
                            "json": 1,
                        }
                        
                        solve_response = requests.get(solve_url, params=solve_data)
                        solve_result = solve_response.json()
                        
                        if solve_result.get("status") == 1:
                            return solve_result.get("request")
            
            return None
            
        except:
            return None
    
    def _solve_anti_captcha(self, challenge_url):
        """حل عبر Anti-Captcha"""
        try:
            url = "https://api.anti-captcha.com/createTask"
            
            data = {
                "clientKey": self.api_key,
                "task": {
                    "type": "NoCaptchaTaskProxyless",
                    "websiteURL": challenge_url,
                    "websiteKey": self._extract_site_key(challenge_url),
                },
            }
            
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("errorId") == 0:
                    task_id = result.get("taskId")
                    
                    # انتظار الحل
                    get_url = "https://api.anti-captcha.com/getTaskResult"
                    
                    for _ in range(30):
                        time.sleep(5)
                        
                        get_data = {
                            "clientKey": self.api_key,
                            "taskId": task_id,
                        }
                        
                        get_response = requests.post(get_url, json=get_data)
                        get_result = get_response.json()
                        
                        if get_result.get("status") == "ready":
                            return get_result["solution"]["gRecaptchaResponse"]
            
            return None
            
        except:
            return None
    
    def _solve_manually(self, challenge_url):
        """حل يدوي"""
        print_status(f"يرجى حل الكابتشا يدوياً: {challenge_url}", "warning")
        solution = input("أدخل الحل: ")
        return solution
    
    def _extract_site_key(self, url):
        """استخراج مفتاح الموقع"""
        try:
            response = requests.get(url)
            
            import re
            match = re.search(r'data-sitekey="([^"]+)"', response.text)
            
            if match:
                return match.group(1)
            
            return None
            
        except:
            return None
