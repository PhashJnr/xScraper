#!/usr/bin/env python3
"""
Interactive setup script for .env configuration
"""

import os
import shutil

def setup_env():
    """Interactive .env setup"""
    print("Twitter Scraper & Monitor - Environment Setup")
    print("="*50)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        choice = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if choice != 'y':
            print("Setup cancelled.")
            return
    
    # Copy from example
    if os.path.exists('env_example.txt'):
        shutil.copy('env_example.txt', '.env')
        print("✅ Created .env file from env_example.txt")
    else:
        print("❌ env_example.txt not found!")
        return
    
    # Interactive configuration
    print("\nCustomize your settings:")
    print("(Press Enter to keep default values)")
    
    # Read current .env
    with open('.env', 'r') as f:
        content = f.read()
    
    # Get user preferences
    max_tweets = input(f"MAX_TWEETS_TO_SCRAPE (default: 50): ").strip()
    if max_tweets:
        content = content.replace('MAX_TWEETS_TO_SCRAPE=50', f'MAX_TWEETS_TO_SCRAPE={max_tweets}')
    
    check_interval = input(f"CHECK_INTERVAL_MINUTES (default: 15): ").strip()
    if check_interval:
        content = content.replace('CHECK_INTERVAL_MINUTES=15', f'CHECK_INTERVAL_MINUTES={check_interval}')
    
    log_level = input(f"LOG_LEVEL (default: INFO): ").strip()
    if log_level:
        content = content.replace('LOG_LEVEL=INFO', f'LOG_LEVEL={log_level}')
    
    # Write updated .env
    with open('.env', 'w') as f:
        f.write(content)
    
    print("\n✅ .env file configured!")
    print("\nNext steps:")
    print("1. Edit .env file to add your API keys")
    print("2. Run 'python check_config.py' to verify settings")
    print("3. Run 'python main_menu.py' to start the application")

if __name__ == "__main__":
    setup_env() 