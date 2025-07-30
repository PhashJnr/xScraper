#!/usr/bin/env python3
"""
Test Telegram file sending functionality
"""

import logging
import sys
import os
from config import LOG_LEVEL, LOG_FILE
from robust_notifier import RobustTelegramNotifier

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

def test_telegram_file_send():
    """Test sending a file to Telegram"""
    logger.info("Testing Telegram file sending...")
    
    try:
        # Create a test file
        test_file = "test_yap_links.txt"
        test_content = """https://x.com/user1/status/123456789
https://x.com/user2/status/987654321
https://x.com/user3/status/555666777
https://x.com/user4/status/111222333
https://x.com/user5/status/444555666"""
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        logger.info(f"Created test file: {test_file}")
        
        # Initialize Telegram notifier
        notifier = RobustTelegramNotifier()
        
        # Send the file
        caption = "🧪 Test YAP Links File\n\n📊 Found 5 tweet URLs\n📅 Test run"
        
        logger.info("Sending file to Telegram...")
        success = notifier.send_document(test_file, caption)
        
        if success:
            logger.info("✅ File sent successfully to Telegram!")
        else:
            logger.error("❌ Failed to send file to Telegram")
        
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)
            logger.info(f"Cleaned up test file: {test_file}")
        
        logger.info("Telegram file sending test completed!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")

if __name__ == "__main__":
    print("Testing Telegram file sending...")
    test_telegram_file_send() 