#!/usr/bin/env python3
"""
Check YAP search configuration settings
"""

import os
from config import *

def check_yap_config():
    """Display current YAP search configuration"""
    print("🔍 YAP Search Configuration Checker")
    print("=" * 50)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found - using default values")
    
    print("\n📋 Current YAP Search Settings:")
    print("-" * 40)
    
    # Search Keywords
    print(f"🔤 Search Keywords: {YAP_SEARCH_KEYWORDS}")
    
    # Account Filters
    print(f"✅ Verified Only: {YAP_FILTER_VERIFIED}")
    
    # Content Type Filters
    print(f"🔄 Exclude Native Retweets: {YAP_FILTER_NATIVE_RETWEETS}")
    print(f"🔄 Exclude Retweets: {YAP_FILTER_RETWEETS}")
    print(f"💬 Exclude Replies: {YAP_FILTER_REPLIES}")
    
    # Engagement Filters
    print(f"💬 Min Replies: {YAP_MIN_REPLIES}")
    print(f"❤️  Min Likes: {YAP_MIN_LIKES}")
    print(f"🔄 Min Retweets: {YAP_MIN_RETWEETS}")
    
    # Language and Time
    print(f"🌐 Language: {YAP_LANGUAGE}")
    print(f"⏰ Time Window: {YAP_TIME_WINDOW} minutes ({YAP_TIME_WINDOW/60:.1f} hours)")
    
    # Content Filters
    print(f"🔗 Links Only: {YAP_FILTER_LINKS}")
    print(f"📷 Media Only: {YAP_FILTER_MEDIA}")
    print(f"🖼️  Images Only: {YAP_FILTER_IMAGES}")
    print(f"🎥 Videos Only: {YAP_FILTER_VIDEOS}")
    
    # Search Source
    print(f"🔍 Search Source: {YAP_SEARCH_SOURCE}")
    
    # Build and show the actual query
    print("\n🔍 Generated Search Query:")
    print("-" * 30)
    
    try:
        from yap_scraper import YapSearchScraper
        scraper = YapSearchScraper()
        query = scraper._build_yap_search_query()
        print(f"Query: {query}")
        scraper.cleanup()
    except Exception as e:
        print(f"Error building query: {e}")
    
    print("\n💡 Tips:")
    print("- Edit .env file to change YAP search settings")
    print("- Test your query with: python test_simplified_yap.py")
    print("- All YAP settings can be configured via .env file")

if __name__ == "__main__":
    check_yap_config() 