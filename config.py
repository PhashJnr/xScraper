#!/usr/bin/env python3
"""
Configuration settings for Twitter Monitor
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
        print("\nPlease check your .env file and ensure all required values are set.")
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