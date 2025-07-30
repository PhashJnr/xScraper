#!/usr/bin/env python3
"""
Fix Chrome Path Issue
Explicitly sets Chrome binary path for Selenium WebDriver
"""

import os
import sys
import subprocess
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def find_chrome_binary():
    """Find the Chrome binary path"""
    possible_paths = [
        '/usr/bin/google-chrome',
        '/usr/bin/chrome',
        '/usr/bin/chromium-browser',
        '/usr/bin/chromium',
        '/snap/bin/chromium',
        '/usr/bin/google-chrome-stable'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            logger.info(f"Found Chrome at: {path}")
            return path
    
    # Try to find Chrome using which command
    try:
        result = subprocess.run(['which', 'google-chrome'], capture_output=True, text=True)
        if result.returncode == 0:
            chrome_path = result.stdout.strip()
            logger.info(f"Found Chrome using 'which': {chrome_path}")
            return chrome_path
    except Exception as e:
        logger.warning(f"Could not find Chrome using 'which': {e}")
    
    return None

def test_chrome_driver():
    """Test Chrome driver with explicit binary path"""
    try:
        chrome_binary = find_chrome_binary()
        if not chrome_binary:
            logger.error("❌ Chrome binary not found!")
            return False
        
        logger.info(f"Testing Chrome driver with binary: {chrome_binary}")
        
        # Setup Chrome options with explicit binary path
        chrome_options = Options()
        chrome_options.binary_location = chrome_binary
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')  # Run in headless mode for testing
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--silent')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Test navigation
        driver.get("https://www.google.com")
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        logger.info("✅ Chrome driver test successful!")
        
        # Close the driver
        driver.quit()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Chrome driver test failed: {e}")
        return False

def update_config_files():
    """Update configuration files to include Chrome binary path"""
    try:
        chrome_binary = find_chrome_binary()
        if not chrome_binary:
            logger.error("❌ Cannot update config files - Chrome binary not found!")
            return False
        
        # Update config.py to include Chrome binary path
        config_content = f'''#!/usr/bin/env python3
"""
Configuration settings for Twitter Monitor
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Chrome binary path
CHROME_BINARY_PATH = "{chrome_binary}"

# Twitter API Configuration (for reference, not used in scraping mode)
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', '')

# Twitter Login Credentials (for cloud VPS)
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME', '')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD', '')

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# Monitoring intervals (in minutes)
CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', '15'))  # User monitoring interval
YAP_CHECK_INTERVAL_MINUTES = int(os.getenv('YAP_CHECK_INTERVAL_MINUTES', '1080'))  # YAP links interval (18 hours = 1080 minutes)

# Maximum tweets to scrape
MAX_TWEETS_TO_SCRAPE = int(os.getenv('MAX_TWEETS_TO_SCRAPE', '50'))

# Users to monitor (comma-separated list)
USERS_TO_MONITOR = [
    user.strip() for user in os.getenv('USERS_TO_MONITOR', 'phashcooks,JoeParys,curtislepore,cryptojack,greg_miller05,CryptoWendyO,MasonVersluis,Sheldon_Sniper,blockchainchick,cryptorecruitr,EleanorTerrett,SadafJadran,LadyofCrypto1,MacnBTC,CryptoWizardd,eliz883,ariusCrypt0,KoroushAK').split(',')
    if user.strip()
]

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'tweet_monitor.log')

# YAP Search Query Configuration
# These parameters control the YAP search query for finding relevant tweets

# Individual Chrome profiles
CHROME_PROFILE_USER = os.path.join(BASE_DIR, "chrome_profile_user")
CHROME_PROFILE_YAP = os.path.join(BASE_DIR, "chrome_profile_yap")

# Search Keywords (REQUIRED)
YAP_SEARCH_KEYWORDS = os.getenv('YAP_SEARCH_KEYWORDS', '("cysic" OR @cysic_xyz)')

# Account Verification Filter
YAP_FILTER_VERIFIED = os.getenv('YAP_FILTER_VERIFIED', 'true').lower() == 'true'  # Only verified accounts

# Content Type Filters
YAP_FILTER_NATIVE_RETWEETS = os.getenv('YAP_FILTER_NATIVE_RETWEETS', 'true').lower() == 'true'  # Exclude native retweets
YAP_FILTER_RETWEETS = os.getenv('YAP_FILTER_RETWEETS', 'true').lower() == 'true'  # Exclude retweets
YAP_FILTER_REPLIES = os.getenv('YAP_FILTER_REPLIES', 'true').lower() == 'true'  # Exclude replies

# Engagement Filters
YAP_MIN_REPLIES = int(os.getenv('YAP_MIN_REPLIES', '20'))  # Minimum replies required
YAP_MIN_LIKES = int(os.getenv('YAP_MIN_LIKES', '0'))  # Minimum likes required
YAP_MIN_RETWEETS = int(os.getenv('YAP_MIN_RETWEETS', '0'))  # Minimum retweets required

# Language and Time Filters
YAP_LANGUAGE = os.getenv('YAP_LANGUAGE', 'en')  # Language filter (en, es, fr, etc.)
YAP_TIME_WINDOW = int(os.getenv('YAP_TIME_WINDOW', '1440'))  # Time window in minutes (1440 = 24 hours)

# Additional Filters
YAP_FILTER_LINKS = os.getenv('YAP_FILTER_LINKS', 'false').lower() == 'true'  # Only tweets with links
YAP_FILTER_MEDIA = os.getenv('YAP_FILTER_MEDIA', 'false').lower() == 'true'  # Only tweets with media
YAP_FILTER_IMAGES = os.getenv('YAP_FILTER_IMAGES', 'false').lower() == 'true'  # Only tweets with images
YAP_FILTER_VIDEOS = os.getenv('YAP_FILTER_VIDEOS', 'false').lower() == 'true'  # Only tweets with videos

# Search Source
YAP_SEARCH_SOURCE = os.getenv('YAP_SEARCH_SOURCE', 'recent_search_click')  # Search source parameter

# Validate required settings
def validate_config():
    """Validate that required configuration is present"""
    errors = []
    
    if not TELEGRAM_BOT_TOKEN:
        errors.append("TELEGRAM_BOT_TOKEN is required")
    
    if not TELEGRAM_CHAT_ID:
        errors.append("TELEGRAM_CHAT_ID is required")
    
    if not USERS_TO_MONITOR:
        errors.append("USERS_TO_MONITOR is required")
    
    if errors:
        print("Configuration errors found:")
        for error in errors:
            print(f"  - {error}")
        print("\\nPlease check your .env file and ensure all required values are set.")
        return False
    
    return True

# Print current configuration for debugging
def print_config():
    """Print current configuration settings"""
    print("Current Configuration:")
    print(f"  CHECK_INTERVAL_MINUTES: {CHECK_INTERVAL_MINUTES}")
    print(f"  YAP_CHECK_INTERVAL_MINUTES: {YAP_CHECK_INTERVAL_MINUTES}")
    print(f"  MAX_TWEETS_TO_SCRAPE: {MAX_TWEETS_TO_SCRAPE}")
    print(f"  USERS_TO_MONITOR: {len(USERS_TO_MONITOR)} users")
    print(f"  LOG_LEVEL: {LOG_LEVEL}")
    print(f"  LOG_FILE: {LOG_FILE}")
    print(f"  CHROME_BINARY_PATH: {CHROME_BINARY_PATH}")
    print(f"  TELEGRAM_BOT_TOKEN: {'Set' if TELEGRAM_BOT_TOKEN else 'Not set'}")
    print(f"  TELEGRAM_CHAT_ID: {'Set' if TELEGRAM_CHAT_ID else 'Not set'}")
    
    # YAP search settings
    print(f"  YAP_SEARCH_KEYWORDS: {YAP_SEARCH_KEYWORDS}")
    print(f"  YAP_FILTER_VERIFIED: {YAP_FILTER_VERIFIED}")
    print(f"  YAP_MIN_REPLIES: {YAP_MIN_REPLIES}")
    print(f"  YAP_LANGUAGE: {YAP_LANGUAGE}")
    print(f"  YAP_TIME_WINDOW: {YAP_TIME_WINDOW}")

if __name__ == "__main__":
    print_config()
    validate_config()
'''
        
        # Write updated config.py
        with open('config.py', 'w') as f:
            f.write(config_content)
        
        logger.info("✅ Updated config.py with Chrome binary path")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to update config files: {e}")
        return False

def main():
    """Main function to fix Chrome path issues"""
    print("🔧 Fixing Chrome Path Issues")
    print("=" * 40)
    
    # Step 1: Find Chrome binary
    print("\n🔍 Finding Chrome binary...")
    chrome_binary = find_chrome_binary()
    
    if not chrome_binary:
        print("❌ Chrome binary not found!")
        print("\n💡 Please install Chrome first:")
        print("  sudo apt update")
        print("  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
        print("  sudo apt install -y ./google-chrome-stable_current_amd64.deb")
        return False
    
    print(f"✅ Found Chrome at: {chrome_binary}")
    
    # Step 2: Test Chrome driver
    print("\n🧪 Testing Chrome driver...")
    if not test_chrome_driver():
        print("❌ Chrome driver test failed!")
        return False
    
    # Step 3: Update config files
    print("\n📝 Updating configuration files...")
    if not update_config_files():
        print("❌ Failed to update config files!")
        return False
    
    print("\n🎉 Chrome path issues fixed successfully!")
    print("\n💡 Next Steps:")
    print("  1. Run 'python3 setup_individual_profiles.py' to create profiles")
    print("  2. Run 'python3 setup_twitter_login_user.py' to login")
    print("  3. Run 'python3 setup_twitter_login_yap.py' to login")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Operation interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1) 