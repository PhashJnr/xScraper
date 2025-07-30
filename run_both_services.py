#!/usr/bin/env python3
"""
Combined service runner for both user monitoring and YAP scraping
Runs both services simultaneously with proper coordination
"""

import logging
import sys
import time
import threading
import signal
from datetime import datetime
from config import (
    LOG_LEVEL, 
    LOG_FILE, 
    CHECK_INTERVAL_MINUTES, 
    YAP_CHECK_INTERVAL_MINUTES
)
from main_scraper import TweetMonitorService
from main_yap_scraper import YapScraperService

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class CombinedServiceRunner:
    def __init__(self):
        self.user_service = TweetMonitorService()
        self.yap_service = YapScraperService()
        self.running = True
        
    def run_user_monitor(self):
        """Run user monitoring service"""
        logger.info(f"Starting user monitoring service (every {CHECK_INTERVAL_MINUTES} minutes)")
        
        while self.running:
            try:
                logger.info("🔄 User monitoring cycle starting...")
                self.user_service.check_and_notify()
                
                # Wait for next cycle
                logger.info(f"⏰ Next user monitoring in {CHECK_INTERVAL_MINUTES} minutes...")
                for i in range(CHECK_INTERVAL_MINUTES * 60):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error in user monitoring: {e}")
                time.sleep(60)  # Wait before retry
    
    def run_yap_scraper(self):
        """Run YAP scraping service"""
        logger.info(f"Starting YAP scraping service (every {YAP_CHECK_INTERVAL_MINUTES} minutes)")
        
        while self.running:
            try:
                logger.info("🔄 YAP scraping cycle starting...")
                self.yap_service.run_yap_scraping()
                
                # Wait for next cycle
                logger.info(f"⏰ Next YAP scraping in {YAP_CHECK_INTERVAL_MINUTES} minutes...")
                for i in range(YAP_CHECK_INTERVAL_MINUTES * 60):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error in YAP scraping: {e}")
                time.sleep(60)  # Wait before retry
    
    def signal_handler(self, sig, frame):
        """Handle shutdown signals"""
        logger.info("Shutdown signal received, stopping services...")
        self.running = False
    
    def run_combined_services(self):
        """Run both services simultaneously"""
        logger.info("🚀 Starting combined services...")
        logger.info(f"👥 User monitoring: Every {CHECK_INTERVAL_MINUTES} minutes")
        logger.info(f"🔍 YAP scraping: Every {YAP_CHECK_INTERVAL_MINUTES} minutes")
        
        # Set up signal handlers
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Create threads for each service
        user_thread = threading.Thread(target=self.run_user_monitor, daemon=True)
        yap_thread = threading.Thread(target=self.run_yap_scraper, daemon=True)
        
        try:
            # Start both services
            user_thread.start()
            yap_thread.start()
            
            logger.info("✅ Both services started successfully!")
            
            # Keep main thread alive
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Error in combined services: {e}")
        finally:
            self.running = False
            logger.info("🛑 Services stopped")

def main():
    """Main function"""
    logger.info("Starting Combined Service Runner")
    
    try:
        runner = CombinedServiceRunner()
        runner.run_combined_services()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 