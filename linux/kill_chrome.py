#!/usr/bin/env python3
"""
Chrome Process Killer - Kills all Chrome and ChromeDriver processes
"""

import psutil
import subprocess
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def kill_all_chrome_processes():
    """Kill ALL Chrome and ChromeDriver processes"""
    try:
        logger.info("🔪 Starting Chrome process cleanup...")
        
        killed_count = 0
        
        # Method 1: Kill using psutil
        logger.info("📋 Scanning for Chrome processes...")
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                proc_name = proc.info['name']
                if proc_name and ('chrome' in proc_name.lower() or 'chromedriver' in proc_name.lower()):
                    logger.info(f"Found Chrome process: {proc.pid} ({proc_name})")
                    proc.terminate()
                    proc.wait(timeout=3)
                    killed_count += 1
                    logger.info(f"✅ Terminated process: {proc.pid}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                try:
                    # Force kill if terminate fails
                    proc.kill()
                    killed_count += 1
                    logger.info(f"✅ Force killed process: {proc.pid}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            except Exception as e:
                logger.warning(f"Error killing process {proc.pid}: {e}")
        
        # Method 2: Kill using system commands
        logger.info("🔧 Using system commands for additional cleanup...")
        system_commands = [
            ['pkill', '-f', 'chrome'],
            ['pkill', '-f', 'chromedriver'],
            ['pkill', '-f', 'google-chrome'],
            ['pkill', '-f', 'chromium'],
            ['killall', 'chrome'],
            ['killall', 'chromedriver'],
            ['killall', 'google-chrome']
        ]
        
        for cmd in system_commands:
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=5)
                if result.returncode == 0:
                    logger.info(f"✅ System command successful: {' '.join(cmd)}")
            except Exception as e:
                logger.debug(f"System command failed: {' '.join(cmd)} - {e}")
        
        # Wait for processes to fully terminate
        time.sleep(3)
        
        # Final check
        remaining_chrome = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name']
                if proc_name and ('chrome' in proc_name.lower() or 'chromedriver' in proc_name.lower()):
                    remaining_chrome.append(f"{proc.pid} ({proc_name})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if remaining_chrome:
            logger.warning(f"⚠️ Remaining Chrome processes: {', '.join(remaining_chrome)}")
        else:
            logger.info("✅ All Chrome processes successfully killed!")
        
        logger.info(f"🎯 Cleanup Summary: Killed {killed_count} processes via psutil")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during Chrome cleanup: {e}")
        return False

def main():
    """Main function"""
    print("🧹 Chrome Process Cleanup Tool")
    print("=" * 40)
    
    success = kill_all_chrome_processes()
    
    if success:
        print("\n✅ Chrome cleanup completed successfully!")
        print("💡 You can now run your scrapers safely.")
    else:
        print("\n❌ Chrome cleanup encountered issues.")
        print("💡 You may need to run with sudo or check permissions.")

if __name__ == "__main__":
    main() 