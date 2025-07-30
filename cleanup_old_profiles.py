#!/usr/bin/env python3
"""
Cleanup Old Chrome Profiles and Processes
Removes old shared profiles and kills conflicting Chrome processes
"""

import os
import sys
import psutil
import logging
from config import LOG_LEVEL, LOG_FILE

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

def kill_chrome_processes():
    """Kill all Chrome and ChromeDriver processes"""
    try:
        killed_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                proc_name = proc.info['name']
                if proc_name and any(name in proc_name.lower() for name in ['chrome', 'chromedriver']):
                    logger.info(f"Killing process: {proc_name} (PID: {proc.pid})")
                    proc.terminate()
                    proc.wait(timeout=5)
                    killed_processes.append(proc.pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                continue
        
        if killed_processes:
            logger.info(f"Killed {len(killed_processes)} Chrome processes")
        else:
            logger.info("No Chrome processes found to kill")
            
        return len(killed_processes)
        
    except Exception as e:
        logger.error(f"Error killing Chrome processes: {e}")
        return 0

def remove_old_profiles():
    """Remove old Chrome profile directories"""
    try:
        removed_dirs = []
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # List of old profile directories to remove
        old_profiles = [
            os.path.join(current_dir, 'chrome_profile'),
            os.path.join(current_dir, 'chrome_profile_user'),
            os.path.join(current_dir, 'chrome_profile_yap'),
            os.path.join(current_dir, 'chrome_profile_old'),
            os.path.join(current_dir, 'chrome_profile_backup')
        ]
        
        for profile_dir in old_profiles:
            if os.path.exists(profile_dir):
                try:
                    import shutil
                    shutil.rmtree(profile_dir)
                    logger.info(f"Removed old profile directory: {profile_dir}")
                    removed_dirs.append(profile_dir)
                except Exception as e:
                    logger.error(f"Failed to remove {profile_dir}: {e}")
        
        return removed_dirs
        
    except Exception as e:
        logger.error(f"Error removing old profiles: {e}")
        return []

def cleanup_system_chrome():
    """Clean up system Chrome cache and config"""
    try:
        cleaned_items = []
        
        # System Chrome directories to clean
        system_dirs = [
            os.path.expanduser('~/.config/google-chrome'),
            os.path.expanduser('~/.cache/google-chrome'),
            os.path.expanduser('~/.local/share/google-chrome')
        ]
        
        for dir_path in system_dirs:
            if os.path.exists(dir_path):
                try:
                    import shutil
                    shutil.rmtree(dir_path)
                    logger.info(f"Cleaned system Chrome directory: {dir_path}")
                    cleaned_items.append(dir_path)
                except Exception as e:
                    logger.error(f"Failed to clean {dir_path}: {e}")
        
        return cleaned_items
        
    except Exception as e:
        logger.error(f"Error cleaning system Chrome: {e}")
        return []

def main():
    """Main cleanup function"""
    print("🧹 Cleaning up Old Chrome Profiles and Processes")
    print("=" * 55)
    
    # Step 1: Kill Chrome processes
    print("\n🔪 Killing Chrome processes...")
    killed_count = kill_chrome_processes()
    print(f"   Killed {killed_count} Chrome processes")
    
    # Step 2: Remove old profile directories
    print("\n🗑️ Removing old profile directories...")
    removed_dirs = remove_old_profiles()
    print(f"   Removed {len(removed_dirs)} old profile directories")
    
    # Step 3: Clean system Chrome (optional)
    print("\n🧼 Cleaning system Chrome cache...")
    cleaned_items = cleanup_system_chrome()
    print(f"   Cleaned {len(cleaned_items)} system directories")
    
    # Summary
    print("\n" + "=" * 55)
    print("📋 Cleanup Summary:")
    print(f"  Chrome processes killed: {killed_count}")
    print(f"  Profile directories removed: {len(removed_dirs)}")
    print(f"  System directories cleaned: {len(cleaned_items)}")
    
    if killed_count > 0 or removed_dirs or cleaned_items:
        print("\n✅ Cleanup completed successfully!")
        print("\n💡 Next Steps:")
        print("  1. Run 'python3 setup_individual_profiles.py' to create new profiles")
        print("  2. Run 'python3 setup_twitter_login.py' to login to Twitter")
    else:
        print("\nℹ️ No cleanup needed - everything was already clean")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Cleanup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error during cleanup: {e}")
        sys.exit(1) 