#!/usr/bin/env python3
"""
Twitter Monitor using Web Scraping (Selenium)
Alternative to API approach - no rate limits!
"""

import logging
import json
import os
import time
import sys
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Set, Optional
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
from config import USERS_TO_MONITOR, LOG_FILE, MAX_TWEETS_TO_SCRAPE, CHROME_PROFILE_USER, CHROME_BINARY_PATH
import psutil
import subprocess
from robust_notifier import RobustTelegramNotifier

logger = logging.getLogger(__name__)

class TwitterScraperMonitor:
    def __init__(self):
        self.seen_tweets_file = 'seen_tweets_scraper.json'
        self.seen_tweet_ids = self.load_seen_tweets()
        self.driver = None
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Kill any existing Chrome processes for this project
        self._kill_existing_chrome()
        
        # Setup driver with unique profile
        self.setup_driver()
        self.user_links_file = 'users_tweetlinks.txt'
        
    def _kill_existing_chrome(self):
        """Kill any Chrome processes that might interfere"""
        try:
            # Since we're using unique profiles, we can be less aggressive
            # Just kill any Chrome processes that might be hanging
            chrome_processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name']
                    if proc_name and 'chrome' in proc_name.lower():
                        chrome_processes.append(proc)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if chrome_processes:
                logger.info(f"Found {len(chrome_processes)} Chrome processes, killing them...")
                for proc in chrome_processes:
                    try:
                        logger.info(f"Killing Chrome process: {proc.pid}")
                        proc.terminate()
                        proc.wait(timeout=3)
                    except psutil.TimeoutExpired:
                        proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            else:
                logger.info("No Chrome processes found")
                    
        except Exception as e:
            logger.warning(f"Error killing existing Chrome processes: {e}")
    
    def setup_driver(self):
        """Setup Chrome driver with unique user profile directory"""
        try:
            import uuid
            
            # Create unique profile directory in /tmp for this instance
            unique_profile = f"/tmp/chrome_profile_user_{uuid.uuid4().hex[:8]}"
            profile_dir = unique_profile
            
            # Ensure the directory exists
            os.makedirs(profile_dir, exist_ok=True)
            
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = CHROME_BINARY_PATH
            chrome_options.add_argument(f'--user-data-dir={profile_dir}')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-logging')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument('--silent')
            chrome_options.add_argument('--disable-remote-fonts')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Suppress verbose logging
            logging.getLogger('selenium').setLevel(logging.ERROR)
            logging.getLogger('urllib3').setLevel(logging.ERROR)
            logging.getLogger('httpx').setLevel(logging.ERROR)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info(f"Chrome driver initialized successfully with unique profile: {profile_dir}")
            
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
    
    def get_user_tweets(self, username: str) -> List[Dict]:
        """Get tweets from a specific user"""
        try:
            # Navigate to user's profile
            profile_url = f"https://twitter.com/{username}"
            self.driver.get(profile_url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]'))
            )
            
            # Handle any popups that might appear
            self._handle_popups()
            
            # Scroll to load more tweets
            self._scroll_to_load_tweets()
            
            # Find tweet elements
            tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
            
            if not tweet_elements:
                logger.warning(f"No tweet elements found for @{username}")
                return []
            
            logger.info(f"Found {len(tweet_elements)} tweet elements for @{username}")
            
            # Extract tweet data
            tweets = []
            for tweet_element in tweet_elements[:MAX_TWEETS_TO_SCRAPE]:
                try:
                    tweet_data = self.extract_tweet_data(tweet_element, username)
                    if tweet_data:
                        tweets.append(tweet_data)
                except Exception as e:
                    logger.error(f"Error extracting tweet data: {e}")
                    continue
            
            logger.info(f"Successfully extracted {len(tweets)} tweets for @{username}")
            return tweets
            
        except Exception as e:
            logger.error(f"Error getting tweets for @{username}: {e}")
            return []
    
    def _handle_popups(self):
        """Handle various popups and dialogs"""
        popup_selectors = [
            '[data-testid="app-bar-close"]',
            '[data-testid="sheetDialog"] button',
            '[data-testid="modal"] button',
            'button[aria-label*="Close"]',
            'button[aria-label*="close"]'
        ]
        
        for selector in popup_selectors:
            try:
                close_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if close_buttons:
                    close_buttons[0].click()
                    time.sleep(1)
                    break
            except Exception as e:
                logger.debug(f"Could not close popup with selector {selector}: {e}")
    
    def _wait_for_tweets_alternative(self) -> bool:
        """Try alternative selectors if main selector fails"""
        alternative_selectors = [
            '[data-testid="tweet"]',
            'article[data-testid="tweet"]',
            'div[data-testid="tweet"]',
            'article',
            '[role="article"]'
        ]
        
        for selector in alternative_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    return True
            except Exception as e:
                logger.debug(f"Alternative selector {selector} failed: {e}")
        
        return False
    
    def _scroll_to_load_tweets(self):
        """Scroll to load more tweets"""
        try:
            # Scroll multiple times to ensure we get recent tweets
            for i in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Scroll back up to get recent tweets
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
                
            logger.debug("Scrolled to load tweets")
        except Exception as e:
            logger.error(f"Error scrolling: {e}")
    
    def _find_tweet_elements(self) -> List:
        """Find tweet elements with retry mechanism"""
        selectors = [
            '[data-testid="tweet"]',
            'article[data-testid="tweet"]',
            'div[data-testid="tweet"]'
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    return elements
            except Exception as e:
                logger.debug(f"Selector {selector} failed: {e}")
        
        return []
    
    def _process_tweets(self, tweets: List[Dict], username: str) -> List[Dict]:
        """Process tweets and filter for new ones"""
        try:
            new_tweets = []
            
            for tweet in tweets:
                if tweet and 'id' in tweet:
                    tweet_id = tweet['id']
                    
                    # Check if we've seen this tweet before
                    if tweet_id not in self.seen_tweet_ids:
                        # Check if tweet is within the last hour
                        if self._is_tweet_recent(tweet):
                            new_tweets.append(tweet)
                            self.seen_tweet_ids.add(tweet_id)
                            logger.info(f"New tweet found: {tweet_id} for @{username}")
                        else:
                            logger.debug(f"Tweet {tweet_id} is too old for @{username}")
                    else:
                        logger.debug(f"Tweet {tweet_id} already seen for @{username}")
            
            # Save updated seen tweets
            if new_tweets:
                self.save_seen_tweets()
            
            return new_tweets
            
        except Exception as e:
            logger.error(f"Error processing tweets for @{username}: {e}")
            return []
    
    def _is_tweet_recent(self, tweet: Dict) -> bool:
        """Check if tweet is within the last hour"""
        try:
            if 'created_at' not in tweet:
                return True  # Assume recent if we can't determine time
            
            tweet_time = tweet['created_at']
            current_time = datetime.now(timezone.utc)
            
            # Calculate time difference
            time_diff = current_time - tweet_time
            
            # Check if tweet is within the last hour
            return time_diff.total_seconds() <= 3600  # 1 hour = 3600 seconds
            
        except Exception as e:
            logger.error(f"Error checking tweet recency: {e}")
            return True  # Assume recent if we can't determine
    
    def _extract_tweet_data_with_retry(self, tweet_element, username: str) -> Optional[Dict]:
        """Extract tweet data with retry mechanism"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return self.extract_tweet_data(tweet_element, username)
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    logger.debug(f"Tweet element stale, retrying... (attempt {attempt + 1})")
                    time.sleep(0.5)
                    continue
                else:
                    logger.warning("Tweet element became stale after retries")
                    return None
            except Exception as e:
                logger.error(f"Error extracting tweet data (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(0.5)
                    continue
                else:
                    return None
        return None
    
    def _is_original_tweet_with_retry(self, tweet_element) -> bool:
        """Check if tweet is original with retry mechanism"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return self.is_original_tweet(tweet_element)
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    logger.debug(f"Tweet element stale during type check, retrying... (attempt {attempt + 1})")
                    time.sleep(0.5)
                    continue
                else:
                    logger.warning("Tweet element became stale during type check")
                    return True  # Assume original if we can't determine
            except Exception as e:
                logger.error(f"Error checking tweet type (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(0.5)
                    continue
                else:
                    return True  # Assume original if we can't determine
        return True
    
    def extract_tweet_data(self, tweet_element, username: str) -> Dict:
        """Extract tweet data from a tweet element"""
        try:
            # Try multiple selectors for tweet text
            text_selectors = [
                'div[data-testid="tweetText"]',
                'div[lang]',  # Language attribute often indicates text content
                'div[dir="ltr"]',  # Left-to-right text direction
                'span[dir="ltr"]',
                'div[data-testid="tweet"] div[lang]',
                'div[data-testid="tweet"] span[dir="ltr"]',
                'article div[lang]',
                'article span[dir="ltr"]'
            ]
            
            tweet_text = ""
            for selector in text_selectors:
                try:
                    text_elements = tweet_element.find_elements(By.CSS_SELECTOR, selector)
                    for element in text_elements:
                        text = element.text.strip()
                        if text and len(text) > 10:  # Minimum meaningful text length
                            tweet_text = text
                            break
                    if tweet_text:
                        break
                except Exception:
                    continue
            
            # If still no text, try a broader approach for media tweets
            if not tweet_text:
                try:
                    # Look for any text content within the tweet
                    all_text_elements = tweet_element.find_elements(By.CSS_SELECTOR, 'div, span')
                    for element in all_text_elements:
                        text = element.text.strip()
                        if text and len(text) > 10 and not text.startswith('@') and not text.startswith('#'):
                            # Avoid usernames and hashtags as main content
                            tweet_text = text
                            break
                except Exception:
                    pass
            
            # If still no text, try to get any available text
            if not tweet_text:
                try:
                    # Last resort: get all text from the tweet
                    all_text = tweet_element.text
                    lines = all_text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and len(line) > 10 and not line.startswith('@') and not line.startswith('#'):
                            tweet_text = line
                            break
                except Exception:
                    pass
            
            # If we still don't have text, create a placeholder
            if not tweet_text:
                tweet_text = "[Media tweet - text not available]"
                logger.warning(f"Could not extract tweet text for @{username}")
            
            # Extract tweet ID from URL or data attribute
            tweet_id = self.extract_tweet_id(tweet_element)
            
            # Extract timestamp
            timestamp = self.extract_timestamp(tweet_element)
            
            # Determine tweet type
            tweet_type = self.determine_tweet_type(tweet_element)
            
            return {
                'id': tweet_id,
                'text': tweet_text,
                'username': username,
                'created_at': timestamp,
                'type': tweet_type
            }
            
        except Exception as e:
            logger.error(f"Error extracting tweet data: {e}")
            return None
    
    def is_original_tweet(self, tweet_element) -> bool:
        """Check if tweet is original (not retweet/quote)"""
        try:
            # Look for retweet indicators
            retweet_indicators = tweet_element.find_elements(By.CSS_SELECTOR, '[data-testid="socialContext"]')
            if retweet_indicators:
                return False
            
            # Look for quote tweet indicators
            quote_indicators = tweet_element.find_elements(By.CSS_SELECTOR, '[data-testid="quote"]')
            if quote_indicators:
                return False
            
            return True
            
        except Exception as e:
            logger.debug(f"Error checking tweet type: {e}")
            return True  # Assume original if we can't determine
    
    def check_new_tweets(self):
        """Check for new tweets from all monitored users"""
        try:
            all_tweet_urls = []
            new_tweets = []
            
            for username in USERS_TO_MONITOR:
                try:
                    logger.info(f"Checking tweets for @{username}...")
                    user_tweets = self.get_user_tweets(username)
                    
                    if user_tweets:
                        processed_tweets = self._process_tweets(user_tweets, username)
                        new_tweets.extend(processed_tweets)
                        
                        # Collect tweet URLs
                        for tweet in user_tweets:
                            if 'id' in tweet:
                                tweet_url = self.format_tweet_url(username, tweet['id'])
                                all_tweet_urls.append(tweet_url)
                    
                    # Small delay between users
                    time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Error checking tweets for @{username}: {e}")
                    continue
            
            # Save all collected tweet URLs
            if all_tweet_urls:
                self.save_user_tweet_urls(all_tweet_urls)
            
            return new_tweets
            
        except Exception as e:
            logger.error(f"Error in check_new_tweets: {e}")
            return []
    
    def quit_chrome_after_task(self):
        """Quit Chrome after completing a task"""
        try:
            if self.driver:
                logger.info("Quitting Chrome after task completion...")
                self.driver.quit()
                self.driver = None
                logger.info("Chrome quit successfully")
        except Exception as e:
            logger.error(f"Error quitting Chrome: {e}")
            self._force_kill_chrome()
    
    def reopen_chrome_for_next_check(self):
        """Reopen Chrome for the next check"""
        try:
            logger.info("Reopening Chrome for next check...")
            self.setup_driver()
            logger.info("Chrome reopened successfully")
        except Exception as e:
            logger.error(f"Error reopening Chrome: {e}")
            raise
    
    def save_user_tweet_urls(self, all_tweet_urls):
        """Save user tweet URLs to file and send to Telegram"""
        try:
            if not all_tweet_urls:
                logger.info("No user tweet URLs to save")
                return
            
            project_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(project_dir, 'users_tweetlinks.txt')
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for url in all_tweet_urls:
                    f.write(f"{url}\n")
            
            logger.info(f"Saved {len(all_tweet_urls)} user tweet URLs to {output_file}")
            
            # Send file to Telegram
            self.send_user_links_to_telegram(output_file, len(all_tweet_urls))
            
        except Exception as e:
            logger.error(f"Error saving user tweet URLs: {e}")

    def send_user_links_to_telegram(self, file_path, url_count):
        """Send user tweet links file to Telegram"""
        try:
            if not os.path.exists(file_path):
                logger.warning(f"File {file_path} does not exist, skipping Telegram send")
                return
            
            # Check if file has content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    logger.warning("File is empty, skipping Telegram send")
                    return
            
            # Initialize Telegram notifier
            notifier = RobustTelegramNotifier()
            
            # Send file with caption
            caption = f"👥 User Tweet Monitoring Results\n\n📊 Found {url_count} tweet URLs\n📅 {time.strftime('%Y-%m-%d %H:%M:%S')}"
            
            success = notifier.send_document(file_path, caption)
            
            if success:
                logger.info(f"✅ Successfully sent user tweet links file to Telegram ({url_count} URLs)")
            else:
                logger.error("❌ Failed to send user tweet links file to Telegram")
                
        except Exception as e:
            logger.error(f"Error sending user tweet links to Telegram: {e}")
    
    def format_tweet_url(self, username: str, tweet_id: str) -> str:
        """Generate tweet URL"""
        return f"https://twitter.com/{username}/status/{tweet_id}"
    
    def format_created_at(self, created_at) -> str:
        """Format tweet creation time"""
        if created_at:
            return created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
        return "Unknown time"
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                logger.info("Chrome driver quit successfully")
            
            # Clean up any profile directories in /tmp
            self._cleanup_tmp_profiles()
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def _cleanup_tmp_profiles(self):
        """Clean up Chrome profile directories in /tmp"""
        try:
            import glob
            import shutil
            
            # Find and remove Chrome profile directories in /tmp
            tmp_profiles = glob.glob("/tmp/chrome_profile_*")
            for profile in tmp_profiles:
                try:
                    if os.path.isdir(profile):
                        shutil.rmtree(profile)
                        logger.info(f"Cleaned up profile: {profile}")
                except Exception as e:
                    logger.warning(f"Failed to clean up profile {profile}: {e}")
                    
        except Exception as e:
            logger.warning(f"Error cleaning up /tmp profiles: {e}")
    
    def _force_kill_chrome(self):
        """Force kill Chrome processes if normal cleanup fails"""
        try:
            logger.info("Force killing Chrome processes...")
            
            # Kill Chrome processes on Windows
            if os.name == 'nt':
                subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], 
                             capture_output=True, timeout=10)
                subprocess.run(['taskkill', '/f', '/im', 'chromedriver.exe'], 
                             capture_output=True, timeout=10)
            else:
                # Kill Chrome processes on Unix-like systems
                subprocess.run(['pkill', '-f', 'chrome'], 
                             capture_output=True, timeout=10)
                subprocess.run(['pkill', '-f', 'chromedriver'], 
                             capture_output=True, timeout=10)
                
        except Exception as e:
            logger.error(f"Error force killing Chrome: {e}") 

    def extract_tweet_id(self, tweet_element) -> str:
        """Extract tweet ID from tweet element"""
        try:
            # Try multiple approaches to get tweet ID
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
                            tweet_id = href.split('/status/')[-1].split('?')[0]
                            if tweet_id and tweet_id.isdigit():
                                return tweet_id
                except Exception:
                    continue
            
            # Fallback: generate a timestamp-based ID
            return str(int(time.time()))
            
        except Exception as e:
            logger.error(f"Error extracting tweet ID: {e}")
            return str(int(time.time()))
    
    def extract_timestamp(self, tweet_element) -> datetime:
        """Extract timestamp from tweet element"""
        try:
            # Default to current time
            created_at = datetime.now(timezone.utc)
            
            time_selectors = [
                'time',
                '[datetime]',
                'span[title*="202"]'  # Look for year in title
            ]
            
            for selector in time_selectors:
                try:
                    time_elements = tweet_element.find_elements(By.CSS_SELECTOR, selector)
                    for time_elem in time_elements:
                        # Try datetime attribute first
                        time_attr = time_elem.get_attribute('datetime')
                        if time_attr:
                            try:
                                created_at = datetime.fromisoformat(time_attr.replace('Z', '+00:00'))
                                return created_at
                            except Exception:
                                continue
                        
                        # Try title attribute
                        title_attr = time_elem.get_attribute('title')
                        if title_attr and '202' in title_attr:
                            # Parse relative time like "2h" or "1d"
                            try:
                                if 'h' in title_attr:
                                    hours = int(title_attr.replace('h', ''))
                                    created_at = datetime.now(timezone.utc) - timedelta(hours=hours)
                                elif 'd' in title_attr:
                                    days = int(title_attr.replace('d', ''))
                                    created_at = datetime.now(timezone.utc) - timedelta(days=days)
                                return created_at
                            except Exception:
                                continue
                except Exception:
                    continue
            
            return created_at
            
        except Exception as e:
            logger.error(f"Error extracting timestamp: {e}")
            return datetime.now(timezone.utc)
    
    def determine_tweet_type(self, tweet_element) -> str:
        """Determine if tweet is original, retweet, or quote"""
        try:
            # Check for retweet indicators
            retweet_selectors = [
                '[data-testid="socialContext"]',
                'span[data-testid="socialContext"]',
                'div[data-testid="socialContext"]'
            ]
            
            for selector in retweet_selectors:
                try:
                    elements = tweet_element.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        text = elements[0].text.lower()
                        if 'retweeted' in text:
                            return 'retweet'
                        elif 'quoted' in text:
                            return 'quote'
                except Exception:
                    continue
            
            # Check for quote tweet indicators
            quote_selectors = [
                '[data-testid="quote"]',
                'div[data-testid="quote"]'
            ]
            
            for selector in quote_selectors:
                try:
                    elements = tweet_element.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        return 'quote'
                except Exception:
                    continue
            
            return 'original'
            
        except Exception as e:
            logger.error(f"Error determining tweet type: {e}")
            return 'original' 