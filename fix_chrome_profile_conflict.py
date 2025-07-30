#!/usr/bin/env python3
"""
Fix Chrome Profile Conflicts
"""

import os
import shutil
import subprocess
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_chrome_profile_conflicts():
    """Fix Chrome profile conflicts by using unique profiles"""
    try:
        # Kill all Chrome processes
        logger.info("Killing all Chrome processes...")
        subprocess.run(['sudo', 'pkill', 'chrome'], check=False)
        subprocess.run(['sudo', 'pkill', 'chromedriver'], check=False)
        time.sleep(2)
        subprocess.run(['sudo', 'pkill', '-9', 'chrome'], check=False)
        subprocess.run(['sudo', 'pkill', '-9', 'chromedriver'], check=False)
        time.sleep(2)
        
        # Create unique profiles for each service
        profiles = ['chrome_profile_user', 'chrome_profile_yap']
        
        for profile in profiles:
            profile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), profile)
            
            # Remove existing profile
            if os.path.exists(profile_path):
                shutil.rmtree(profile_path)
                logger.info(f"Removed existing {profile}")
            
            # Create new profile
            os.makedirs(profile_path, mode=0o700, exist_ok=True)
            logger.info(f"Created new {profile}")
        
        # Copy login data to both profiles
        logger.info("Setting up Twitter login for both profiles...")
        
        # Setup login for user profile
        os.environ['CHROME_PROFILE'] = 'chrome_profile_user'
        subprocess.run(['python3', 'setup_twitter_login.py'], check=True)
        
        # Setup login for YAP profile  
        os.environ['CHROME_PROFILE'] = 'chrome_profile_yap'
        subprocess.run(['python3', 'setup_twitter_login.py'], check=True)
        
        logger.info("✅ Chrome profile conflicts fixed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error fixing Chrome profile conflicts: {e}")
        return False

def update_service_files():
    """Update service files to use unique Chrome profiles"""
    try:
        # Update scraper_monitor.py to use user profile
        with open('scraper_monitor.py', 'r') as f:
            content = f.read()
        
        # Replace chrome_profile with chrome_profile_user
        content = content.replace("'chrome_profile'", "'chrome_profile_user'")
        
        with open('scraper_monitor.py', 'w') as f:
            f.write(content)
        
        # Update yap_scraper.py to use YAP profile
        with open('yap_scraper.py', 'r') as f:
            content = f.read()
        
        # Replace chrome_profile with chrome_profile_yap
        content = content.replace("'chrome_profile'", "'chrome_profile_yap'")
        
        with open('yap_scraper.py', 'w') as f:
            f.write(content)
        
        logger.info("✅ Service files updated with unique Chrome profiles")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error updating service files: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Fixing Chrome Profile Conflicts")
    print("="*40)
    
    # Step 1: Fix Chrome profile conflicts
    print("1. Fixing Chrome profile conflicts...")
    if fix_chrome_profile_conflicts():
        print("✅ Chrome profile conflicts fixed")
    else:
        print("❌ Failed to fix Chrome profile conflicts")
        return
    
    # Step 2: Update service files
    print("2. Updating service files...")
    if update_service_files():
        print("✅ Service files updated")
    else:
        print("❌ Failed to update service files")
        return
    
    print("\n🚀 Chrome profile conflicts resolved!")
    print("🔄 Restart services to apply changes:")
    print("   sudo systemctl restart tweet-monitor-user")
    print("   sudo systemctl restart tweet-monitor-yap")

if __name__ == "__main__":
    main() 