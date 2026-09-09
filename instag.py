#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
InstaG - Instagram Ghost Tool
أداة جمع المعلومات الشاملة من إنستغرام
المؤلف: GENERAL
الإصدار: 1.0
"""

import os
import sys
import json
import argparse
import asyncio
from datetime import datetime

# إضافة المسارات
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# استيراد الوحدات
from config import Config
from core.auth import AuthManager
from core.scraper import Scraper
from core.analyzer import Analyzer
from core.reporter import Reporter
from utils.helpers import *

class InstaG:
    """الفئة الرئيسية للأداة"""
    
    def __init__(self):
        self.config = Config()
        self.auth_manager = AuthManager(self.config)
        self.client = None
        self.target_data = {}
    
    def setup(self, args):
        """إعداد الأداة"""
        print_banner()
        
        # تسجيل الدخول
        if args.session:
            # استخدام جلسة محفوظة
            session_file = os.path.join(self.config.SESSION_DIR, args.session)
            if not self.auth_manager.login_with_session(session_file):
                print_status("فشل تحميل الجلسة", "error")
                return False
        elif args.username and args.password:
            # تسجيل الدخول بالبيانات
            if not self.auth_manager.login_with_credentials(args.username, args.password):
                print_status("فشل تسجيل الدخول", "error")
                return False
        elif args.login_only:
            # إنشاء حساب وهمي تلقائياً
            fake_account = self.auth_manager.create_fake_account()
            if fake_account:
                print_status(f"تم إنشاء الحساب: {fake_account['username']}", "success")
                
                if not self.auth_manager.login_with_credentials(
                    fake_account["username"], 
                    fake_account["password"]
                ):
                    return False
            else:
                return False
        else:
            print_status("يجب توفير بيانات تسجيل الدخول أو جلسة", "error")
            return False
        
        self.client = self.auth_manager.client
        return True
    
    async def run(self, args):
        """تشغيل الأداة"""
        try:
            # إنشاء كائن الجمع
            scraper = Scraper(self.client, self.config)
            
            # جمع المعلومات
            self.target_data = await scraper.scrape_all(args.target)
            
            # التحليل
            print_status("بدء تحليل البيانات...", "info")
            analyzer = Analyzer(self.target_data)
            
            analysis_results = {
                "activity_analysis": analyzer.analyze_activity(),
                "engagement_analysis": analyzer.analyze_engagement(),
                "content_analysis": analyzer.analyze_content(),
                "fake_followers": analyzer.detect_fake_followers(),
            }
            
            self.target_data["analysis"] = analysis_results
            
            # إنشاء التقارير
            reporter = Reporter(self.target_data, self.config)
            
            timestamp = get_timestamp()
            target_name = args.target.replace("@", "")
            
            # حفظ التقارير
            if args.output == "json" or args.output == "all":
                reporter.save_json(f"{target_name}_{timestamp}.json")
            
            if args.output == "html" or args.output == "all":
                reporter.save_html(f"{target_name}_{timestamp}.html")
            
            if args.output == "csv" or args.output == "all":
                reporter.save_csv(f"{target_name}_{timestamp}.csv")
            
            if args.output == "txt" or args.output == "all":
                reporter.save_txt(f"{target_name}_{timestamp}.txt")
            
            # عرض ملخص
            self.display_summary()
            
            return True
            
        except Exception as e:
            print_status(f"فشل تشغيل الأداة: {str(e)}", "error")
            return False
    
    def display_summary(self):
        """عرض ملخص النتائج"""
        print("\n" + "=" * 60)
        print(Fore.CYAN + "📊 ملخص النتائج")
        print("=" * 60)
        
        basic_info = self.target_data.get("basic_info", {})
        
        if basic_info:
            print(f"{Fore.YELLOW}👤 المستخدم: {basic_info.get('username', 'N/A')}")
            print(f"{Fore.YELLOW}📛 الاسم: {basic_info.get('full_name', 'N/A')}")
            print(f"{Fore.YELLOW}👥 المتابعون: {format_number(basic_info.get('follower_count', 0))}")
            print(f"{Fore.YELLOW}📝 المنشورات: {basic_info.get('media_count', 0)}")
            
            if basic_info.get('is_private'):
                print(f"{Fore.RED}🔒 حساب خاص")
            else:
                print(f"{Fore.GREEN}🔓 حساب عام")
            
            if basic_info.get('is_verified'):
                print(f"{Fore.GREEN}✓ موثق")
        
        posts = self.target_data.get("posts", [])
        print(f"{Fore.YELLOW}📰 تم جمع {len(posts)} منشور")
        
        followers = self.target_data.get("followers", [])
        print(f"{Fore.YELLOW}👥 تم جمع {len(followers)} متابع")
        
        hidden_info = self.target_data.get("hidden_info", {})
        
        if hidden_info:
            if hidden_info.get("email"):
                print(f"{Fore.GREEN}📧 البريد: {hidden_info['email']}")
            
            if hidden_info.get("phone"):
                print(f"{Fore.GREEN}📱 الهاتف: {hidden_info['phone']}")
            
            if hidden_info.get("approximate_ip"):
                print(f"{Fore.GREEN}🌍 المنطقة التقريبية: {hidden_info['approximate_ip']}")
        
        print("=" * 60 + "\n")

def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(
        description="InstaG - Instagram Ghost Tool",
        epilog="المؤلف: GENERAL",
    )
    
    # خيارات تسجيل الدخول
    parser.add_argument("-u", "--username", help="اسم المستخدم للحساب الوهمي")
    parser.add_argument("-p", "--password", help="كلمة المرور للحساب الوهمي")
    parser.add_argument("-s", "--session", help="ملف الجلسة المحفوظة")
    parser.add_argument("--login-only", action="store_true", help="تسجيل الدخول وحفظ الجلسة فقط")
    
    # خيارات الهدف
    parser.add_argument("-t", "--target", help="اسم المستخدم المستهدف")
    
    # خيارات الإخراج
    parser.add_argument("-o", "--output", 
                       choices=["json", "html", "csv", "txt", "all"],
                       default="json",
                       help="صيغة التقرير (الافتراضي: json)")
    
    # خيارات إضافية
    parser.add_argument("--proxy", help="استخدام وكيل محدد")
    parser.add_argument("--delay", type=float, default=3, help="التأخير بين الطلبات")
    parser.add_argument("-v", "--version", action="version", version="InstaG v1.0")
    
    args = parser.parse_args()
    
    # إنشاء كائن الأداة
    instag = InstaG()
    
    # الإعداد
    if not instag.setup(args):
        sys.exit(1)
    
    # التشغيل
    if args.login_only:
        print_status("تم تسجيل الدخول وحفظ الجلسة", "success")
        sys.exit(0)
    
    if not args.target:
        print_status("يجب تحديد الحساب المستهدف (-t)", "error")
        sys.exit(1)
    
    # تشغيل الأداة
    try:
        asyncio.run(instag.run(args))
    except KeyboardInterrupt:
        print_status("\nتم إيقاف الأداة بواسطة المستخدم", "warning")
        sys.exit(0)

if __name__ == "__main__":
    main()
