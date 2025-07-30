#!/usr/bin/env python3
"""
Test the simplified YAP scraper that extracts URLs from current page only
"""

import logging
import sys
import time
from config import LOG_LEVEL, LOG_FILE, MAX_TWEETS_TO_SCRAPE, YAP_SEARCH_SOURCE
from yap_scraper import YapSearchScraper

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
logging.getLogger('selenium').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

def test_simplified_yap_scraper():
    """Test the enhanced YAP scraper with multiple scrolls"""
    logger.info("Testing enhanced YAP scraper with multiple scrolls...")
    
    try:
        scraper = YapSearchScraper()
        
        logger.info(f"Target: Find {MAX_TWEETS_TO_SCRAPE} tweets with multiple scrolls")
        logger.info("Running enhanced YAP scraper...")
        
        start_time = time.time()
        success = scraper.run_yap_scraper()
        end_time = time.time()
        
        if success:
            # Check results
            import os
            output_file = 'yap_links.txt'
            
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        lines = content.split('\n')
                        logger.info(f"✅ Enhanced YAP scraper successful!")
                        logger.info(f"📊 Results:")
                        logger.info(f"  - Target tweets: {MAX_TWEETS_TO_SCRAPE}")
                        logger.info(f"  - Found tweets: {len(lines)}")
                        logger.info(f"  - Time taken: {end_time - start_time:.1f} seconds")
                        logger.info(f"  - Success rate: {(len(lines)/MAX_TWEETS_TO_SCRAPE)*100:.1f}%")
                        
                        if len(lines) >= MAX_TWEETS_TO_SCRAPE * 0.8:  # 80% success rate
                            logger.info("🎉 Excellent results!")
                        elif len(lines) >= MAX_TWEETS_TO_SCRAPE * 0.5:  # 50% success rate
                            logger.info("👍 Good results!")
                        else:
                            logger.warning("⚠️ Could find more tweets")
                        
                        # Show first few URLs
                        print(f"\nFirst 5 tweet URLs found:")
                        for i, url in enumerate(lines[:5], 1):
                            print(f"{i}. {url}")
                    else:
                        logger.warning("⚠️ Enhanced YAP scraper completed but no URLs found")
            else:
                logger.error("❌ Enhanced YAP scraper failed - no output file created")
        else:
            logger.error("❌ Enhanced YAP scraper failed")
        
        scraper.cleanup()
        logger.info("Enhanced YAP scraper test completed!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")

if __name__ == "__main__":
    print("Testing enhanced YAP scraper with multiple scrolls...")
    test_simplified_yap_scraper() 