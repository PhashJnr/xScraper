#!/usr/bin/env python3
"""
Twitter User Monitor optimized for running when PC is locked
"""

import logging
import time
import sys
import signal
import os
from datetime import datetime
from config import CHECK_INTERVAL_MINUTES, LOG_LEVEL, LOG_FILE, MAX_TWEETS_TO_SCRAPE
from scraper_monitor import TwitterScraperMonitor
from robust_notifier import RobustTelegramNotifier
from countdown_timer import show_countdown

# Configure logging for locked PC (more verbose)
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

class LockedPCMonitorService:
    def __init__(self):
        self.twitter_monitor = None
        self.telegram_notifier = RobustTelegramNotifier()
        self.check_count = 0
        logger.info("Locked PC monitor service initialized")
    
    def initialize_monitor(self):
        """Initialize the Twitter monitor with locked PC optimizations"""
        if self.twitter_monitor is None:
            try:
                self.twitter_monitor = TwitterScraperMonitor()
                logger.info("Twitter monitor initialized for locked PC mode")
            except Exception as e:
                logger.error(f"Failed to initialize monitor: {e}")
                # Wait and retry
                time.sleep(30)
                return False
        return True
    
    def check_and_notify(self):
        """Check for new tweets and send notifications (locked PC optimized)"""
        try:
            self.check_count += 1
            logger.info(f"=== Check #{self.check_count} ===")
            
            # Initialize monitor if needed
            if not self.initialize_monitor():
                return
            
            logger.info("Checking for tweets...")
            new_tweets = self.twitter_monitor.check_new_tweets()
            
            if new_tweets:
                logger.info(f"Tweet found: {len(new_tweets)} new tweets")
                for i, tweet in enumerate(new_tweets, 1):
                    try:
                        self.send_tweet_notification(tweet)
                        # Longer delay for locked PC
                        if i < len(new_tweets):
                            time.sleep(5)  # 5 second delay between notifications
                    except Exception as e:
                        logger.error(f"Error sending notification for tweet {i}: {e}")
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
    
    def run_continuous_locked_pc(self):
        """Run the monitor continuously optimized for locked PC"""
        logger.info("Starting Twitter monitor (Locked PC Mode)...")
        logger.info(f"Check interval: {CHECK_INTERVAL_MINUTES} minutes")
        logger.info("This will continue running when PC is locked")
        
        # Setup signal handler for graceful shutdown
        def signal_handler(sig, frame):
            logger.info("Stopping monitor...")
            try:
                if self.twitter_monitor:
                    self.twitter_monitor.cleanup()
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Run initial check
        self.check_and_notify()
        
        # Main loop with countdown timer (simplified for locked PC)
        while True:
            try:
                # Show countdown timer
                if not show_countdown(CHECK_INTERVAL_MINUTES, "Next tweet check"):
                    break  # User interrupted
                
                # Run the check
                self.check_and_notify()
                
            except KeyboardInterrupt:
                logger.info("Monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(60)  # Wait before retrying
        
        # Final cleanup
        if self.twitter_monitor:
            self.twitter_monitor.cleanup()

def main():
    """Main function"""
    print("🚀 Starting Twitter Monitor (Locked PC Mode)")
    print("=" * 50)
    
    # Kill any existing Chrome processes before starting
    try:
        from kill_chrome import kill_all_chrome_processes
        print("🧹 Cleaning up any existing Chrome processes...")
        kill_all_chrome_processes()
        print("✅ Chrome cleanup completed")
    except Exception as e:
        print(f"⚠️ Chrome cleanup warning: {e}")
    
    print("\n📡 Initializing monitor...")
    
    # Create and run the monitor service
    monitor_service = LockedPCMonitorService()
    
    try:
        monitor_service.run_continuous_locked_pc()
    except KeyboardInterrupt:
        print("\n🛑 Stopping monitor...")
        monitor_service.cleanup()
    except Exception as e:
        print(f"\n❌ Error running monitor: {e}")
        monitor_service.cleanup()

if __name__ == "__main__":
    main() 