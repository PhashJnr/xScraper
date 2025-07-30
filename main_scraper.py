#!/usr/bin/env python3
"""
Twitter User Monitor with Telegram Notifications (Web Scraping Version)
No API rate limits - uses Selenium to scrape Twitter directly
"""

import logging
import time
import schedule
import sys
import signal
from datetime import datetime
from config import (
    LOG_LEVEL, 
    LOG_FILE, 
    USERS_TO_MONITOR, 
    CHECK_INTERVAL_MINUTES,
    YAP_CHECK_INTERVAL_MINUTES
)
from scraper_monitor import TwitterScraperMonitor
from robust_notifier import RobustTelegramNotifier
from countdown_timer import show_countdown

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

# Suppress verbose logging
logging.getLogger('httpx').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('selenium').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

class TweetMonitorService:
    def __init__(self):
        self.twitter_monitor = None
        self.telegram_notifier = RobustTelegramNotifier()
        logger.info("Tweet monitor service initialized (Web Scraping Mode)")
    
    def initialize_monitor(self):
        """Initialize the Twitter monitor"""
        if self.twitter_monitor is None:
            self.twitter_monitor = TwitterScraperMonitor()
            logger.info("Twitter monitor initialized")
    
    def check_and_notify(self):
        """Check for new tweets and send notifications"""
        try:
            # Initialize monitor if needed
            self.initialize_monitor()
            
            logger.info("Checking for tweets...")
            new_tweets = self.twitter_monitor.check_new_tweets()
            
            if new_tweets:
                logger.info(f"Tweet found: {len(new_tweets)} new tweets")
                for i, tweet in enumerate(new_tweets, 1):
                    try:
                        self.send_tweet_notification(tweet)
                        # Longer delay between notifications to prevent connection pool issues
                        if i < len(new_tweets):
                            time.sleep(3)  # 3 second delay between notifications
                    except Exception as e:
                        logger.error(f"Error sending notification for tweet {i}: {e}")
                        # Continue with next tweet even if one fails
                        continue
            else:
                logger.info("No new tweets found")
            
            # Quit Chrome after task completion
            self.twitter_monitor.quit_chrome_after_task()
            self.twitter_monitor = None  # Reset for next check
                
        except Exception as e:
            logger.error(f"Error during tweet check: {e}")
            # Ensure Chrome is quit even on error
            if self.twitter_monitor:
                self.twitter_monitor.quit_chrome_after_task()
                self.twitter_monitor = None
    
    def send_tweet_notification(self, tweet):
        """Send notification for a single tweet"""
        try:
            username = tweet['username']
            tweet_text = tweet['text']
            tweet_id = tweet['id']
            created_at = tweet['created_at']
            
            # Generate tweet URL
            tweet_url = self.twitter_monitor.format_tweet_url(username, tweet_id)
            
            # Format creation time
            formatted_time = self.twitter_monitor.format_created_at(created_at)
            
            # Get tweet type
            tweet_type = tweet.get('type', 'original')
            
            # Create and send notification
            message = self.telegram_notifier.format_tweet_message(
                username, tweet_text, tweet_url, formatted_time, tweet_type
            )
            
            self.telegram_notifier.send_notification_sync(message)
            logger.info("Notification sent")
            
        except Exception as e:
            logger.error(f"Error sending notification for tweet: {e}")
    
    def run_continuous(self):
        """Run the monitor continuously"""
        logger.info(f"Starting continuous monitoring (User monitoring every {CHECK_INTERVAL_MINUTES} minutes)")
        
        def signal_handler(sig, frame):
            logger.info("Shutdown signal received, cleaning up...")
            if self.twitter_monitor:
                self.twitter_monitor.cleanup()
            sys.exit(0)
        
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        
        while True:
            try:
                # Run the check
                self.check_and_notify()
                
                # Show countdown for next check
                logger.info(f"Next user monitoring check in {CHECK_INTERVAL_MINUTES} minutes...")
                show_countdown(CHECK_INTERVAL_MINUTES * 60)
                
            except KeyboardInterrupt:
                logger.info("Interrupted by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in continuous loop: {e}")
                time.sleep(60)  # Wait a minute before retrying

def main():
    """Main entry point"""
    service = TweetMonitorService()
    service.run_continuous()

if __name__ == "__main__":
    main() 