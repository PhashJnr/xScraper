#!/usr/bin/env python3
"""
Setup Individual Chrome Profiles for Twitter Monitor
Creates separate Chrome profiles for user monitoring and YAP scraping
"""

import os
import sys
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import CHROME_PROFILE_USER, CHROME_PROFILE_YAP, LOG_LEVEL, LOG_FILE

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_profile_directory(profile_path, profile_name):
    """Create and initialize a Chrome profile directory"""
    try:
        # Create the profile directory
        os.makedirs(profile_path, exist_ok=True)
        logger.info(f"Created {profile_name} profile directory: {profile_path}")
        
        # Setup Chrome options for this profile
        chrome_options = Options()
        chrome_options.add_argument(f'--user-data-dir={profile_path}')
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
        
        # Initialize Chrome driver to create profile
        logger.info(f"Initializing {profile_name} Chrome profile...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to Twitter to initialize the profile
        driver.get("https://twitter.com")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        logger.info(f"✅ {profile_name} profile initialized successfully")
        
        # Close the driver
        driver.quit()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create {profile_name} profile: {e}")
        return False

def setup_individual_profiles():
    """Setup individual Chrome profiles for user monitoring and YAP scraping"""
    print("🔧 Setting up Individual Chrome Profiles")
    print("=" * 50)
    
    # Create user monitoring profile
    print("\n📁 Setting up User Monitoring Profile...")
    user_success = create_profile_directory(CHROME_PROFILE_USER, "User Monitoring")
    
    # Create YAP scraping profile
    print("\n📁 Setting up YAP Scraping Profile...")
    yap_success = create_profile_directory(CHROME_PROFILE_YAP, "YAP Scraping")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Profile Setup Summary:")
    print(f"  User Monitoring Profile: {'✅ Success' if user_success else '❌ Failed'}")
    print(f"  YAP Scraping Profile: {'✅ Success' if yap_success else '❌ Failed'}")
    
    if user_success and yap_success:
        print("\n🎉 All profiles created successfully!")
        print("\n💡 Next Steps:")
        print("  1. Run 'python setup_twitter_login_user.py' to login to user profile")
        print("  2. Run 'python setup_twitter_login_yap.py' to login to YAP profile")
        print("  3. Test user monitoring: 'python main_scraper_locked_pc.py'")
        print("  4. Test YAP scraping: 'python main_yap_scraper.py'")
        return True
    else:
        print("\n❌ Some profiles failed to create. Please check the logs.")
        return False

if __name__ == "__main__":
    try:
        success = setup_individual_profiles()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error during profile setup: {e}")
        sys.exit(1) 