#!/usr/bin/env python3
"""
Cleanup script to remove any leftover unique Chrome profile directories
"""

import os
import glob
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_unique_profiles():
    """Clean up any leftover unique Chrome profile directories"""
    try:
        # Get the project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Find all unique profile directories
        profile_pattern = os.path.join(project_dir, 'chrome_profile_*')
        profile_dirs = glob.glob(profile_pattern)
        
        if not profile_dirs:
            logger.info("No unique profile directories found to clean up")
            return
        
        logger.info(f"Found {len(profile_dirs)} unique profile directories to clean up")
        
        # Remove each unique profile directory
        for profile_dir in profile_dirs:
            try:
                shutil.rmtree(profile_dir)
                logger.info(f"Cleaned up: {profile_dir}")
            except Exception as e:
                logger.error(f"Could not clean up {profile_dir}: {e}")
        
        logger.info("Profile cleanup completed!")
        
    except Exception as e:
        logger.error(f"Error during profile cleanup: {e}")

if __name__ == "__main__":
    print("Cleaning up unique Chrome profile directories...")
    cleanup_unique_profiles() 