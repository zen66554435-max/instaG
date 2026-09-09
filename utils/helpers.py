import os
import sys
import time
import json
import random
import shutil
from datetime import datetime
from colorama import init, Fore, Back, Style

# تهيئة colorama
init(autoreset=True)

def print_banner():
    """طباعة شعار الأداة"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
{Fore.CYAN}║                                                          ║
{Fore.MAGENTA}║  ██╗███╗   ██╗███████╗████████╗ █████╗  ██████╗       ║
{Fore.MAGENTA}║  ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝       ║
{Fore.MAGENTA}║  ██║██╔██╗ ██║███████╗   ██║   ███████║██║  ███╗      ║
{Fore.MAGENTA}║  ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║   ██║      ║
{Fore.MAGENTA}║  ██║██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝      ║
{Fore.MAGENTA}║  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝       ║
{Fore.CYAN}║                                                          ║
{Fore.YELLOW}║  🕵️  Instagram Ghost - أداة جمع المعلومات الشاملة       ║
{Fore.YELLOW}║  👻  InstaG v1.0 - بواسطة GENERAL                        ║
{Fore.CYAN}║                                                          ║
{Fore.CYAN}╚══════════════════════════════════════════════════════════╝
"""
    print(banner)

def print_status(message, status="info"):
    """طباعة رسالة حالة"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if status == "success":
        print(f"{Fore.GREEN}[✓] {timestamp} - {message}")
    elif status == "error":
        print(f"{Fore.RED}[✗] {timestamp} - {message}")
    elif status == "warning":
        print(f"{Fore.YELLOW}[!] {timestamp} - {message}")
    else:
        print(f"{Fore.CYAN}[*] {timestamp} - {message}")

def print_progress(current, total, prefix="", suffix=""):
    """طباعة شريط تقدم"""
    percentage = int(current / total * 100)
    bar_length = 50
    filled = int(bar_length * current / total)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    print(f"\r{Fore.CYAN}{prefix} |{Fore.GREEN}{bar}{Fore.CYAN}| {percentage}% {suffix}", end="")
    
    if current == total:
        print()

def random_delay(min_seconds=2, max_seconds=5):
    """تأخير عشوائي"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    return delay

def format_number(number):
    """تنسيق الأرقام"""
    if number >= 1000000:
        return f"{number/1000000:.1f}M"
    elif number >= 1000:
        return f"{number/1000:.1f}K"
    return str(number)

def save_json_file(data, filepath):
    """حفظ ملف JSON"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        return True
        
    except Exception as e:
        print_status(f"فشل حفظ الملف: {str(e)}", "error")
        return False

def load_json_file(filepath):
    """تحميل ملف JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except Exception as e:
        print_status(f"فشل تحميل الملف: {str(e)}", "error")
        return None

def create_directory(directory):
    """إنشاء مجلد"""
    try:
        os.makedirs(directory, exist_ok=True)
        return True
        
    except Exception as e:
        print_status(f"فشل إنشاء المجلد: {str(e)}", "error")
        return False

def clean_filename(filename):
    """تنظيف اسم الملف"""
    import re
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.strip()
    return filename if filename else "unnamed"

def get_timestamp():
    """الحصول على الوقت الحالي"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def download_file(url, filepath, headers=None):
    """تحميل ملف"""
    try:
        import requests
        
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        
        if response.status_code == 200:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
        
        return False
        
    except Exception as e:
        print_status(f"فشل تحميل الملف: {str(e)}", "error")
        return False

def get_file_size(filepath):
    """الحصول على حجم الملف"""
    try:
        size = os.path.getsize(filepath)
        
        if size >= 1024 * 1024:
            return f"{size/(1024*1024):.2f} MB"
        elif size >= 1024:
            return f"{size/1024:.2f} KB"
        else:
            return f"{size} B"
            
    except:
        return "N/A"
