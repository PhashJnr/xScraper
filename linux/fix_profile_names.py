#!/usr/bin/env python3
"""
Fix Profile Names - Clean up old profiles and create fresh ones with proper names
"""

import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import CHROME_BINARY_PATH, CHROME_PROFILE_USER, CHROME_PROFILE_YAP

def cleanup_old_profiles():
    """Remove all old profile directories"""
    print("🧹 Cleaning up old profile directories...")
    
    # Remove any profile directories that start with chrome_profile_ in current dir
    current_dir = os.getcwd()
    for item in os.listdir(current_dir):
        if item.startswith('chrome_profile_'):
            full_path = os.path.join(current_dir, item)
            if os.path.isdir(full_path):
                try:
                    shutil.rmtree(full_path)
                    print(f"✅ Removed: {item}")
                except Exception as e:
                    print(f"❌ Failed to remove {item}: {e}")
    
    # Also clean up /tmp profiles
    try:
        import glob
        tmp_profiles = glob.glob("/tmp/chrome_profile_*")
        for profile in tmp_profiles:
            try:
                if os.path.isdir(profile):
                    shutil.rmtree(profile)
                    print(f"✅ Removed /tmp profile: {profile}")
            except Exception as e:
                print(f"❌ Failed to remove /tmp profile {profile}: {e}")
    except Exception as e:
        print(f"⚠️ Error cleaning /tmp profiles: {e}")

def kill_chrome_processes():
    """Kill any existing Chrome processes"""
    print("🔪 Killing Chrome processes...")
    
    try:
        import psutil
        killed_count = 0
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name']
                if proc_name and 'chrome' in proc_name.lower():
                    proc.terminate()
                    killed_count += 1
                    print(f"✅ Killed Chrome process: {proc.pid}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        print(f"   Killed {killed_count} Chrome processes")
        
        # Wait a moment for processes to fully terminate
        time.sleep(3)
        
    except Exception as e:
        print(f"⚠️ Error killing Chrome processes: {e}")

def create_profile(profile_name, profile_type):
    """Create a fresh Chrome profile"""
    print(f"📁 Creating {profile_type} profile: {profile_name}")
    
    try:
        # Create profile in /tmp directory
        profile_path = f"/tmp/{profile_name}"
        
        # Ensure the directory exists
        os.makedirs(profile_path, exist_ok=True)
        
        # Setup Chrome options
        options = Options()
        options.binary_location = CHROME_BINARY_PATH
        options.add_argument(f'--user-data-dir={profile_path}')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-logging')
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        
        # Test the profile
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.google.com')
        print(f"✅ {profile_type} profile created successfully: {profile_path}")
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Failed to create {profile_type} profile: {e}")
        return False

def main():
    """Main function to fix profile names"""
    print("🔧 Fixing Profile Names")
    print("=" * 50)
    
    # Step 1: Clean up old profiles
    cleanup_old_profiles()
    
    # Step 2: Kill Chrome processes
    kill_chrome_processes()
    
    # Step 3: Create fresh profiles with proper names
    print("\n📁 Creating fresh profiles with proper names...")
    
    user_success = create_profile(CHROME_PROFILE_USER, "User")
    yap_success = create_profile(CHROME_PROFILE_YAP, "YAP")
    
    # Step 4: Summary
    print("\n" + "=" * 50)
    print("📋 Profile Setup Summary:")
    print(f"  User Profile: {'✅ Success' if user_success else '❌ Failed'}")
    print(f"  YAP Profile: {'✅ Success' if yap_success else '❌ Failed'}")
    
    if user_success and yap_success:
        print("\n✅ All profiles created successfully!")
        print("💡 Next Steps:")
        print("  1. Run 'python3 setup_twitter_login_user.py' to login to Twitter")
        print("  2. Run 'python3 setup_twitter_login_yap.py' to login to Twitter")
        print("  3. Test scrapers: 'python3 main_scraper_locked_pc.py'")
    else:
        print("\n❌ Some profiles failed to create. Please check the logs.")

if __name__ == "__main__":
    main() 