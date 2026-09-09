import json
from datetime import datetime
from collections import Counter
from utils.helpers import *

class Analyzer:
    """تحليل البيانات والاستنتاج"""
    
    def __init__(self, data):
        self.data = data
    
    def analyze_activity(self):
        """تحليل النشاط"""
        try:
            posts = self.data.get("posts", [])
            
            if not posts:
                return None
            
            # تحليل الأيام
            day_counts = Counter()
            hour_counts = Counter()
            
            for post in posts:
                if post.get("taken_at"):
                    dt = datetime.fromisoformat(post["taken_at"])
                    day_counts[dt.strftime("%A")] += 1
                    hour_counts[dt.hour] += 1
            
            return {
                "most_active_day": day_counts.most_common(1)[0] if day_counts else None,
                "most_active_hour": hour_counts.most_common(1)[0] if hour_counts else None,
                "total_posts": len(posts),
                "days_active": list(day_counts.items()),
                "hours_active": list(hour_counts.items()),
            }
            
        except Exception as e:
            return None
    
    def analyze_engagement(self):
        """تحليل التفاعل"""
        try:
            posts = self.data.get("posts", [])
            
            if not posts:
                return None
            
            total_likes = sum(p.get("like_count", 0) for p in posts)
            total_comments = sum(p.get("comment_count", 0) for p in posts)
            
            avg_likes = total_likes / len(posts) if posts else 0
            avg_comments = total_comments / len(posts) if posts else 0
            
            # أكثر المنشورات تفاعلاً
            most_liked = max(posts, key=lambda p: p.get("like_count", 0)) if posts else None
            most_commented = max(posts, key=lambda p: p.get("comment_count", 0)) if posts else None
            
            return {
                "total_likes": total_likes,
                "total_comments": total_comments,
                "avg_likes": avg_likes,
                "avg_comments": avg_comments,
                "most_liked_post": most_liked,
                "most_commented_post": most_commented,
            }
            
        except Exception as e:
            return None
    
    def analyze_content(self):
        """تحليل المحتوى"""
        try:
            posts = self.data.get("posts", [])
            
            if not posts:
                return None
            
            content_types = Counter()
            
            for post in posts:
                media_type = post.get("media_type", 0)
                
                if media_type == 1:
                    content_types["صور"] += 1
                elif media_type == 2:
                    content_types["فيديو"] += 1
                elif media_type == 8:
                    content_types["كاروسيل"] += 1
            
            return {
                "content_types": dict(content_types),
                "hashtags": self._count_hashtags(posts),
                "mentions": self._count_mentions(posts),
            }
            
        except Exception as e:
            return None
    
    def detect_fake_followers(self):
        """كشف الحسابات المزيفة"""
        try:
            followers = self.data.get("followers", [])
            
            if not followers:
                return None
            
            fake_accounts = []
            
            for follower in followers:
                is_fake = False
                
                # معايير الكشف
                if not follower.get("full_name"):
                    is_fake = True
                
                if not follower.get("profile_pic_url"):
                    is_fake = True
                
                username = follower.get("username", "")
                if username.count("_") > 3:
                    is_fake = True
                
                if len(username) > 30:
                    is_fake = True
                
                if is_fake:
                    fake_accounts.append(follower)
            
            return {
                "total_followers": len(followers),
                "fake_followers": len(fake_accounts),
                "fake_percentage": (len(fake_accounts) / len(followers)) * 100 if followers else 0,
                "fake_accounts_list": fake_accounts[:20],
            }
            
        except Exception as e:
            return None
    
    def _count_hashtags(self, posts):
        """عد الهاشتاقات"""
        hashtags = Counter()
        
        for post in posts:
            for hashtag in post.get("hashtags", []):
                hashtags[hashtag] += 1
        
        return hashtags.most_common(20)
    
    def _count_mentions(self, posts):
        """عد الإشارات"""
        mentions = Counter()
        
        for post in posts:
            for mention in post.get("mentions", []):
                mentions[mention] += 1
        
        return mentions.most_common(20)
