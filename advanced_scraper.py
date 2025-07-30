#!/usr/bin/env python3
"""
Advanced Twitter Scraper with Enhanced Features
"""

import logging
import json
import os
import time
import sys
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Set, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    WebDriverException,
    StaleElementReferenceException
)
from config import USERS_TO_MONITOR, LOG_FILE, MAX_TWEETS_TO_SCRAPE

logger = logging.getLogger(__name__)

class AdvancedTwitterScraper:
    def __init__(self):
        self.seen_tweets_file = 'seen_tweets_advanced.json'
        self.seen_tweet_ids = self.load_seen_tweets()
        self.driver = None
        self.setup_driver()
        
    def setup_driver(self):
        """Setup Chrome driver with dedicated project profile"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Use dedicated project Chrome profile
            project_dir = os.path.dirname(os.path.abspath(__file__))
            chrome_profile_dir = os.path.join(project_dir, "chrome_profile")
            
            if not os.path.exists(chrome_profile_dir):
                os.makedirs(chrome_profile_dir)
                logger.info(f"Created dedicated Chrome profile directory: {chrome_profile_dir}")
            
            chrome_options.add_argument(f"--user-data-dir={chrome_profile_dir}")
            chrome_options.add_argument("--profile-directory=Default")
            logger.info(f"Using dedicated Chrome profile: {chrome_profile_dir}")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Advanced Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to setup Chrome driver: {e}")
            raise
    
    def load_seen_tweets(self) -> Set[str]:
        """Load previously seen tweet IDs from file"""
        try:
            if os.path.exists(self.seen_tweets_file):
                with open(self.seen_tweets_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('seen_tweets', []))
            return set()
        except Exception as e:
            logger.error(f"Error loading seen tweets: {e}")
            return set()
    
    def save_seen_tweets(self):
        """Save seen tweet IDs to file"""
        try:
            data = {
                'seen_tweets': list(self.seen_tweet_ids),
                'last_updated': datetime.now().isoformat()
            }
            with open(self.seen_tweets_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving seen tweets: {e}")
    
    def extract_advanced_tweet_data(self, tweet_element, username: str) -> Optional[Dict]:
        """Extract comprehensive tweet data including media, engagement, etc."""
        try:
            # Basic tweet data
            basic_data = self._extract_basic_tweet_data(tweet_element, username)
            if not basic_data:
                return None
            
            # Enhanced data extraction
            enhanced_data = {
                **basic_data,
                'media': self._extract_media_info(tweet_element),
                'engagement': self._extract_engagement_metrics(tweet_element),
                'hashtags': self._extract_hashtags(basic_data['text']),
                'mentions': self._extract_mentions(basic_data['text']),
                'links': self._extract_links(basic_data['text']),
                'language': self._detect_language(basic_data['text']),
                'sentiment': self._analyze_sentiment(basic_data['text']),
                'tweet_type': self._determine_tweet_type(tweet_element),
                'is_pinned': self._is_pinned_tweet(tweet_element),
                'has_poll': self._has_poll(tweet_element),
                'has_thread': self._is_thread_tweet(tweet_element)
            }
            
            return enhanced_data
            
        except Exception as e:
            logger.error(f"Error extracting advanced tweet data: {e}")
            return None
    
    def _extract_basic_tweet_data(self, tweet_element, username: str) -> Optional[Dict]:
        """Extract basic tweet information"""
        try:
            # Get tweet text with multiple selectors
            tweet_text = self._extract_tweet_text(tweet_element)
            if not tweet_text:
                return None
            
            # Get tweet ID
            tweet_id = self._extract_tweet_id(tweet_element)
            if not tweet_id:
                return None
            
            # Get timestamp
            created_at = self._extract_timestamp(tweet_element)
            
            return {
                'id': tweet_id,
                'text': tweet_text,
                'created_at': created_at,
                'username': username,
                'type': 'original'
            }
            
        except Exception as e:
            logger.error(f"Error extracting basic tweet data: {e}")
            return None
    
    def _extract_tweet_text(self, tweet_element) -> str:
        """Extract tweet text with multiple strategies"""
        text_selectors = [
            '[data-testid="tweetText"]',
            '[data-testid="tweet"] span',
            'div[lang]',
            'article span',
            '[role="text"]'
        ]
        
        for selector in text_selectors:
            try:
                text_elements = tweet_element.find_elements(By.CSS_SELECTOR, selector)
                if text_elements:
                    text = text_elements[0].text.strip()
                    if text:
                        return text
            except Exception:
                continue
        
        return ""
    
    def _extract_tweet_id(self, tweet_element) -> str:
        """Extract tweet ID from various sources"""
        # Try link-based extraction
        link_selectors = [
            'a[href*="/status/"]',
            'a[href*="twitter.com"]',
            'a'
        ]
        
        for selector in link_selectors:
            try:
                link_elements = tweet_element.find_elements(By.CSS_SELECTOR, selector)
                for link in link_elements:
                    href = link.get_attribute('href')
                    if href and '/status/' in href:
                        return href.split('/status/')[-1].split('?')[0]
            except Exception:
                continue
        
        # Try data attribute
        try:
            tweet_id = tweet_element.get_attribute('data-tweet-id')
            if tweet_id:
                return tweet_id
        except Exception:
            pass
        
        return None
    
    def _extract_timestamp(self, tweet_element) -> datetime:
        """Extract timestamp with multiple strategies"""
        time_selectors = [
            'time',
            '[datetime]',
            'span[title*="202"]',
            '[data-testid="tweet"] time'
        ]
        
        for selector in time_selectors:
            try:
                time_elements = tweet_element.find_elements(By.CSS_SELECTOR, selector)
                for time_elem in time_elements:
                    # Try datetime attribute
                    time_attr = time_elem.get_attribute('datetime')
                    if time_attr:
                        try:
                            return datetime.fromisoformat(time_attr.replace('Z', '+00:00'))
                        except Exception:
                            continue
                    
                    # Try title attribute for relative time
                    title_attr = time_elem.get_attribute('title')
                    if title_attr and '202' in title_attr:
                        try:
                            if 'h' in title_attr:
                                hours = int(title_attr.replace('h', ''))
                                return datetime.now(timezone.utc) - timedelta(hours=hours)
                            elif 'd' in title_attr:
                                days = int(title_attr.replace('d', ''))
                                return datetime.now(timezone.utc) - timedelta(days=days)
                        except Exception:
                            continue
            except Exception:
                continue
        
        return datetime.now(timezone.utc)
    
    def _extract_media_info(self, tweet_element) -> Dict:
        """Extract media information (images, videos, GIFs)"""
        media_info = {
            'has_media': False,
            'images': [],
            'videos': [],
            'gifs': []
        }
        
        try:
            # Check for images
            image_selectors = [
                '[data-testid="tweetPhoto"]',
                'img[alt*="Image"]',
                'img[src*="media"]'
            ]
            
            for selector in image_selectors:
                try:
                    images = tweet_element.find_elements(By.CSS_SELECTOR, selector)
                    for img in images:
                        src = img.get_attribute('src')
                        alt = img.get_attribute('alt')
                        if src:
                            media_info['images'].append({
                                'src': src,
                                'alt': alt or 'Image'
                            })
                            media_info['has_media'] = True
                except Exception:
                    continue
            
            # Check for videos
            video_selectors = [
                '[data-testid="videoPlayer"]',
                'video',
                '[data-testid="tweetVideo"]'
            ]
            
            for selector in video_selectors:
                try:
                    videos = tweet_element.find_elements(By.CSS_SELECTOR, selector)
                    for video in videos:
                        src = video.get_attribute('src')
                        if src:
                            media_info['videos'].append({'src': src})
                            media_info['has_media'] = True
                except Exception:
                    continue
            
            # Check for GIFs
            gif_selectors = [
                '[data-testid="tweetPhoto"][alt*="GIF"]',
                'img[src*="gif"]'
            ]
            
            for selector in gif_selectors:
                try:
                    gifs = tweet_element.find_elements(By.CSS_SELECTOR, selector)
                    for gif in gifs:
                        src = gif.get_attribute('src')
                        if src and 'gif' in src.lower():
                            media_info['gifs'].append({'src': src})
                            media_info['has_media'] = True
                except Exception:
                    continue
                    
        except Exception as e:
            logger.debug(f"Error extracting media info: {e}")
        
        return media_info
    
    def _extract_engagement_metrics(self, tweet_element) -> Dict:
        """Extract engagement metrics (likes, retweets, replies, quotes)"""
        metrics = {
            'likes': 0,
            'retweets': 0,
            'replies': 0,
            'quotes': 0,
            'bookmarks': 0
        }
        
        try:
            # Like count
            like_selectors = [
                '[data-testid="like"]',
                '[data-testid="likeCount"]',
                'span[aria-label*="like"]'
            ]
            
            for selector in like_selectors:
                try:
                    like_elements = tweet_element.find_elements(By.CSS_SELECTOR, selector)
                    for elem in like_elements:
                        text = elem.text.strip()
                        if text and text.isdigit():
                            metrics['likes'] = int(text)
                            break
                except Exception:
                    continue
            
            # Retweet count
            retweet_selectors = [
                '[data-testid="retweet"]',
                '[data-testid="retweetCount"]',
                'span[aria-label*="retweet"]'
            ]
            
            for selector in retweet_selectors:
                try:
                    retweet_elements = tweet_element.find_elements(By.CSS_SELECTOR, selector)
                    for elem in retweet_elements:
                        text = elem.text.strip()
                        if text and text.isdigit():
                            metrics['retweets'] = int(text)
                            break
                except Exception:
                    continue
            
            # Reply count
            reply_selectors = [
                '[data-testid="reply"]',
                '[data-testid="replyCount"]',
                'span[aria-label*="reply"]'
            ]
            
            for selector in reply_selectors:
                try:
                    reply_elements = tweet_element.find_elements(By.CSS_SELECTOR, selector)
                    for elem in reply_elements:
                        text = elem.text.strip()
                        if text and text.isdigit():
                            metrics['replies'] = int(text)
                            break
                except Exception:
                    continue
                    
        except Exception as e:
            logger.debug(f"Error extracting engagement metrics: {e}")
        
        return metrics
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from tweet text"""
        hashtags = re.findall(r'#\w+', text)
        return [tag.lower() for tag in hashtags]
    
    def _extract_mentions(self, text: str) -> List[str]:
        """Extract mentions from tweet text"""
        mentions = re.findall(r'@\w+', text)
        return [mention.lower() for mention in mentions]
    
    def _extract_links(self, text: str) -> List[str]:
        """Extract links from tweet text"""
        url_pattern = r'https?://[^\s]+'
        return re.findall(url_pattern, text)
    
    def _detect_language(self, text: str) -> str:
        """Simple language detection"""
        # Basic language detection based on character sets
        if re.search(r'[\u4e00-\u9fff]', text):  # Chinese
            return 'zh'
        elif re.search(r'[\u3040-\u309f\u30a0-\u30ff]', text):  # Japanese
            return 'ja'
        elif re.search(r'[\uac00-\ud7af]', text):  # Korean
            return 'ko'
        elif re.search(r'[\u0600-\u06ff]', text):  # Arabic
            return 'ar'
        elif re.search(r'[\u0900-\u097f]', text):  # Hindi
            return 'hi'
        else:
            return 'en'  # Default to English
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        text_lower = text.lower()
        
        # Positive words
        positive_words = ['good', 'great', 'awesome', 'amazing', 'love', 'happy', 'excellent', 'wonderful', 'fantastic']
        # Negative words
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'sad', 'horrible', 'worst', 'disappointed', 'angry']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _determine_tweet_type(self, tweet_element) -> str:
        """Determine the type of tweet"""
        try:
            # Check for retweet indicators
            retweet_indicators = [
                '[data-testid="socialContext"]',
                'span[data-testid="retweet"]',
                'div[data-testid="retweet"]'
            ]
            
            for selector in retweet_indicators:
                if tweet_element.find_elements(By.CSS_SELECTOR, selector):
                    return 'retweet'
            
            # Check for quote tweet indicators
            quote_indicators = [
                '[data-testid="quote"]',
                'div[data-testid="quoteTweet"]'
            ]
            
            for selector in quote_indicators:
                if tweet_element.find_elements(By.CSS_SELECTOR, selector):
                    return 'quote'
            
            # Check for reply indicators
            reply_indicators = [
                '[data-testid="reply"]',
                'div[data-testid="reply"]'
            ]
            
            for selector in reply_indicators:
                if tweet_element.find_elements(By.CSS_SELECTOR, selector):
                    return 'reply'
            
            return 'original'
            
        except Exception as e:
            logger.debug(f"Error determining tweet type: {e}")
            return 'original'
    
    def _is_pinned_tweet(self, tweet_element) -> bool:
        """Check if tweet is pinned"""
        try:
            pinned_indicators = [
                '[data-testid="pin"]',
                'span[aria-label*="pinned"]',
                'div[data-testid="pinned"]'
            ]
            
            for selector in pinned_indicators:
                if tweet_element.find_elements(By.CSS_SELECTOR, selector):
                    return True
            
            return False
        except Exception:
            return False
    
    def _has_poll(self, tweet_element) -> bool:
        """Check if tweet contains a poll"""
        try:
            poll_selectors = [
                '[data-testid="poll"]',
                'div[data-testid="poll"]',
                '[data-testid="pollOption"]'
            ]
            
            for selector in poll_selectors:
                if tweet_element.find_elements(By.CSS_SELECTOR, selector):
                    return True
            
            return False
        except Exception:
            return False
    
    def _is_thread_tweet(self, tweet_element) -> bool:
        """Check if tweet is part of a thread"""
        try:
            thread_indicators = [
                '[data-testid="thread"]',
                'div[data-testid="thread"]',
                '[data-testid="threadConnector"]'
            ]
            
            for selector in thread_indicators:
                if tweet_element.find_elements(By.CSS_SELECTOR, selector):
                    return True
            
            return False
        except Exception:
            return False
    
    def get_user_tweets(self, username: str) -> List[Dict]:
        """Get advanced tweet data for a user"""
        # This would use the same navigation logic as the basic scraper
        # but with enhanced data extraction
        # Implementation would be similar to the basic scraper but using extract_advanced_tweet_data
        pass
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Advanced Chrome driver closed successfully")
            except WebDriverException as e:
                logger.warning(f"Error closing Chrome driver: {e}")
            except Exception as e:
                logger.error(f"Unexpected error during cleanup: {e}")
            finally:
                self.driver = None 