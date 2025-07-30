#!/usr/bin/env python3
"""
Improve Chrome Profile Persistence
Fixes issues with Chrome profiles getting logged out
"""

import os
import shutil
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import CHROME_PROFILE_YAP, CHROME_PROFILE_USER, LOG_LEVEL, LOG_FILE

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

def backup_profile(profile_path, backup_name):
    """Backup existing profile before modifications"""
    try:
        if os.path.exists(profile_path):
            backup_path = f"{profile_path}_{backup_name}"
            shutil.copytree(profile_path, backup_path)
            logger.info(f"Backed up profile to: {backup_path}")
            return backup_path
        return None
    except Exception as e:
        logger.error(f"Error backing up profile: {e}")
        return None

def clean_profile_data(profile_path):
    """Clean problematic data from Chrome profile"""
    try:
        if not os.path.exists(profile_path):
            logger.info(f"Profile {profile_path} doesn't exist, skipping cleanup")
            return
        
        # Files that can cause login issues
        problematic_files = [
            'Cookies-journal',
            'Login Data-journal',
            'Web Data-journal',
            'Local State',
            'Preferences',
            'Secure Preferences'
        ]
        
        default_dir = os.path.join(profile_path, 'Default')
        if os.path.exists(default_dir):
            cleaned_count = 0
            for file_name in problematic_files:
                file_path = os.path.join(default_dir, file_name)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        logger.info(f"Removed problematic file: {file_name}")
                        cleaned_count += 1
                    except Exception as e:
                        logger.warning(f"Could not remove {file_name}: {e}")
            
            logger.info(f"Cleaned {cleaned_count} problematic files from profile")
        
    except Exception as e:
        logger.error(f"Error cleaning profile data: {e}")

def create_improved_chrome_options(profile_path):
    """Create Chrome options optimized for session persistence"""
    try:
        chrome_options = Options()
        chrome_options.add_argument(f'--user-data-dir={profile_path}')
        
        # Essential options for stability
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Options to improve session persistence
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-features=TranslateUI')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        
        # Disable features that can cause session issues
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')
        chrome_options.add_argument('--disable-remote-fonts')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        
        # Experimental options for better persistence
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('detach', True)
        
        # Additional options for session stability
        chrome_options.add_argument('--disable-session-crashed-bubble')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-popup-blocking')
        
        return chrome_options
        
    except Exception as e:
        logger.error(f"Error creating Chrome options: {e}")
        raise

def test_profile_persistence(profile_path, profile_name):
    """Test profile persistence by navigating to Twitter"""
    driver = None
    try:
        logger.info(f"Testing {profile_name} profile persistence...")
        
        # Create improved Chrome options
        chrome_options = create_improved_chrome_options(profile_path)
        
        # Initialize driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Navigate to Twitter
        logger.info("Navigating to Twitter...")
        driver.get("https://twitter.com")
        
        # Wait for page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Check if logged in
        try:
            # Look for login indicators
            login_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="AppTabBar_Home_Link"]')
            if login_elements:
                logger.info(f"✅ {profile_name} profile appears to be logged in")
                return True
            else:
                logger.info(f"ℹ️ {profile_name} profile is not logged in")
                return False
                
        except Exception as e:
            logger.warning(f"Could not determine login status: {e}")
            return False
            
    except Exception as e:
        logger.error(f"Error testing {profile_name} profile: {e}")
        return False
    finally:
        if driver:
            driver.quit()

def improve_yap_profile():
    """Improve YAP profile persistence"""
    print("🔧 Improving YAP Profile Persistence")
    print("=" * 50)
    
    # Backup existing profile
    backup_path = backup_profile(CHROME_PROFILE_YAP, "backup_before_improvement")
    
    # Clean problematic data
    print("\n🧹 Cleaning problematic profile data...")
    clean_profile_data(CHROME_PROFILE_YAP)
    
    # Test profile persistence
    print("\n🧪 Testing profile persistence...")
    persistence_ok = test_profile_persistence(CHROME_PROFILE_YAP, "YAP")
    
    if persistence_ok:
        print("\n✅ YAP profile persistence improved!")
        print("\n💡 Next Steps:")
        print("  1. Run 'python setup_twitter_login_yap.py' to login again")
        print("  2. Test the profile with 'python main_yap_scraper.py'")
    else:
        print("\n⚠️ Profile may need re-login")
        print("\n💡 Next Steps:")
        print("  1. Run 'python setup_twitter_login_yap.py' to login")
        print("  2. Test the profile with 'python main_yap_scraper.py'")
    
    return persistence_ok

def improve_user_profile():
    """Improve user profile persistence"""
    print("🔧 Improving User Profile Persistence")
    print("=" * 50)
    
    # Backup existing profile
    backup_path = backup_profile(CHROME_PROFILE_USER, "backup_before_improvement")
    
    # Clean problematic data
    print("\n🧹 Cleaning problematic profile data...")
    clean_profile_data(CHROME_PROFILE_USER)
    
    # Test profile persistence
    print("\n🧪 Testing profile persistence...")
    persistence_ok = test_profile_persistence(CHROME_PROFILE_USER, "User")
    
    if persistence_ok:
        print("\n✅ User profile persistence improved!")
        print("\n💡 Next Steps:")
        print("  1. Run 'python setup_twitter_login_user.py' to login again")
        print("  2. Test the profile with 'python main_scraper_locked_pc.py'")
    else:
        print("\n⚠️ Profile may need re-login")
        print("\n💡 Next Steps:")
        print("  1. Run 'python setup_twitter_login_user.py' to login")
        print("  2. Test the profile with 'python main_scraper_locked_pc.py'")
    
    return persistence_ok

def main():
    """Main function to improve profile persistence"""
    print("🔧 Chrome Profile Persistence Improvement")
    print("=" * 50)
    
    print("Choose an option:")
    print("1. Improve YAP profile (recommended for logout issues)")
    print("2. Improve User profile")
    print("3. Improve both profiles")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        improve_yap_profile()
    elif choice == "2":
        improve_user_profile()
    elif choice == "3":
        print("\n" + "=" * 50)
        improve_yap_profile()
        print("\n" + "=" * 50)
        improve_user_profile()
    elif choice == "4":
        print("❌ Operation cancelled")
        return False
    else:
        print("❌ Invalid choice")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Operation interrupted by user")
        exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        exit(1) 