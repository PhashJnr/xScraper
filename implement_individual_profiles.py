#!/usr/bin/env python3
"""
Implement Individual Chrome Profiles for Multi-Service VPS
"""

import os
import re

def update_scraper_monitor_for_user_profile():
    """Update scraper_monitor.py to use chrome_profile_user"""
    try:
        with open('scraper_monitor.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the profile directory setup
        old_profile_setup = '''    def setup_driver(self):
        """Setup Chrome driver with single main profile directory"""
        try:
            # Use single main profile directory
            profile_dir = os.path.join(self.project_dir, 'chrome_profile')
            
            # Ensure the directory exists
            os.makedirs(profile_dir, exist_ok=True)'''
        
        new_profile_setup = '''    def setup_driver(self):
        """Setup Chrome driver with user-specific profile directory"""
        try:
            # Use user-specific profile directory for user monitoring service
            profile_dir = os.path.join(self.project_dir, 'chrome_profile_user')
            
            # Ensure the directory exists
            os.makedirs(profile_dir, exist_ok=True)'''
        
        content = content.replace(old_profile_setup, new_profile_setup)
        
        with open('scraper_monitor.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated scraper_monitor.py to use chrome_profile_user")
        return True
        
    except Exception as e:
        print(f"❌ Error updating scraper_monitor.py: {e}")
        return False

def update_yap_scraper_for_yap_profile():
    """Update yap_scraper.py to use chrome_profile_yap"""
    try:
        with open('yap_scraper.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the profile directory setup
        old_profile_setup = '''    def setup_driver(self):
        """Setup Chrome driver with single main profile directory"""
        try:
            # Use single main profile directory
            profile_dir = os.path.join(self.project_dir, 'chrome_profile')
            
            # Ensure the directory exists
            os.makedirs(profile_dir, exist_ok=True)'''
        
        new_profile_setup = '''    def setup_driver(self):
        """Setup Chrome driver with YAP-specific profile directory"""
        try:
            # Use YAP-specific profile directory for YAP scraping service
            profile_dir = os.path.join(self.project_dir, 'chrome_profile_yap')
            
            # Ensure the directory exists
            os.makedirs(profile_dir, exist_ok=True)'''
        
        content = content.replace(old_profile_setup, new_profile_setup)
        
        with open('yap_scraper.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated yap_scraper.py to use chrome_profile_yap")
        return True
        
    except Exception as e:
        print(f"❌ Error updating yap_scraper.py: {e}")
        return False

def update_setup_twitter_login_for_individual_profiles():
    """Update setup_twitter_login.py to support individual profiles"""
    try:
        with open('setup_twitter_login.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the Chrome profile setup section
        old_profile_setup = '''        # Profile directory
        chrome_profile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chrome_profile')
        chrome_options.add_argument(f'--user-data-dir={chrome_profile}')'''
        
        new_profile_setup = '''        # Profile directory - use environment variable or default
        profile_name = os.getenv('CHROME_PROFILE', 'chrome_profile')
        chrome_profile = os.path.join(os.path.dirname(os.path.abspath(__file__)), profile_name)
        chrome_options.add_argument(f'--user-data-dir={chrome_profile}')'''
        
        content = content.replace(old_profile_setup, new_profile_setup)
        
        with open('setup_twitter_login.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated setup_twitter_login.py to support individual profiles")
        return True
        
    except Exception as e:
        print(f"❌ Error updating setup_twitter_login.py: {e}")
        return False

def create_profile_setup_script():
    """Create a script to setup individual profiles"""
    script_content = '''#!/usr/bin/env python3
"""
Setup Individual Chrome Profiles for Multi-Service VPS
"""

import os
import subprocess
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_individual_profiles():
    """Setup individual Chrome profiles for each service"""
    try:
        # Kill all Chrome processes first
        logger.info("Killing all Chrome processes...")
        subprocess.run(['sudo', 'pkill', 'chrome'], check=False)
        subprocess.run(['sudo', 'pkill', 'chromedriver'], check=False)
        time.sleep(2)
        subprocess.run(['sudo', 'pkill', '-9', 'chrome'], check=False)
        subprocess.run(['sudo', 'pkill', '-9', 'chromedriver'], check=False)
        time.sleep(2)
        
        # Create individual profile directories
        profiles = ['chrome_profile_user', 'chrome_profile_yap']
        
        for profile in profiles:
            profile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), profile)
            
            # Remove existing profile
            if os.path.exists(profile_path):
                import shutil
                shutil.rmtree(profile_path)
                logger.info(f"Removed existing {profile}")
            
            # Create new profile
            os.makedirs(profile_path, mode=0o700, exist_ok=True)
            logger.info(f"Created new {profile}")
        
        # Setup Twitter login for user profile
        logger.info("Setting up Twitter login for user profile...")
        os.environ['CHROME_PROFILE'] = 'chrome_profile_user'
        subprocess.run(['python3', 'setup_twitter_login.py'], check=True)
        
        # Setup Twitter login for YAP profile
        logger.info("Setting up Twitter login for YAP profile...")
        os.environ['CHROME_PROFILE'] = 'chrome_profile_yap'
        subprocess.run(['python3', 'setup_twitter_login.py'], check=True)
        
        logger.info("✅ Individual Chrome profiles setup completed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error setting up individual profiles: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Setting up Individual Chrome Profiles")
    print("="*45)
    
    if setup_individual_profiles():
        print("✅ Individual Chrome profiles setup successful!")
        print("🔄 Restart services to use individual profiles:")
        print("   sudo systemctl restart tweet-monitor-user")
        print("   sudo systemctl restart tweet-monitor-yap")
    else:
        print("❌ Individual Chrome profiles setup failed!")

if __name__ == "__main__":
    main()
'''
    
    with open('setup_individual_profiles.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Created setup_individual_profiles.py")

def main():
    """Main function to implement individual Chrome profiles"""
    print("🔧 Implementing Individual Chrome Profiles for Multi-Service VPS")
    print("="*60)
    
    # Step 1: Update scraper_monitor.py
    print("1. Updating scraper_monitor.py for user profile...")
    if update_scraper_monitor_for_user_profile():
        print("✅ scraper_monitor.py updated")
    else:
        print("❌ Failed to update scraper_monitor.py")
        return
    
    # Step 2: Update yap_scraper.py
    print("2. Updating yap_scraper.py for YAP profile...")
    if update_yap_scraper_for_yap_profile():
        print("✅ yap_scraper.py updated")
    else:
        print("❌ Failed to update yap_scraper.py")
        return
    
    # Step 3: Update setup_twitter_login.py
    print("3. Updating setup_twitter_login.py for individual profiles...")
    if update_setup_twitter_login_for_individual_profiles():
        print("✅ setup_twitter_login.py updated")
    else:
        print("❌ Failed to update setup_twitter_login.py")
        return
    
    # Step 4: Create setup script
    print("4. Creating individual profile setup script...")
    create_profile_setup_script()
    
    print("\n🚀 Individual Chrome profiles implementation completed!")
    print("📋 Next steps:")
    print("   1. Run: python3 setup_individual_profiles.py")
    print("   2. Restart services: sudo systemctl restart tweet-monitor-user tweet-monitor-yap")
    print("   3. Check status: sudo systemctl status tweet-monitor-user tweet-monitor-yap")

if __name__ == "__main__":
    main() 