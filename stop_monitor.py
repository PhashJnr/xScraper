#!/usr/bin/env python3
"""
Simple script to stop the Twitter monitor
"""

import os
import signal
import psutil
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def stop_monitor():
    """Stop the Twitter monitor process"""
    try:
        # Find Python processes running main_scraper.py
        monitor_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and 'main_scraper.py' in ' '.join(cmdline):
                    monitor_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        if not monitor_processes:
            logger.info("No monitor process found")
            return False
        
        # Also find and kill Chrome processes that might be orphaned
        chrome_processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                    chrome_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        

        
        logger.info(f"Found {len(monitor_processes)} monitor process(es) and {len(chrome_processes)} Chrome process(es)")
        
        # Kill monitor processes first
        for proc in monitor_processes:
            try:
                logger.info(f"Terminating monitor process (PID: {proc.info['pid']})")
                proc.terminate()
            except Exception as e:
                logger.warning(f"Error terminating monitor process: {e}")
        
        # Wait for graceful shutdown
        for proc in monitor_processes:
            try:
                proc.wait(timeout=15)
                logger.info(f"Monitor process {proc.info['pid']} stopped gracefully")
            except psutil.TimeoutExpired:
                logger.warning(f"Monitor process {proc.info['pid']} didn't stop gracefully, forcing...")
                try:
                    proc.kill()
                    logger.info(f"Monitor process {proc.info['pid']} force stopped")
                except Exception as e:
                    logger.error(f"Error force killing monitor process: {e}")
        
        # Kill Chrome processes if they're still running
        for proc in chrome_processes:
            try:
                logger.info(f"Terminating Chrome process (PID: {proc.info['pid']})")
                proc.terminate()
                proc.wait(timeout=5)
            except psutil.TimeoutExpired:
                try:
                    proc.kill()
                    logger.info(f"Chrome process {proc.info['pid']} force stopped")
                except Exception as e:
                    logger.debug(f"Error killing Chrome process: {e}")
            except Exception as e:
                logger.debug(f"Error terminating Chrome process: {e}")
        
        logger.info("All processes stopped")
        return True
        
    except Exception as e:
        logger.error(f"Error stopping monitor: {e}")
        return False

if __name__ == "__main__":
    print("Stopping Twitter monitor...")
    if stop_monitor():
        print("✅ Monitor stopped successfully")
    else:
        print("❌ No monitor process found or error occurred") 