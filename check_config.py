#!/usr/bin/env python3
"""
Check current configuration settings
"""

import os
from config import print_config, validate_config

def main():
    """Display current configuration"""
    print("🔧 Twitter Monitor Configuration Checker")
    print("=" * 50)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found - using default values")
    
    print("\n📋 Current Settings:")
    print("-" * 30)
    
    # Print configuration
    print_config()
    
    print("\n🔍 Validation:")
    print("-" * 30)
    
    # Validate configuration
    if validate_config():
        print("✅ Configuration is valid!")
    else:
        print("❌ Configuration has issues - please check your .env file")
    
    print("\n💡 Tips:")
    print("- Edit .env file to change settings")
    print("- Run 'python setup_env.py' to create .env file")
    print("- All settings can be configured via .env file")

if __name__ == "__main__":
    main() 