#!/usr/bin/env python3
"""
YAP Search Scraper - Scrapes tweets from Twitter search based on YAP query
"""

import logging
import json
import os
import time
import sys
import re
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
from config import (
    MAX_TWEETS_TO_SCRAPE,
    YAP_SEARCH_KEYWORDS,
    YAP_FILTER_VERIFIED,
    YAP_FILTER_NATIVE_RETWEETS,
    YAP_FILTER_RETWEETS,
    YAP_FILTER_REPLIES,
    YAP_MIN_REPLIES,
    YAP_MIN_LIKES,
    YAP_MIN_RETWEETS,
    YAP_LANGUAGE,
    YAP_TIME_WINDOW,
    YAP_FILTER_LINKS,
    YAP_FILTER_MEDIA,
    YAP_FILTER_IMAGES,
    YAP_FILTER_VIDEOS,
    YAP_SEARCH_SOURCE,
    CHROME_PROFILE_YAP,
    CHROME_BINARY_PATH
)
import psutil
import subprocess
from robust_notifier import RobustTelegramNotifier

logger = logging.getLogger(__name__)

class YapSearchScraper:
    def __init__(self):
        self.driver = None
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Kill any existing Chrome processes for this project
        self._kill_existing_chrome()
        
        # Setup driver with unique profile
        self.setup_driver()
        self.output_file = 'yap_links.txt'
        
    def _kill_existing_chrome(self):
        """Kill ALL Chrome processes to ensure clean environment"""
        try:
            logger.info("🔪 Killing ALL Chrome processes for clean environment...")
            
            killed_count = 0
            
            # Kill all Chrome and ChromeDriver processes
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    proc_name = proc.info['name']
                    if proc_name and ('chrome' in proc_name.lower() or 'chromedriver' in proc_name.lower()):
                        logger.info(f"Killing Chrome process: {proc.pid} ({proc_name})")
                        proc.terminate()
                        proc.wait(timeout=3)
                        killed_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                    try:
                        # Force kill if terminate fails
                        proc.kill()
                        killed_count += 1
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                except Exception as e:
                    logger.warning(f"Error killing process {proc.pid}: {e}")
            
            # Also use system commands for extra cleanup
            try:
                import subprocess
                # Kill Chrome processes using system commands
                subprocess.run(['pkill', '-f', 'chrome'], capture_output=True, timeout=5)
                subprocess.run(['pkill', '-f', 'chromedriver'], capture_output=True, timeout=5)
                subprocess.run(['pkill', '-f', 'google-chrome'], capture_output=True, timeout=5)
            except Exception as e:
                logger.warning(f"Error using system commands to kill Chrome: {e}")
            
            # Wait for processes to fully terminate
            time.sleep(3)
            
            logger.info(f"✅ Killed {killed_count} Chrome processes")
                    
        except Exception as e:
            logger.warning(f"Error killing existing Chrome processes: {e}")
    
    def setup_driver(self):
        """Setup Chrome driver with unique YAP profile directory"""
        try:
            import uuid
            
            # Create unique profile directory in /tmp for this instance
            unique_profile = f"/tmp/chrome_profile_yap_{uuid.uuid4().hex[:8]}"
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
    
    def clear_output_file(self):
        """Clear the output file contents"""
        try:
            # Get absolute path for the output file
            import os
            project_dir = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.join(project_dir, self.output_file)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('')  # Clear file contents
            logger.info(f"Cleared {output_path}")
        except Exception as e:
            logger.error(f"Error clearing output file: {e}")
    
    def save_tweet_urls(self, urls):
        """Save tweet URLs to file"""
        try:
            project_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(project_dir, 'yap_links.txt')
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for url in urls:
                    f.write(f"{url}\n")
            
            logger.info(f"Saved {len(urls)} tweet URLs to {output_file}")
            
            # Send file to Telegram
            self.send_yap_links_to_telegram(output_file, len(urls))
            
        except Exception as e:
            logger.error(f"Error saving tweet URLs: {e}")

    def send_yap_links_to_telegram(self, file_path, url_count):
        """Send YAP links file to Telegram"""
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
            caption = f"🔗 YAP Search Results\n\n📊 Found {url_count} tweet URLs\n📅 {time.strftime('%Y-%m-%d %H:%M:%S')}"
            
            success = notifier.send_document(file_path, caption)
            
            if success:
                logger.info(f"✅ Successfully sent YAP links file to Telegram ({url_count} URLs)")
            else:
                logger.error("❌ Failed to send YAP links file to Telegram")
                
        except Exception as e:
            logger.error(f"Error sending YAP links to Telegram: {e}")
    
    def get_yap_search_tweets(self):
        """Get tweets from YAP search query"""
        try:
            # Build search query from config
            search_query = self._build_yap_search_query()
            
            # Navigate to search page
            base_url = "https://x.com/search"
            query_params = {
                'q': search_query,
                'src': YAP_SEARCH_SOURCE
            }
            
            from urllib.parse import urlencode
            search_url = f"{base_url}?{urlencode(query_params)}"
            
            logger.info(f"Navigating to YAP search: {search_url}")
            self.driver.get(search_url)
            
            # Wait for tweets to load
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]'))
            )
            
            # Wait 10 seconds for initial content to load
            logger.info("Waiting 10 seconds for initial content to load...")
            time.sleep(10)
            
            # Start with initial extraction
            all_urls = []
            seen_urls = set()
            scroll_count = 0
            max_scrolls = 15  # Increased scroll iterations
            no_new_urls_count = 0
            
            logger.info(f"Starting extraction with up to {max_scrolls} scroll iterations...")
            
            for scroll_iteration in range(max_scrolls):
                logger.info(f"Scroll iteration {scroll_iteration + 1}/{max_scrolls}")
                
                # Extract URLs from current page
                current_urls = self._extract_urls_from_current_page()
                new_urls = []
                
                # Find new URLs
                for url in current_urls:
                    if url not in seen_urls:
                        new_urls.append(url)
                        seen_urls.add(url)
                
                if new_urls:
                    all_urls.extend(new_urls)
                    logger.info(f"Found {len(new_urls)} new URLs in iteration {scroll_iteration + 1}. Total: {len(all_urls)}")
                    no_new_urls_count = 0  # Reset counter
                else:
                    no_new_urls_count += 1
                    logger.info(f"No new URLs found in iteration {scroll_iteration + 1}. No new URLs count: {no_new_urls_count}")
                
                # Check if we have enough URLs
                if len(all_urls) >= MAX_TWEETS_TO_SCRAPE:
                    logger.info(f"Reached target of {MAX_TWEETS_TO_SCRAPE} URLs, stopping")
                    break
                
                # Check if we're not finding new URLs for too long
                if no_new_urls_count >= 3:
                    logger.info("No new URLs found for 3 consecutive iterations, stopping")
                    break
                
                # Scroll down for next iteration
                if scroll_iteration < max_scrolls - 1:  # Don't scroll on last iteration
                    logger.info("Scrolling down to load more tweets...")
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(5)  # Wait for new content to load
                    
                    # Wait for new content to appear
                    self._wait_for_new_content()
            
            logger.info(f"Extraction completed. Total unique URLs found: {len(all_urls)}")
            return all_urls
                
        except Exception as e:
            logger.error(f"Error getting YAP search tweets: {e}")
            return []

    def _extract_urls_from_current_page(self):
        """Extract tweet URLs from the current page"""
        urls = []
        
        try:
            # Find all tweet elements
            tweet_elements = self._find_tweet_elements_enhanced()
            
            if not tweet_elements:
                logger.warning("No tweet elements found on page")
                return urls
            
            logger.info(f"Found {len(tweet_elements)} tweet elements on page")
            
            # Extract URLs from each tweet
            for i, tweet in enumerate(tweet_elements[:MAX_TWEETS_TO_SCRAPE]):
                try:
                    url = self._extract_tweet_url(tweet)
                    if url and url not in urls:
                        urls.append(url)
                        logger.info(f"Extracted URL {len(urls)}: {url}")
                        
                        if len(urls) >= MAX_TWEETS_TO_SCRAPE:
                            logger.info(f"Reached target of {MAX_TWEETS_TO_SCRAPE} URLs")
                            break
                            
                except StaleElementReferenceException:
                    logger.warning(f"Tweet element {i} became stale, skipping")
                    continue
                except Exception as e:
                    logger.warning(f"Error extracting URL from tweet {i}: {e}")
                    continue
            
            logger.info(f"Successfully extracted {len(urls)} unique URLs")
            return urls
            
        except Exception as e:
            logger.error(f"Error extracting URLs from current page: {e}")
            return urls
    
    def _build_yap_search_query(self) -> str:
        """Build the YAP search query using configurable parameters"""
        query_parts = []
        
        # Add keywords (REQUIRED)
        query_parts.append(YAP_SEARCH_KEYWORDS)
        
        # Add verification filter
        if YAP_FILTER_VERIFIED:
            query_parts.append("filter:blue_verified")
        
        # Add content type filters
        if YAP_FILTER_NATIVE_RETWEETS:
            query_parts.append("-filter:nativeretweets")
        
        if YAP_FILTER_RETWEETS:
            query_parts.append("-filter:retweets")
        
        if YAP_FILTER_REPLIES:
            query_parts.append("-filter:replies")
        
        # Add engagement filters
        if YAP_MIN_REPLIES > 0:
            query_parts.append(f"min_replies:{YAP_MIN_REPLIES}")
        
        if YAP_MIN_LIKES > 0:
            query_parts.append(f"min_faves:{YAP_MIN_LIKES}")
        
        if YAP_MIN_RETWEETS > 0:
            query_parts.append(f"min_retweets:{YAP_MIN_RETWEETS}")
        
        # Add language filter
        if YAP_LANGUAGE:
            query_parts.append(f"lang:{YAP_LANGUAGE}")
        
        # Add time window filter
        if YAP_TIME_WINDOW > 0:
            query_parts.append(f"within_time:{YAP_TIME_WINDOW}min")
        
        # Add additional filters
        if YAP_FILTER_LINKS:
            query_parts.append("filter:links")
        
        if YAP_FILTER_MEDIA:
            query_parts.append("filter:media")
        
        if YAP_FILTER_IMAGES:
            query_parts.append("filter:images")
        
        if YAP_FILTER_VIDEOS:
            query_parts.append("filter:videos")
        
        # Join all parts with spaces
        final_query = " ".join(query_parts)
        
        logger.info(f"Built search query: {final_query}")
        return final_query
    
    def _find_tweet_elements_enhanced(self):
        """Find tweet elements using multiple selectors"""
        selectors = [
            '[data-testid="tweet"]',
            'article[data-testid="tweet"]',
            'div[data-testid="tweet"]',
            'article[role="article"]',
            'div[role="article"]'
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    logger.info(f"Found {len(elements)} tweet elements using selector: {selector}")
                    return elements
            except Exception as e:
                logger.warning(f"Selector {selector} failed: {e}")
                continue
        
        logger.warning("No tweet elements found with any selector")
        return []

    def _extract_tweet_url(self, tweet_element):
        """Extract tweet URL from tweet element"""
        try:
            # Try multiple selectors for tweet links
            link_selectors = [
                'a[href*="/status/"]',
                'a[data-testid="tweetText"]',
                'a[href*="x.com/status/"]',
                'a[href*="twitter.com/status/"]'
            ]
            
            for selector in link_selectors:
                try:
                    link = tweet_element.find_element(By.CSS_SELECTOR, selector)
                    href = link.get_attribute('href')
                    if href and '/status/' in href:
                        return href
                except:
                    continue
            
            # Fallback: try to construct URL from tweet ID
            try:
                tweet_id = tweet_element.get_attribute('data-tweet-id')
                if tweet_id:
                    return f"https://x.com/i/status/{tweet_id}"
            except:
                pass
            
            return None
            
        except Exception as e:
            logger.warning(f"Error extracting tweet URL: {e}")
            return None
    
    def run_yap_scraper(self):
        """Run the YAP scraper"""
        try:
            logger.info("Starting YAP search scraper...")
            
            # Clear output file
            self.clear_output_file()
            
            # Get tweet URLs
            urls = self.get_yap_search_tweets()
            
            if urls:
                logger.info(f"Found {len(urls)} tweet URLs")
                self.save_tweet_urls(urls)
                return True
            else:
                logger.warning("No tweet URLs found")
                return False
                
        except Exception as e:
            logger.error(f"Error in YAP scraper: {e}")
            return False
    
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

    def _wait_for_new_content(self):
        """Wait for new content to load after scrolling"""
        try:
            # Wait for loading indicators to disappear
            loading_selectors = [
                '[data-testid="loading"]',
                '.loading',
                '[aria-label*="Loading"]',
                '[data-testid="spinner"]'
            ]
            
            for selector in loading_selectors:
                try:
                    WebDriverWait(self.driver, 3).until_not(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                except TimeoutException:
                    pass  # No loading indicator found
            
            # Wait a bit more for content to settle
            time.sleep(2)
            
        except Exception as e:
            logger.debug(f"Error waiting for new content: {e}") 