#!/usr/bin/env python3
"""
Check if output files exist and show their contents
"""

import os
import sys

def check_output_files():
    """Check if output files exist and show their contents"""
    print("Checking output files...")
    print("="*50)
    
    # Get project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Project directory: {project_dir}")
    print()
    
    # Check yap_links.txt
    yap_file = os.path.join(project_dir, "yap_links.txt")
    print(f"Checking: {yap_file}")
    if os.path.exists(yap_file):
        print("✅ yap_links.txt exists")
        try:
            with open(yap_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.strip().split('\n')
                print(f"📄 Contains {len(lines)} URLs:")
                for i, url in enumerate(lines[:5], 1):  # Show first 5 URLs
                    print(f"  {i}. {url}")
                if len(lines) > 5:
                    print(f"  ... and {len(lines) - 5} more URLs")
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    else:
        print("❌ yap_links.txt does not exist")
    print()
    
    # Check users_tweetlinks.txt
    users_file = os.path.join(project_dir, "users_tweetlinks.txt")
    print(f"Checking: {users_file}")
    if os.path.exists(users_file):
        print("✅ users_tweetlinks.txt exists")
        try:
            with open(users_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.strip().split('\n')
                print(f"📄 Contains {len(lines)} URLs:")
                for i, url in enumerate(lines[:5], 1):  # Show first 5 URLs
                    print(f"  {i}. {url}")
                if len(lines) > 5:
                    print(f"  ... and {len(lines) - 5} more URLs")
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    else:
        print("❌ users_tweetlinks.txt does not exist")
    print()
    
    # List all files in project directory
    print("All files in project directory:")
    for file in os.listdir(project_dir):
        if file.endswith('.txt'):
            file_path = os.path.join(project_dir, file)
            size = os.path.getsize(file_path)
            print(f"  📄 {file} ({size} bytes)")

if __name__ == "__main__":
    check_output_files() 