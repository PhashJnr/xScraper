#!/usr/bin/env python3
"""
Clear Twitter Login Data from Chrome Profiles
Removes login sessions and cookies from both user and YAP Chrome profiles
"""

import os
import sys
import shutil
import logging
from config import CHROME_PROFILE_USER, CHROME_PROFILE_YAP, LOG_LEVEL, LOG_FILE

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def clear_profile_data(profile_path, profile_name):
    """Clear login data from a specific Chrome profile"""
    try:
        if not os.path.exists(profile_path):
            print(f"ℹ️ {profile_name} profile directory doesn't exist: {profile_path}")
            return False
        
        # Directories to clear (contain login data)
        data_dirs = [
            'Cookies',
            'Cookies-journal',
            'Login Data',
            'Login Data-journal',
            'Web Data',
            'Web Data-journal',
            'Local State',
            'Preferences',
            'Secure Preferences'
        ]
        
        cleared_items = []
        
        for data_file in data_dirs:
            file_path = os.path.join(profile_path, 'Default', data_file)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"  🗑️ Removed: {data_file}")
                    cleared_items.append(data_file)
                except Exception as e:
                    print(f"  ❌ Failed to remove {data_file}: {e}")
        
        # Also clear the entire Default directory if it exists
        default_dir = os.path.join(profile_path, 'Default')
        if os.path.exists(default_dir):
            try:
                shutil.rmtree(default_dir)
                print(f"  🗑️ Removed entire Default directory")
                cleared_items.append("Default directory")
            except Exception as e:
                print(f"  ❌ Failed to remove Default directory: {e}")
        
        if cleared_items:
            print(f"✅ Cleared {len(cleared_items)} items from {profile_name} profile")
            return True
        else:
            print(f"ℹ️ No login data found in {profile_name} profile")
            return False
            
    except Exception as e:
        print(f"❌ Error clearing {profile_name} profile: {e}")
        return False

def clear_all_profiles():
    """Clear login data from both Chrome profiles"""
    print("🧹 Clearing Twitter Login Data from Chrome Profiles")
    print("=" * 55)
    
    # Clear user monitoring profile
    print("\n📁 Clearing User Monitoring Profile...")
    user_cleared = clear_profile_data(CHROME_PROFILE_USER, "User Monitoring")
    
    # Clear YAP scraping profile
    print("\n📁 Clearing YAP Scraping Profile...")
    yap_cleared = clear_profile_data(CHROME_PROFILE_YAP, "YAP Scraping")
    
    # Summary
    print("\n" + "=" * 55)
    print("📋 Clear Summary:")
    print(f"  User Monitoring Profile: {'✅ Cleared' if user_cleared else 'ℹ️ No data'}")
    print(f"  YAP Scraping Profile: {'✅ Cleared' if yap_cleared else 'ℹ️ No data'}")
    
    if user_cleared or yap_cleared:
        print("\n🎉 Login data cleared successfully!")
        print("\n💡 Next Steps:")
        print("  1. Run 'python setup_twitter_login_user.py' to login to user profile")
        print("  2. Run 'python setup_twitter_login_yap.py' to login to YAP profile")
        print("  3. Test both services after login")
    else:
        print("\nℹ️ No login data was found to clear")
    
    return True

def force_clear_all_profiles():
    """Force clear all profile directories completely"""
    print("⚠️ Force Clearing All Chrome Profiles")
    print("=" * 40)
    print("This will completely remove both profile directories!")
    
    response = input("\nAre you sure you want to continue? (y/N): ")
    if response.lower() != 'y':
        print("❌ Operation cancelled")
        return False
    
    try:
        # Remove user profile directory
        if os.path.exists(CHROME_PROFILE_USER):
            shutil.rmtree(CHROME_PROFILE_USER)
            print(f"🗑️ Removed user profile: {CHROME_PROFILE_USER}")
        
        # Remove YAP profile directory
        if os.path.exists(CHROME_PROFILE_YAP):
            shutil.rmtree(CHROME_PROFILE_YAP)
            print(f"🗑️ Removed YAP profile: {CHROME_PROFILE_YAP}")
        
        print("\n✅ All profile directories removed completely!")
        print("\n💡 Next Steps:")
        print("  1. Run 'python setup_individual_profiles.py' to recreate profiles")
        print("  2. Run 'python setup_twitter_login_user.py' to login to user profile")
        print("  3. Run 'python setup_twitter_login_yap.py' to login to YAP profile")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during force clear: {e}")
        return False

def main():
    """Main function to clear login data"""
    print("Choose an option:")
    print("1. Clear login data only (recommended)")
    print("2. Force clear all profile directories")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "1":
        return clear_all_profiles()
    elif choice == "2":
        return force_clear_all_profiles()
    elif choice == "3":
        print("❌ Operation cancelled")
        return False
    else:
        print("❌ Invalid choice")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Operation interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1) 