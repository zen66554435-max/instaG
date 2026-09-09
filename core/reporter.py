import os
import json
import csv
import html as html_module
from datetime import datetime
from utils.helpers import *

class Reporter:
    """إنشاء التقارير"""
    
    def __init__(self, data, config):
        self.data = data
        self.config = config
    
    def save_json(self, filename):
        """حفظ التقرير بصيغة JSON"""
        try:
            os.makedirs(self.config.REPORT_DIR, exist_ok=True)
            filepath = os.path.join(self.config.REPORT_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False, default=str)
            
            print_status(f"تم حفظ التقرير: {filepath}", "success")
            return filepath
            
        except Exception as e:
            print_status(f"فشل حفظ التقرير: {str(e)}", "error")
            return None
    
    def save_html(self, filename):
        """حفظ التقرير بصيغة HTML"""
        try:
            os.makedirs(self.config.REPORT_DIR, exist_ok=True)
            filepath = os.path.join(self.config.REPORT_DIR, filename)
            
            html_content = self._generate_html_report()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print_status(f"تم حفظ التقرير: {filepath}", "success")
            return filepath
            
        except Exception as e:
            print_status(f"فشل حفظ التقرير: {str(e)}", "error")
            return None
    
    def save_csv(self, filename):
        """حفظ التقرير بصيغة CSV"""
        try:
            os.makedirs(self.config.REPORT_DIR, exist_ok=True)
            filepath = os.path.join(self.config.REPORT_DIR, filename)
            
            # حفظ المعلومات الأساسية
            basic_info = self.data.get("basic_info", {})
            
            if basic_info:
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["المفتاح", "القيمة"])
                    
                    for key, value in basic_info.items():
                        writer.writerow([key, value])
            
            print_status(f"تم حفظ التقرير: {filepath}", "success")
            return filepath
            
        except Exception as e:
            print_status(f"فشل حفظ التقرير: {str(e)}", "error")
            return None
    
    def save_txt(self, filename):
        """حفظ التقرير بصيغة TXT"""
        try:
            os.makedirs(self.config.REPORT_DIR, exist_ok=True)
            filepath = os.path.join(self.config.REPORT_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("تقرير InstaG - Instagram Ghost\n")
                f.write(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                # المعلومات الأساسية
                basic_info = self.data.get("basic_info", {})
                if basic_info:
                    f.write("## المعلومات الأساسية\n")
                    f.write("-" * 30 + "\n")
                    
                    for key, value in basic_info.items():
                        f.write(f"{key}: {value}\n")
                    
                    f.write("\n")
                
                # المنشورات
                posts = self.data.get("posts", [])
                if posts:
                    f.write("## المنشورات\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"عدد المنشورات: {len(posts)}\n\n")
                    
                    for i, post in enumerate(posts[:10], 1):
                        f.write(f"المنشور {i}:\n")
                        f.write(f"  - النص: {post.get('caption', '')[:100]}\n")
                        f.write(f"  - الإعجابات: {post.get('like_count', 0)}\n")
                        f.write(f"  - التعليقات: {post.get('comment_count', 0)}\n\n")
            
            print_status(f"تم حفظ التقرير: {filepath}", "success")
            return filepath
            
        except Exception as e:
            print_status(f"فشل حفظ التقرير: {str(e)}", "error")
            return None
    
    def _generate_html_report(self):
        """توليد تقرير HTML"""
        basic_info = self.data.get("basic_info", {})
        posts = self.data.get("posts", [])
        
        html_template = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير InstaG - {basic_info.get('username', 'Unknown')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
        }}
        
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        
        .header {{
            text-align: center;
            padding: 20px;
            border-bottom: 3px solid #667eea;
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            color: #333;
            font-size: 36px;
            margin-bottom: 10px;
        }}
        
        .header .target {{
            color: #667eea;
            font-size: 24px;
            font-weight: bold;
        }}
        
        .section {{
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        
        .section h2 {{
            color: #667eea;
            margin-bottom: 15px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}
        
        .info-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .info-item .label {{
            font-weight: bold;
            color: #555;
            font-size: 14px;
        }}
        
        .info-item .value {{
            color: #333;
            font-size: 18px;
            margin-top: 5px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th, td {{
            padding: 12px;
            text-align: right;
            border-bottom: 1px solid #ddd;
        }}
        
        th {{
            background: #667eea;
            color: white;
        }}
        
        tr:hover {{
            background: #f5f5f5;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }}
        
        .badge-verified {{
            background: #28a745;
            color: white;
        }}
        
        .badge-private {{
            background: #dc3545;
            color: white;
        }}
        
        .badge-public {{
            background: #17a2b8;
            color: white;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🕵️ InstaG Report</h1>
            <div class="target">الهدف: {basic_info.get('username', 'Unknown')}</div>
            <p>تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="section">
            <h2>📋 المعلومات الأساسية</h2>
            <div class="info-grid">
                <div class="info-item">
                    <div class="label">اسم المستخدم</div>
                    <div class="value">{basic_info.get('username', 'N/A')}</div>
                </div>
                <div class="info-item">
                    <div class="label">الاسم الكامل</div>
                    <div class="value">{basic_info.get('full_name', 'N/A')}</div>
                </div>
                <div class="info-item">
                    <div class="label">المتابعون</div>
                    <div class="value">{basic_info.get('follower_count', 0)}</div>
                </div>
                <div class="info-item">
                    <div class="label">المتابَعون</div>
                    <div class="value">{basic_info.get('following_count', 0)}</div>
                </div>
                <div class="info-item">
                    <div class="label">المنشورات</div>
                    <div class="value">{basic_info.get('media_count', 0)}</div>
                </div>
                <div class="info-item">
                    <div class="label">نوع الحساب</div>
                    <div class="value">
                        <span class="badge {'badge-private' if basic_info.get('is_private') else 'badge-public'}">
                            {'خاص' if basic_info.get('is_private') else 'عام'}
                        </span>
                        {f'<span class="badge badge-verified">موثق</span>' if basic_info.get('is_verified') else ''}
                    </div>
                </div>
                <div class="info-item">
                    <div class="label">البايو</div>
                    <div class="value">{html_module.escape(str(basic_info.get('bio', 'N/A')))}</div>
                </div>
                <div class="info-item">
                    <div class="label">الرابط الخارجي</div>
                    <div class="value">{html_module.escape(str(basic_info.get('external_url', 'N/A')))}</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📝 المنشورات الأخيرة</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>النص</th>
                        <th>الإعجابات</th>
                        <th>التعليقات</th>
                        <th>التاريخ</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_posts_rows(posts[:20])}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
        """
        
        return html_template
    
    def _generate_posts_rows(self, posts):
        """توليد صفوف المنشورات"""
        rows = ""
        
        for i, post in enumerate(posts, 1):
            caption = html_module.escape(str(post.get('caption', '')))[:50]
            likes = post.get('like_count', 0)
            comments = post.get('comment_count', 0)
            date = post.get('taken_at', 'N/A')
            
            if date != 'N/A':
                try:
                    date = datetime.fromisoformat(date).strftime('%Y-%m-%d')
                except:
                    pass
            
            rows += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{caption}...</td>
                        <td>{likes}</td>
                        <td>{comments}</td>
                        <td>{date}</td>
                    </tr>
            """
        
        return rows
