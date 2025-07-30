#!/usr/bin/env python3
"""
Configuration settings for Twitter Monitor
"""

import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Twitter credentials
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

# Telegram credentials
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Check intervals (in minutes)
CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', 5))
YAP_CHECK_INTERVAL_MINUTES = int(os.getenv('YAP_CHECK_INTERVAL_MINUTES', 3))

# Chrome profiles - Use proper names
CHROME_PROFILE_USER = 'chrome_profile_user'
CHROME_PROFILE_YAP = 'chrome_profile_yap'

# Chrome binary path
CHROME_BINARY_PATH = '/usr/bin/google-chrome'

# Scraping configuration
MAX_TWEETS_TO_SCRAPE = int(os.getenv('MAX_TWEETS_TO_SCRAPE', 10))

# Users to monitor (comma-separated list)
USERS_TO_MONITOR = os.getenv('USERS_TO_MONITOR', 'elonmusk,OpenAI,AnthropicAI').split(',')

# YAP Search Configuration
YAP_SEARCH_KEYWORDS = os.getenv('YAP_SEARCH_KEYWORDS', 'AI,artificial intelligence,machine learning').split(',')
YAP_FILTER_VERIFIED = os.getenv('YAP_FILTER_VERIFIED', 'true').lower() == 'true'
YAP_FILTER_NATIVE_RETWEETS = os.getenv('YAP_FILTER_NATIVE_RETWEETS', 'false').lower() == 'true'
YAP_FILTER_RETWEETS = os.getenv('YAP_FILTER_RETWEETS', 'false').lower() == 'true'
YAP_FILTER_REPLIES = os.getenv('YAP_FILTER_REPLIES', 'false').lower() == 'true'
YAP_MIN_REPLIES = int(os.getenv('YAP_MIN_REPLIES', 0))
YAP_MIN_LIKES = int(os.getenv('YAP_MIN_LIKES', 0))
YAP_MIN_RETWEETS = int(os.getenv('YAP_MIN_RETWEETS', 0))
YAP_LANGUAGE = os.getenv('YAP_LANGUAGE', 'en')
YAP_TIME_WINDOW = os.getenv('YAP_TIME_WINDOW', '7d')  # 7d, 1d, 1h, etc.
YAP_FILTER_LINKS = os.getenv('YAP_FILTER_LINKS', 'false').lower() == 'true'
YAP_FILTER_MEDIA = os.getenv('YAP_FILTER_MEDIA', 'false').lower() == 'true'
YAP_FILTER_IMAGES = os.getenv('YAP_FILTER_IMAGES', 'false').lower() == 'true'
YAP_FILTER_VIDEOS = os.getenv('YAP_FILTER_VIDEOS', 'false').lower() == 'true'
YAP_SEARCH_SOURCE = os.getenv('YAP_SEARCH_SOURCE', 'twitter')  # twitter, news, etc.

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = 'tweet_monitor.log'

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)