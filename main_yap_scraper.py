#!/usr/bin/env python3
"""
YAP Links Scraper with Telegram File Sending
Runs on a separate interval from user monitoring
"""

import logging
import time
import sys
import signal
from datetime import datetime
from config import (
    LOG_LEVEL, 
    LOG_FILE, 
    YAP_CHECK_INTERVAL_MINUTES
)
from yap_scraper import YapSearchScraper
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

class YapScraperService:
    def __init__(self):
        self.yap_scraper = None
        logger.info("YAP scraper service initialized")
    
    def initialize_scraper(self):
        """Initialize the YAP scraper"""
        if self.yap_scraper is None:
            self.yap_scraper = YapSearchScraper()
            logger.info("YAP scraper initialized")
    
    def run_yap_scraping(self):
        """Run YAP scraping and send results to Telegram"""
        try:
            # Initialize scraper if needed
            self.initialize_scraper()
            
            logger.info("Starting YAP links scraping...")
            success = self.yap_scraper.run_yap_scraper()
            
            if success:
                logger.info("YAP scraping completed successfully")
            else:
                logger.warning("YAP scraping completed with issues")
            
            # Quit Chrome after task completion
            self.yap_scraper.quit_chrome_after_task()
            self.yap_scraper = None  # Reset for next check
                
        except Exception as e:
            logger.error(f"Error during YAP scraping: {e}")
            # Ensure Chrome is quit even on error
            if self.yap_scraper:
                self.yap_scraper.quit_chrome_after_task()
                self.yap_scraper = None
    
    def run_continuous(self):
        """Run the YAP scraper continuously"""
        logger.info(f"Starting continuous YAP scraping (Every {YAP_CHECK_INTERVAL_MINUTES} minutes)")
        
        def signal_handler(sig, frame):
            logger.info("Shutdown signal received, cleaning up...")
            if self.yap_scraper:
                self.yap_scraper.cleanup()
            sys.exit(0)
        
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        
        while True:
            try:
                # Run the scraping
                self.run_yap_scraping()
                
                # Show countdown for next check
                logger.info(f"Next YAP scraping in {YAP_CHECK_INTERVAL_MINUTES} minutes...")
                show_countdown(YAP_CHECK_INTERVAL_MINUTES * 60)
                
            except KeyboardInterrupt:
                logger.info("Interrupted by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in continuous loop: {e}")
                time.sleep(60)  # Wait a minute before retrying

def main():
    """Main function"""
    logger.info("Starting YAP Links Scraper Service")
    
    try:
        service = YapScraperService()
        service.run_continuous()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 