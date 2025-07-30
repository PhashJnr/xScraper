#!/usr/bin/env python3
"""
Twitter Login Setup for User Monitoring Profile
Logs into Twitter using the individual user monitoring Chrome profile
"""

import os
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import CHROME_PROFILE_USER, TWITTER_USERNAME, TWITTER_PASSWORD, LOG_LEVEL, LOG_FILE

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

def setup_user_chrome_driver():
    """Setup Chrome driver with user monitoring profile"""
    try:
        # Ensure the profile directory exists
        os.makedirs(CHROME_PROFILE_USER, exist_ok=True)
        
        chrome_options = Options()
        chrome_options.add_argument(f'--user-data-dir={CHROME_PROFILE_USER}')
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
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info("Chrome driver initialized successfully for user monitoring profile")
        return driver
        
    except Exception as e:
        logger.error(f"Failed to setup Chrome driver: {e}")
        raise

def login_to_twitter(driver):
    """Login to Twitter using the provided credentials"""
    try:
        print("🔐 Logging into Twitter for User Monitoring Profile...")
        print("=" * 50)
        
        # Navigate to Twitter login page
        driver.get("https://twitter.com/i/flow/login")
        
        # Wait for login form to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
        )
        
        # Enter username
        username_input = driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="username"]')
        username_input.clear()
        username_input.send_keys(TWITTER_USERNAME)
        
        # Click Next button
        next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
        next_button.click()
        
        # Wait for password field
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
        )
        
        # Enter password
        password_input = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password_input.clear()
        password_input.send_keys(TWITTER_PASSWORD)
        
        # Click Login button
        login_button = driver.find_element(By.XPATH, "//span[text()='Log in']")
        login_button.click()
        
        # Wait for successful login
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="AppTabBar_Home_Link"]'))
        )
        
        print("✅ Successfully logged into Twitter for User Monitoring Profile!")
        print(f"📁 Profile saved to: {CHROME_PROFILE_USER}")
        
        # Wait a bit to ensure everything is saved
        time.sleep(5)
        
        return True
        
    except TimeoutException:
        print("❌ Timeout waiting for login elements")
        return False
    except NoSuchElementException as e:
        print(f"❌ Element not found: {e}")
        return False
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False

def main():
    """Main function to setup Twitter login for user monitoring profile"""
    driver = None
    try:
        # Check if credentials are provided
        if not TWITTER_USERNAME or not TWITTER_PASSWORD:
            print("❌ Twitter credentials not found in .env file")
            print("Please add TWITTER_USERNAME and TWITTER_PASSWORD to your .env file")
            return False
        
        # Setup Chrome driver
        driver = setup_user_chrome_driver()
        
        # Login to Twitter
        success = login_to_twitter(driver)
        
        if success:
            print("\n🎉 User Monitoring Profile setup completed!")
            print("\n💡 Next Steps:")
            print("  1. Run 'python setup_twitter_login_yap.py' to setup YAP profile")
            print("  2. Test user monitoring: 'python main_scraper_locked_pc.py'")
        else:
            print("\n❌ Failed to setup User Monitoring Profile")
        
        return success
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup interrupted by user")
        sys.exit(1) 