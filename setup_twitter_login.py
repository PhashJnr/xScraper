#!/usr/bin/env python3
"""
Twitter Login Setup for Cloud VPS
Handles automatic Twitter authentication for scraping
"""

import logging
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import LOG_LEVEL, LOG_FILE

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class TwitterLoginSetup:
    def __init__(self):
        self.driver = None
        self.chrome_profile_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrome_profile')
        
    def setup_driver(self):
        """Setup Chrome driver with profile"""
        try:
            chrome_options = webdriver.ChromeOptions()
            
            # Use dedicated profile directory
            chrome_options.add_argument(f'--user-data-dir={self.chrome_profile_dir}')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # Anti-detection
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # For cloud VPS (headless mode)
            chrome_options.add_argument('--headless')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome driver initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up Chrome driver: {e}")
            return False
    
    def login_to_twitter(self, username, password):
        """Login to Twitter with provided credentials"""
        try:
            logger.info("Starting Twitter login process...")
            
            # Navigate to Twitter login
            self.driver.get("https://twitter.com/login")
            time.sleep(3)
            
            # Wait for login form
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]'))
            )
            
            # Enter username
            username_input = self.driver.find_element(By.CSS_SELECTOR, 'input[autocomplete="username"]')
            username_input.clear()
            username_input.send_keys(username)
            time.sleep(1)
            
            # Click Next
            next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
            next_button.click()
            time.sleep(3)
            
            # Enter password
            password_input = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
            password_input.clear()
            password_input.send_keys(password)
            time.sleep(1)
            
            # Click Login
            login_button = self.driver.find_element(By.XPATH, "//span[text()='Log in']")
            login_button.click()
            time.sleep(5)
            
            # Check if login was successful
            try:
                # Look for home timeline or profile elements
                WebDriverWait(self.driver, 10).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="primaryColumn"]')),
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="SideNav_AccountSwitcher_Button"]'))
                    )
                )
                logger.info("✅ Twitter login successful!")
                return True
                
            except TimeoutException:
                logger.error("❌ Login failed - could not verify successful login")
                return False
                
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False
    
    def verify_login(self):
        """Verify that login is still valid"""
        try:
            self.driver.get("https://twitter.com/home")
            time.sleep(3)
            
            # Check if we're logged in by looking for timeline elements
            timeline_elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="primaryColumn"]')
            
            if timeline_elements:
                logger.info("✅ Login verification successful")
                return True
            else:
                logger.warning("❌ Login verification failed")
                return False
                
        except Exception as e:
            logger.error(f"Error verifying login: {e}")
            return False
    
    def cleanup(self):
        """Clean up the driver"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Chrome driver closed successfully")
            except Exception as e:
                logger.error(f"Error closing Chrome driver: {e}")

def setup_twitter_login():
    """Main function to setup Twitter login"""
    print("🔐 Twitter Login Setup for Cloud VPS")
    print("="*40)
    
    # Get credentials from environment or user input
    twitter_username = os.getenv('TWITTER_USERNAME')
    twitter_password = os.getenv('TWITTER_PASSWORD')
    
    if not twitter_username:
        twitter_username = input("Enter Twitter username/email: ").strip()
    
    if not twitter_password:
        twitter_password = input("Enter Twitter password: ").strip()
    
    if not twitter_username or not twitter_password:
        print("❌ Twitter credentials are required")
        return False
    
    # Initialize login setup
    login_setup = TwitterLoginSetup()
    
    try:
        # Setup driver
        if not login_setup.setup_driver():
            print("❌ Failed to setup Chrome driver")
            return False
        
        # Attempt login
        if login_setup.login_to_twitter(twitter_username, twitter_password):
            print("✅ Twitter login successful!")
            print("📁 Chrome profile saved for future use")
            
            # Verify login
            if login_setup.verify_login():
                print("✅ Login verification successful")
                print("🚀 Ready for scraping!")
            else:
                print("⚠️  Login verification failed")
            
            return True
        else:
            print("❌ Twitter login failed")
            return False
            
    except Exception as e:
        logger.error(f"Error in login setup: {e}")
        print(f"❌ Error: {e}")
        return False
        
    finally:
        login_setup.cleanup()

if __name__ == "__main__":
    setup_twitter_login() 