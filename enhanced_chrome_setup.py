#!/usr/bin/env python3
"""
Enhanced Chrome setup for VPS deployment
"""

import os
import subprocess
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_enhanced_chrome():
    """Setup Chrome with enhanced options for VPS"""
    try:
        chrome_options = Options()
        
        # Essential VPS options
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-javascript')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--disable-translate')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--mute-audio')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-prompt-on-repost')
        chrome_options.add_argument('--disable-hang-monitor')
        chrome_options.add_argument('--disable-client-side-phishing-detection')
        chrome_options.add_argument('--disable-component-update')
        chrome_options.add_argument('--disable-domain-reliability')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-sync')
        chrome_options.add_argument('--disable-translate')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('--mute-audio')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-prompt-on-repost')
        chrome_options.add_argument('--disable-hang-monitor')
        chrome_options.add_argument('--disable-client-side-phishing-detection')
        chrome_options.add_argument('--disable-component-update')
        chrome_options.add_argument('--disable-domain-reliability')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        
        # Memory optimization
        chrome_options.add_argument('--memory-pressure-off')
        chrome_options.add_argument('--max_old_space_size=512')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--disable-software-rasterizer')
        
        # Window and display
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-infobars')
        
        # User agent
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Profile directory
        chrome_profile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrome_profile')
        chrome_options.add_argument(f'--user-data-dir={chrome_profile}')
        
        # Anti-detection
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        logger.info("Setting up Chrome with enhanced options...")
        
        # Test Chrome startup
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.google.com')
        time.sleep(2)
        
        page_title = driver.title
        driver.quit()
        
        logger.info(f"✅ Chrome setup successful! Page title: {page_title}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Chrome setup failed: {e}")
        return False

def test_twitter_access():
    """Test if we can access Twitter"""
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        chrome_profile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrome_profile')
        chrome_options.add_argument(f'--user-data-dir={chrome_profile}')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://twitter.com')
        time.sleep(3)
        
        page_title = driver.title
        driver.quit()
        
        logger.info(f"✅ Twitter access successful! Page title: {page_title}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Twitter access failed: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Enhanced Chrome Setup for VPS")
    print("="*40)
    
    # Step 1: Enhanced Chrome setup
    print("1. Setting up enhanced Chrome...")
    if setup_enhanced_chrome():
        print("✅ Enhanced Chrome setup successful")
    else:
        print("❌ Enhanced Chrome setup failed")
        return
    
    # Step 2: Test Twitter access
    print("2. Testing Twitter access...")
    if test_twitter_access():
        print("✅ Twitter access successful")
    else:
        print("❌ Twitter access failed")
    
    print("🚀 Enhanced Chrome setup completed!")

if __name__ == "__main__":
    main() 