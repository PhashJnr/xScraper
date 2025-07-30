#!/usr/bin/env python3
"""
Test URL extraction from YAP scraper
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

logger = logging.getLogger(__name__)

def test_url_extraction():
    """Test URL extraction from current page"""
    logger.info("Testing URL extraction...")
    
    try:
        scraper = YapSearchScraper()
        
        # Build search query
        search_query = scraper._build_yap_search_query()
        
        # Navigate to search page
        base_url = "https://x.com/search"
        query_params = {
            'q': search_query,
            'src': YAP_SEARCH_SOURCE
        }
        
        from urllib.parse import urlencode
        search_url = f"{base_url}?{urlencode(query_params)}"
        
        logger.info(f"Navigating to: {search_url}")
        scraper.driver.get(search_url)
        
        # Wait for tweets to load
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        
        WebDriverWait(scraper.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]'))
        )
        
        # Wait 10 seconds for content to load
        logger.info("Waiting 10 seconds for content to load...")
        time.sleep(10)
        
        # Test URL extraction
        logger.info("Testing URL extraction from current page...")
        urls = scraper._extract_urls_from_current_page()
        
        logger.info(f"✅ URL extraction test completed!")
        logger.info(f"📊 Results:")
        logger.info(f"  - Target: {MAX_TWEETS_TO_SCRAPE}")
        logger.info(f"  - Found: {len(urls)} URLs")
        
        if urls:
            print(f"\nFirst 5 URLs found:")
            for i, url in enumerate(urls[:5], 1):
                print(f"{i}. {url}")
        else:
            print("No URLs found")
        
        scraper.cleanup()
        logger.info("URL extraction test completed!")
        
    except Exception as e:
        logger.error(f"URL extraction test failed: {e}")

if __name__ == "__main__":
    print("Testing URL extraction...")
    test_url_extraction() 