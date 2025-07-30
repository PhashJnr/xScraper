#!/usr/bin/env python3
"""
Fix Chrome profile issues for VPS deployment
"""

import os
import subprocess
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def kill_chrome_processes():
    """Kill all Chrome processes"""
    try:
        # Kill Chrome processes
        subprocess.run(['pkill', 'chrome'], check=False)
        subprocess.run(['pkill', 'chromedriver'], check=False)
        
        # Force kill if needed
        subprocess.run(['pkill', '-9', 'chrome'], check=False)
        subprocess.run(['pkill', '-9', 'chromedriver'], check=False)
        
        time.sleep(2)
        logger.info("✅ Chrome processes killed")
        
    except Exception as e:
        logger.error(f"Error killing Chrome processes: {e}")

def clean_chrome_profile():
    """Clean up Chrome profile directory"""
    try:
        chrome_profile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrome_profile')
        
        # Remove existing profile
        if os.path.exists(chrome_profile):
            subprocess.run(['rm', '-rf', chrome_profile], check=True)
            logger.info("✅ Removed existing Chrome profile")
        
        # Create fresh directory
        os.makedirs(chrome_profile, exist_ok=True)
        os.chmod(chrome_profile, 0o700)
        logger.info("✅ Created fresh Chrome profile directory")
        
    except Exception as e:
        logger.error(f"Error cleaning Chrome profile: {e}")

def test_chrome_setup():
    """Test Chrome setup"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        # Use fresh profile
        chrome_profile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrome_profile')
        chrome_options.add_argument(f'--user-data-dir={chrome_profile}')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.google.com')
        time.sleep(2)
        driver.quit()
        
        logger.info("✅ Chrome setup test successful")
        return True
        
    except Exception as e:
        logger.error(f"Chrome setup test failed: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Fixing Chrome Profile Issues")
    print("="*40)
    
    # Step 1: Kill Chrome processes
    print("1. Killing Chrome processes...")
    kill_chrome_processes()
    
    # Step 2: Clean profile
    print("2. Cleaning Chrome profile...")
    clean_chrome_profile()
    
    # Step 3: Test setup
    print("3. Testing Chrome setup...")
    if test_chrome_setup():
        print("✅ Chrome setup fixed successfully!")
        print("🚀 Ready to run services")
    else:
        print("❌ Chrome setup still has issues")
        print("💡 Try restarting the server")

if __name__ == "__main__":
    main() 