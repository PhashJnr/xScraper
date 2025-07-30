#!/usr/bin/env python3
"""
Suppress Chrome Debug Output
"""

import os
import re

def update_chrome_options_in_file(file_path):
    """Update Chrome options to suppress debug output"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add Chrome debug suppression options
        debug_suppression_options = [
            'chrome_options.add_argument("--log-level=3")',
            'chrome_options.add_argument("--silent")',
            'chrome_options.add_argument("--disable-logging")',
            'chrome_options.add_argument("--disable-logging-redirect")',
            'chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])',
            'chrome_options.add_experimental_option("useAutomationExtension", False)',
            'chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])',
            'chrome_options.add_argument("--disable-dev-shm-usage")',
            'chrome_options.add_argument("--disable-gpu-sandbox")',
            'chrome_options.add_argument("--disable-software-rasterizer")',
            'chrome_options.add_argument("--disable-background-timer-throttling")',
            'chrome_options.add_argument("--disable-backgrounding-occluded-windows")',
            'chrome_options.add_argument("--disable-renderer-backgrounding")',
            'chrome_options.add_argument("--disable-background-networking")',
            'chrome_options.add_argument("--disable-default-apps")',
            'chrome_options.add_argument("--disable-sync")',
            'chrome_options.add_argument("--disable-translate")',
            'chrome_options.add_argument("--hide-scrollbars")',
            'chrome_options.add_argument("--mute-audio")',
            'chrome_options.add_argument("--no-first-run")',
            'chrome_options.add_argument("--disable-popup-blocking")',
            'chrome_options.add_argument("--disable-prompt-on-repost")',
            'chrome_options.add_argument("--disable-hang-monitor")',
            'chrome_options.add_argument("--disable-client-side-phishing-detection")',
            'chrome_options.add_argument("--disable-component-update")',
            'chrome_options.add_argument("--disable-domain-reliability")',
            'chrome_options.add_argument("--disable-ipc-flooding-protection")',
            'chrome_options.add_argument("--disable-blink-features=AutomationControlled")',
            'chrome_options.add_argument("--disable-web-security")',
            'chrome_options.add_argument("--disable-features=VizDisplayCompositor")',
            'chrome_options.add_argument("--disable-extensions")',
            'chrome_options.add_argument("--disable-plugins")',
            'chrome_options.add_argument("--disable-images")',
            'chrome_options.add_argument("--disable-javascript")',
            'chrome_options.add_argument("--memory-pressure-off")',
            'chrome_options.add_argument("--max_old_space_size=512")',
            'chrome_options.add_argument("--single-process")',
            'chrome_options.add_argument("--window-size=1920,1080")',
            'chrome_options.add_argument("--start-maximized")',
            'chrome_options.add_argument("--disable-infobars")',
            'chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")'
        ]
        
        # Find where Chrome options are defined
        if 'chrome_options = Options()' in content:
            # Find the line after chrome_options = Options()
            lines = content.split('\n')
            new_lines = []
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                
                # After chrome_options = Options(), add our suppression options
                if line.strip() == 'chrome_options = Options()':
                    # Add a comment
                    new_lines.append('        # Suppress Chrome debug output')
                    # Add all suppression options
                    for option in debug_suppression_options:
                        new_lines.append(f'        {option}')
            
            updated_content = '\n'.join(new_lines)
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Updated {file_path} with Chrome debug suppression")
            return True
        else:
            print(f"⚠️  Could not find Chrome options in {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def main():
    """Main function to suppress Chrome debug output"""
    print("🔇 Suppressing Chrome Debug Output")
    print("="*40)
    
    # Files to update
    files_to_update = [
        'scraper_monitor.py',
        'yap_scraper.py',
        'setup_twitter_login.py'
    ]
    
    updated_count = 0
    for file_path in files_to_update:
        if os.path.exists(file_path):
            if update_chrome_options_in_file(file_path):
                updated_count += 1
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print(f"\n✅ Updated {updated_count} files with Chrome debug suppression")
    print("🔄 Restart services to apply changes:")
    print("   sudo systemctl restart tweet-monitor-user")
    print("   sudo systemctl restart tweet-monitor-yap")

if __name__ == "__main__":
    main() 