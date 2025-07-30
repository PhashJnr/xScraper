#!/usr/bin/env python3
"""
Test separate time intervals for YAP and user monitoring
"""

import logging
import sys
from config import (
    LOG_LEVEL, 
    LOG_FILE, 
    CHECK_INTERVAL_MINUTES, 
    YAP_CHECK_INTERVAL_MINUTES
)

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

def test_separate_intervals():
    """Test that separate intervals are configured correctly"""
    print("🧪 Testing Separate Time Intervals")
    print("="*40)
    
    # Check intervals
    print(f"👥 User Monitoring Interval: {CHECK_INTERVAL_MINUTES} minutes")
    print(f"🔍 YAP Links Interval: {YAP_CHECK_INTERVAL_MINUTES} minutes ({YAP_CHECK_INTERVAL_MINUTES/60:.1f} hours)")
    
    # Validate intervals
    if CHECK_INTERVAL_MINUTES == 15:
        print("✅ User monitoring interval is correct (15 minutes)")
    else:
        print(f"⚠️  User monitoring interval is {CHECK_INTERVAL_MINUTES} minutes (expected 15)")
    
    if YAP_CHECK_INTERVAL_MINUTES == 1080:
        print("✅ YAP links interval is correct (18 hours)")
    else:
        print(f"⚠️  YAP links interval is {YAP_CHECK_INTERVAL_MINUTES} minutes (expected 1080)")
    
    # Show conversion
    print(f"\n📊 Time Conversions:")
    print(f"  User monitoring: {CHECK_INTERVAL_MINUTES} minutes = {CHECK_INTERVAL_MINUTES/60:.2f} hours")
    print(f"  YAP links: {YAP_CHECK_INTERVAL_MINUTES} minutes = {YAP_CHECK_INTERVAL_MINUTES/60:.1f} hours")
    
    # Show frequency
    print(f"\n🔄 Frequency:")
    print(f"  User monitoring: Every {CHECK_INTERVAL_MINUTES} minutes ({24*60/CHECK_INTERVAL_MINUTES:.1f} times per day)")
    print(f"  YAP links: Every {YAP_CHECK_INTERVAL_MINUTES} minutes ({24*60/YAP_CHECK_INTERVAL_MINUTES:.2f} times per day)")
    
    print("\n✅ Separate intervals test completed!")

if __name__ == "__main__":
    test_separate_intervals() 