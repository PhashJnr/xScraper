#!/usr/bin/env python3
"""
Force stop script for Windows - more aggressive process termination
"""

import os
import subprocess
import psutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def force_stop_monitor():
    """Force stop all monitor and Chrome processes"""
    try:
        killed_processes = []
        
        # Find and kill Python processes running our scripts
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and any(script in ' '.join(cmdline) for script in ['main_scraper.py', 'main.py']):
                    logger.info(f"Killing monitor process: {proc.info['pid']}")
                    proc.kill()
                    killed_processes.append(f"Monitor (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        # Kill all Chrome processes (more aggressive)
        chrome_killed = 0
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                    logger.info(f"Killing Chrome process: {proc.info['pid']}")
                    proc.kill()
                    chrome_killed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        if chrome_killed > 0:
            killed_processes.append(f"Chrome processes ({chrome_killed})")
        
        # Use Windows taskkill as backup
        try:
            subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], 
                         capture_output=True, timeout=10)
            logger.info("Used taskkill to force close Chrome")
        except Exception as e:
            logger.debug(f"taskkill failed: {e}")
        
        if killed_processes:
            logger.info(f"Force killed: {', '.join(killed_processes)}")
            return True
        else:
            logger.info("No processes found to kill")
            return False
            
    except Exception as e:
        logger.error(f"Error force stopping: {e}")
        return False

if __name__ == "__main__":
    print("Force stopping Twitter monitor...")
    if force_stop_monitor():
        print("✅ Monitor force stopped")
    else:
        print("❌ No processes found or error occurred") 