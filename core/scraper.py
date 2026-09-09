import os
import json
import time
import random
import asyncio
import aiohttp
import aiofiles
from datetime import datetime
from instagrapi import Client
from utils.helpers import *
from utils.user_agents import USER_AGENTS

class Scraper:
    """جمع المعلومات من إنستغرام"""
    
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.target_data = {}
    
    async def scrape_all(self, target_username):
        """جمع جميع المعلومات عن الحساب المستهدف"""
        print_status(f"بدء جمع المعلومات عن: {target_username}", "info")
        
        # المعلومات الأساسية
        self.target_data["basic_info"] = await self.get_basic_info(target_username)
        
        # المنشورات
        self.target_data["posts"] = await self.get_posts(target_username)
        
        # القصص
        self.target_data["stories"] = await self.get_stories(target_username)
        
        # الهايلايت
        self.target_data["highlights"] = await self.get_highlights(target_username)
        
        # المتابعين
        self.target_data["followers"] = await self.get_followers(target_username)
        
        # المتابَعين
        self.target_data["following"] = await self.get_following(target_username)
        
        # الإشارات
        self.target_data["tags"] = await self.get_tags(target_username)
        
        # المعلومات المخفية
        self.target_data["hidden_info"] = await self.get_hidden_info(target_username)
        
        print_status("اكتمل جمع المعلومات", "success")
        return self.target_data
    
    async def get_basic_info(self, username):
        """جمع المعلومات الأساسية للحساب"""
        try:
            user_info = self.client.user_info_by_username(username)
            
            basic_info = {
                "user_id": user_info.pk,
                "username": user_info.username,
                "full_name": user_info.full_name,
                "bio": user_info.biography,
                "external_url": user_info.external_url,
                "profile_pic_url": user_info.profile_pic_url,
                "follower_count": user_info.follower_count,
                "following_count": user_info.following_count,
                "media_count": user_info.media_count,
                "is_private": user_info.is_private,
                "is_verified": user_info.is_verified,
                "is_business": user_info.is_business,
                "business_category": user_info.business_category_name if user_info.is_business else None,
                "category": user_info.category,
                "contact_phone": user_info.contact_phone_number if hasattr(user_info, 'contact_phone_number') else None,
                "contact_email": user_info.public_email if hasattr(user_info, 'public_email') else None,
                "address": user_info.business_address if hasattr(user_info, 'business_address') else None,
            }
            
            print_status(f"تم جمع المعلومات الأساسية: {username}", "success")
            return basic_info
            
        except Exception as e:
            print_status(f"فشل جمع المعلومات الأساسية: {str(e)}", "error")
            return None
    
    async def get_posts(self, username):
        """جمع جميع المنشورات"""
        try:
            user_id = self.client.user_id_from_username(username)
            posts = self.client.user_medias(user_id, amount=50)
            
            posts_data = []
            for post in posts:
                post_info = {
                    "id": post.pk,
                    "code": post.code,
                    "caption": post.caption_text,
                    "like_count": post.like_count,
                    "comment_count": post.comment_count,
                    "taken_at": post.taken_at.isoformat() if post.taken_at else None,
                    "media_type": post.media_type,
                    "location": post.location.name if post.location else None,
                    "location_lat": post.location.lat if post.location else None,
                    "location_lng": post.location.lng if post.location else None,
                    "hashtags": self._extract_hashtags(post.caption_text),
                    "mentions": self._extract_mentions(post.caption_text),
                    "urls": self._extract_urls(post.caption_text),
                }
                
                # جلب الإعجابات
                post_info["likers"] = self.get_post_likers(post.pk)
                
                # جلب التعليقات
                post_info["comments"] = self.get_post_comments(post.pk)
                
                posts_data.append(post_info)
            
            print_status(f"تم جمع {len(posts_data)} منشور", "success")
            return posts_data
            
        except Exception as e:
            print_status(f"فشل جمع المنشورات: {str(e)}", "error")
            return []
    
    async def get_stories(self, username):
        """جمع القصص النشطة"""
        try:
            user_id = self.client.user_id_from_username(username)
            stories = self.client.user_stories(user_id)
            
            stories_data = []
            for story in stories:
                story_info = {
                    "id": story.pk,
                    "taken_at": story.taken_at.isoformat() if story.taken_at else None,
                    "media_type": story.media_type,
                    "caption": story.caption_text if hasattr(story, 'caption_text') else None,
                }
                stories_data.append(story_info)
            
            print_status(f"تم جمع {len(stories_data)} قصة", "success")
            return stories_data
            
        except Exception as e:
            print_status(f"فشل جمع القصص: {str(e)}", "error")
            return []
    
    async def get_highlights(self, username):
        """جمع الهايلايت"""
        try:
            user_id = self.client.user_id_from_username(username)
            highlights = self.client.user_highlights(user_id)
            
            highlights_data = []
            for highlight in highlights:
                highlight_info = {
                    "id": highlight.pk,
                    "title": highlight.title,
                    "cover": highlight.cover_media_url,
                }
                highlights_data.append(highlight_info)
            
            print_status(f"تم جمع {len(highlights_data)} هايلايت", "success")
            return highlights_data
            
        except Exception as e:
            print_status(f"فشل جمع الهايلايت: {str(e)}", "error")
            return []
    
    async def get_followers(self, username):
        """جمع قائمة المتابعين"""
        try:
            user_id = self.client.user_id_from_username(username)
            followers = self.client.user_followers(user_id, amount=100)
            
            followers_data = []
            for follower_id, follower_info in followers.items():
                follower_data = {
                    "user_id": follower_id,
                    "username": follower_info.username,
                    "full_name": follower_info.full_name,
                    "profile_pic_url": follower_info.profile_pic_url,
                    "is_private": follower_info.is_private,
                    "is_verified": follower_info.is_verified,
                }
                followers_data.append(follower_data)
            
            print_status(f"تم جمع {len(followers_data)} متابع", "success")
            return followers_data
            
        except Exception as e:
            print_status(f"فشل جمع المتابعين: {str(e)}", "error")
            return []
    
    async def get_following(self, username):
        """جمع قائمة المتابَعين"""
        try:
            user_id = self.client.user_id_from_username(username)
            following = self.client.user_following(user_id, amount=100)
            
            following_data = []
            for following_id, following_info in following.items():
                following_data.append({
                    "user_id": following_id,
                    "username": following_info.username,
                    "full_name": following_info.full_name,
                    "profile_pic_url": following_info.profile_pic_url,
                })
            
            print_status(f"تم جمع {len(following_data)} متابَع", "success")
            return following_data
            
        except Exception as e:
            print_status(f"فشل جمع المتابَعين: {str(e)}", "error")
            return []
    
    async def get_tags(self, username):
        """جمع المنشورات التي تمت الإشارة فيها للحساب"""
        try:
            tags = self.client.hashtag_medias_top(username, amount=30)
            
            tags_data = []
            for tag in tags:
                tags_data.append({
                    "id": tag.pk,
                    "code": tag.code,
                    "caption": tag.caption_text,
                })
            
            return tags_data
            
        except Exception as e:
            return []
    
    async def get_hidden_info(self, username):
        """جمع المعلومات غير الظاهرة"""
        from core.exploits import ExploitManager
        
        exploits = ExploitManager(self.client, self.config)
        
        hidden_info = {
            "email": await exploits.get_email_leak(username),
            "phone": await exploits.get_phone_leak(username),
            "approximate_ip": await exploits.get_ip_from_cdn(username),
            "device_type": await exploits.get_device_type(username),
            "activity_times": await exploits.get_activity_times(username),
            "hidden_likes": await exploits.get_hidden_likes(username),
            "deleted_comments": await exploits.get_deleted_comments(username),
            "public_conversations": await exploits.get_public_conversations(username),
            "targeted_ads": await exploits.get_targeted_ads(username),
            "external_links": await exploits.get_external_links(username),
            "geolocation": await exploits.get_geolocation(username),
        }
        
        return hidden_info
    
    def get_post_likers(self, post_id):
        """جلب المعجبين بالمنشور"""
        try:
            likers = self.client.media_likers(post_id)
            return [{"user_id": l.pk, "username": l.username} for l in likers]
        except:
            return []
    
    def get_post_comments(self, post_id):
        """جلب التعليقات على المنشور"""
        try:
            comments = self.client.media_comments(post_id, amount=50)
            return [{"user_id": c.user.pk, "username": c.user.username, "text": c.text} for c in comments]
        except:
            return []
    
    def _extract_hashtags(self, text):
        """استخراج الهاشتاقات"""
        import re
        if not text:
            return []
        return re.findall(r'#(\w+)', text)
    
    def _extract_mentions(self, text):
        """استخراج الإشارات"""
        import re
        if not text:
            return []
        return re.findall(r'@(\w+)', text)
    
    def _extract_urls(self, text):
        """استخراج الروابط"""
        import re
        if not text:
            return []
        return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
