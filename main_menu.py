#!/usr/bin/env python3
"""
Main menu for Twitter monitoring system
"""

import logging
import sys
import time
from config import LOG_LEVEL, LOG_FILE, CHECK_INTERVAL_MINUTES, YAP_CHECK_INTERVAL_MINUTES
from yap_scraper import YapSearchScraper
from main_scraper import TweetMonitorService
from main_yap_scraper import YapScraperService
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
logging.getLogger('selenium').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

def show_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("🐦 X User Tweet Monitor")
    print("="*50)
    print("1. 🧪 Test YAP Link Scraping (Single Run)")
    print("2. 🧪 Test User Tweet Monitoring (Single Run)")
    print("3. 🔄 Run YAP Link Scraper (Continuous - 18 hours)")
    print("4. 🔄 Run User Tweet Monitor (Continuous - 15 mins)")
    print("5. 📊 Check Configuration")
    print("6. 📁 Check Output Files")
    print("7. 🛑 Stop Monitor")
    print("8. ❌ Exit")
    print("="*50)

def run_yap_scraper_continuous():
    """Run YAP scraper continuously with 18-hour interval"""
    print(f"\n🔍 Starting YAP Search Scraper (Continuous - Every {YAP_CHECK_INTERVAL_MINUTES} minutes)...")
    
    try:
        service = YapScraperService()
        service.run_continuous()
    except Exception as e:
        logger.error(f"Error in YAP scraper service: {e}")
        print("❌ YAP scraper service failed!")

def run_user_monitor_continuous():
    """Run user tweet monitor continuously with 15-minute interval"""
    print(f"\n👥 Starting User Tweet Monitor (Continuous - Every {CHECK_INTERVAL_MINUTES} minutes)...")
    
    try:
        service = TweetMonitorService()
        service.run_continuous()
    except Exception as e:
        logger.error(f"Error in user monitor service: {e}")
        print("❌ User monitor service failed!")

def run_yap_scraper_test():
    """Run YAP scraper once for testing"""
    print("\n🧪 Testing YAP Search Scraper (Single Run)...")
    
    try:
        scraper = YapSearchScraper()
        success = scraper.run_yap_scraper()
        
        if success:
            print(f"\n✅ YAP scraper test completed!")
            print(f"📁 Results saved to: yap_links.txt")
        else:
            print("\n❌ YAP scraper test failed!")
            
    except Exception as e:
        logger.error(f"Error in YAP scraper test: {e}")
        print("❌ YAP scraper test failed!")

def run_user_monitor_test():
    """Run user tweet monitor once for testing"""
    print("\n🧪 Testing User Tweet Monitor (Single Run)...")
    
    try:
        service = TweetMonitorService()
        service.check_and_notify()
        print("\n✅ User monitor test completed!")
        
    except Exception as e:
        logger.error(f"Error in user monitor test: {e}")
        print("❌ User monitor test failed!")

def check_configuration():
    """Check current configuration"""
    print("\n📊 Current Configuration:")
    print("="*30)
    from config import print_config
    print_config()

def check_output_files():
    """Check output files"""
    print("\n📁 Output Files:")
    print("="*20)
    
    import os
    files_to_check = ['yap_links.txt', 'users_tweetlinks.txt', 'monitor.log']
    
    for file in files_to_check:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size} bytes)")
        else:
            print(f"❌ {file} (not found)")

def stop_monitor():
    """Stop running monitors"""
    print("\n🛑 Stopping monitors...")
    
    try:
        import subprocess
        import psutil
        
        # Find and kill monitor processes
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and any(script in ' '.join(cmdline) for script in ['main_scraper.py', 'main_yap_scraper.py']):
                    print(f"🔄 Stopping process {proc.info['pid']}")
                    proc.terminate()
                    proc.wait(timeout=10)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass
        
        print("✅ Monitor processes stopped")
        
    except Exception as e:
        logger.error(f"Error stopping monitors: {e}")
        print("❌ Error stopping monitors")

def main():
    """Main menu loop"""
    while True:
        try:
            show_menu()
            choice = input("\nSelect an option (1-8): ").strip()
            
            if choice == "1":
                run_yap_scraper_test()
            elif choice == "2":
                run_user_monitor_test()
            elif choice == "3":
                run_yap_scraper_continuous()
            elif choice == "4":
                run_user_monitor_continuous()
            elif choice == "5":
                check_configuration()
            elif choice == "6":
                check_output_files()
            elif choice == "7":
                stop_monitor()
            elif choice == "8":
                print("\n👋 Goodbye!")
                break
            else:
                print("❌ Invalid option. Please select 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error in main menu: {e}")
            print("❌ An error occurred!")

if __name__ == "__main__":
    main() 