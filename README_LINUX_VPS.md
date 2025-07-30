# X User Tweet Monitor - Linux VPS Deployment Guide

A comprehensive guide for deploying the Twitter/X monitoring application on Linux VPS with individual Chrome profiles.

## 🚀 Features

- **Individual Chrome Profiles**: Separate profiles for user monitoring and YAP scraping
- **Simultaneous Operation**: Both services can run at the same time without conflicts
- **VPS Optimized**: Headless operation with background processes
- **Telegram Integration**: Send notifications and files directly to Telegram
- **24/7 Operation**: Designed for continuous VPS operation
- **Profile Persistence**: Improved Chrome profile management to prevent logout issues

## ⚡ Quick Reference

### Chrome 138+ Installation

```bash
# For Chrome 138 or newer, use Chrome-for-Testing
LATEST_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json | grep -o '"version":"[^"]*"' | head -1 | cut -d'"' -f4)
wget -O chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/$LATEST_VERSION/linux64/chromedriver-linux64.zip"
unzip chromedriver.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm -rf chromedriver.zip chromedriver-linux64
```

### Quick Setup Commands

```bash
cd xUserTweetMonitor/linux
pip3 install -r requirements.txt
cp env_example.txt .env
nano .env
python3 setup_individual_profiles.py
python3 setup_twitter_login_user.py
python3 setup_twitter_login_yap.py
```

### Service Management

```bash
# Start services
sudo systemctl start tweet-monitor-user.service
sudo systemctl start tweet-monitor-yap.service

# Check status
sudo systemctl status tweet-monitor-user.service
sudo systemctl status tweet-monitor-yap.service

# View logs
sudo journalctl -u tweet-monitor-user.service -f
```

## 📋 Prerequisites

### System Requirements

- Ubuntu 20.04+ or Debian 11+
- Python 3.8 or higher
- At least 2GB RAM
- At least 10GB free disk space
- Root or sudo access

### Required Accounts

- Twitter account (for login)
- Telegram bot token and chat ID

## 🛠️ Installation

### Step 1: Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install System Dependencies

```bash
sudo apt install -y python3 python3-pip git wget unzip curl
```

### Step 3: Install Google Chrome

```bash
# Download and install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb

# Clean up
rm google-chrome-stable_current_amd64.deb
```

### Step 4: Install ChromeDriver (Updated Method)

**Method 1: Chrome-for-Testing (Recommended for Chrome 138+)**

```bash
# Remove old ChromeDriver if exists
sudo rm -f /usr/local/bin/chromedriver

# Get latest Chrome-for-Testing version
LATEST_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json | grep -o '"version":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "Latest Chrome-for-Testing version: $LATEST_VERSION"

# Download and install
wget -O chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/$LATEST_VERSION/linux64/chromedriver-linux64.zip"
unzip chromedriver.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# Clean up
rm -rf chromedriver.zip chromedriver-linux64

# Verify installation
chromedriver --version
google-chrome --version

# Test ChromeDriver functionality
chromedriver --help
```

**💡 Suggestion**: After extracting ChromeDriver, you'll see files like `chromedriver-linux64/chromedriver`. Make sure to move the `chromedriver` file (not the folder) to `/usr/local/bin/`. The versions don't need to match exactly - ChromeDriver is often compatible with Chrome versions that are close.

**Method 2: Latest Stable ChromeDriver (Alternative)**

```bash
# Remove old ChromeDriver if exists
sudo rm -f /usr/local/bin/chromedriver

# Get latest stable version
LATEST_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
echo "Latest ChromeDriver version: $LATEST_VERSION"

# Download and install
wget -O chromedriver.zip "https://chromedriver.storage.googleapis.com/$LATEST_VERSION/chromedriver_linux64.zip"
unzip chromedriver.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# Clean up
rm chromedriver.zip

# Verify installation
chromedriver --version
google-chrome --version

# Test ChromeDriver functionality
chromedriver --help
```

**Method 3: Manual Version Selection (For Chrome 138+)**

If the above methods don't work with Chrome 138, try these known working versions:

```bash
# Remove old ChromeDriver
sudo rm -f /usr/local/bin/chromedriver

# Try version 120 (known to work with Chrome 138)
wget -O chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/120.0.6099.109/linux64/chromedriver-linux64.zip"

# Or try version 119
# wget -O chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/119.0.6045.105/linux64/chromedriver-linux64.zip"

# Extract and install
unzip chromedriver.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# Clean up
rm -rf chromedriver.zip chromedriver-linux64

# Verify installation
chromedriver --version
google-chrome --version

# Test ChromeDriver functionality
chromedriver --help
```

### Step 5: Clone Repository

```bash
git clone https://github.com/yourusername/xUserTweetMonitor.git
cd xUserTweetMonitor/linux
```

### Step 6: Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

## ⚙️ Configuration

### Step 1: Create Environment File

```bash
cp env_example.txt .env
```

### Step 2: Edit Environment File

```bash
nano .env
```

### Step 3: Configure Settings

Add your settings to `.env`:

```bash
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Twitter Login Credentials
TWITTER_USERNAME=your_twitter_username
TWITTER_PASSWORD=your_twitter_password

# Monitoring Settings
CHECK_INTERVAL_MINUTES=15
YAP_CHECK_INTERVAL_MINUTES=1080
MAX_TWEETS_TO_SCRAPE=50

# Users to Monitor (comma-separated)
USERS_TO_MONITOR=username1,username2,username3

# YAP Search Configuration
YAP_SEARCH_KEYWORDS=("cysic" OR @cysic_xyz)
YAP_FILTER_VERIFIED=true
YAP_MIN_REPLIES=20
YAP_LANGUAGE=en
YAP_TIME_WINDOW=1440

# Logging
LOG_LEVEL=INFO
LOG_FILE=tweet_monitor.log
```

## 🔐 Setup Individual Chrome Profiles

### Step 1: Clean Up Old Profiles (if needed)

```bash
python3 cleanup_old_profiles.py
```

### Step 2: Setup Individual Profiles

```bash
python3 setup_individual_profiles.py
```

### Step 3: Login to Twitter for Both Profiles

```bash
# Login to Twitter for user monitoring profile
python3 setup_twitter_login_user.py

# Login to Twitter for YAP scraping profile
python3 setup_twitter_login_yap.py
```

### Step 4: Improve Profile Persistence (NEW)

If you experience logout issues with the YAP profile:

```bash
# Improve profile persistence to prevent logout issues
python3 improve_profile_persistence.py
```

Choose option 1 to improve the YAP profile specifically.

### Step 5: Clear Login Data (if needed)

```bash
python3 clear_twitter_login.py
```

## 🚀 Usage

### Running Services Separately

#### User Tweet Monitoring

```bash
# Start user monitoring service
python3 main_scraper_locked_pc.py
```

#### YAP Search Scraping

```bash
# Start YAP scraping service
python3 main_yap_scraper.py
```

### Running Both Services in Background

#### Method 1: Using nohup

```bash
# Start user monitoring in background
nohup python3 main_scraper_locked_pc.py > user_monitor.log 2>&1 &

# Start YAP scraping in background
nohup python3 main_yap_scraper.py > yap_scraper.log 2>&1 &

# Check if services are running
ps aux | grep python

# View logs
tail -f user_monitor.log
tail -f yap_scraper.log
```

#### Method 2: Using screen

```bash
# Install screen if not installed
sudo apt install screen

# Start user monitoring in screen session
screen -S user_monitor
python3 main_scraper_locked_pc.py
# Press Ctrl+A, then D to detach

# Start YAP scraping in screen session
screen -S yap_scraper
python3 main_yap_scraper.py
# Press Ctrl+A, then D to detach

# List screen sessions
screen -ls

# Reattach to sessions
screen -r user_monitor
screen -r yap_scraper
```

#### Method 3: Using systemd Services (Recommended for Production)

```bash
# Copy service files
sudo cp tweet-monitor-user.service /etc/systemd/system/
sudo cp tweet-monitor-yap.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable services to start on boot
sudo systemctl enable tweet-monitor-user.service
sudo systemctl enable tweet-monitor-yap.service

# Start services
sudo systemctl start tweet-monitor-user.service
sudo systemctl start tweet-monitor-yap.service

# Check service status
sudo systemctl status tweet-monitor-user.service
sudo systemctl status tweet-monitor-yap.service

# View logs
sudo journalctl -u tweet-monitor-user.service -f
sudo journalctl -u tweet-monitor-yap.service -f
```

## 🔧 Troubleshooting

### ChromeDriver Version Issues

If you get ChromeDriver version mismatch errors:

```bash
# Check Chrome version
google-chrome --version

# Check ChromeDriver version
chromedriver --version

# If versions don't match, reinstall ChromeDriver using Method 1 above
```

### Chrome 138+ Compatibility Issues

If you have Chrome 138 or newer and encounter compatibility issues:

```bash
# Check your Chrome version
google-chrome --version

# If Chrome is 138+, use Chrome-for-Testing method
LATEST_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json | grep -o '"version":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "Latest Chrome-for-Testing version: $LATEST_VERSION"

# Download and install
sudo rm -f /usr/local/bin/chromedriver
wget -O chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/$LATEST_VERSION/linux64/chromedriver-linux64.zip"
unzip chromedriver.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm -rf chromedriver.zip chromedriver-linux64

# Verify compatibility
chromedriver --version
google-chrome --version
```

**Note**: ChromeDriver versions don't need to match Chrome versions exactly. ChromeDriver is often compatible with Chrome versions that are close (e.g., ChromeDriver 120 can work with Chrome 138).

### Installation Verification

After installing ChromeDriver, verify it works:

```bash
# Check ChromeDriver version
chromedriver --version

# Check Chrome version
google-chrome --version

# Test ChromeDriver functionality
chromedriver --help
```

**💡 Tip**: If you see "chromedriver: command not found", make sure you moved the `chromedriver` file (not the folder) to `/usr/local/bin/` and made it executable with `chmod +x`.

### Profile Logout Issues

If the YAP profile keeps getting logged out:

```bash
# Run profile persistence improvement
python3 improve_profile_persistence.py

# Choose option 1 for YAP profile
# Then re-login if needed
python3 setup_twitter_login_yap.py
```

### Service Management

```bash
# Stop services
sudo systemctl stop tweet-monitor-user.service
sudo systemctl stop tweet-monitor-yap.service

# Restart services
sudo systemctl restart tweet-monitor-user.service
sudo systemctl restart tweet-monitor-yap.service

# Disable services
sudo systemctl disable tweet-monitor-user.service
sudo systemctl disable tweet-monitor-yap.service
```

### Log Management

```bash
# View real-time logs
tail -f tweet_monitor.log

# View systemd logs
sudo journalctl -u tweet-monitor-user.service -n 100
sudo journalctl -u tweet-monitor-yap.service -n 100

# Clear logs
sudo journalctl --vacuum-time=7d
```

## 📁 Directory Structure

```
xUserTweetMonitor/
├── linux/                          ← Linux-specific code
│   ├── chrome_profile_user/        ← User monitoring profile
│   ├── chrome_profile_yap/         ← YAP scraping profile
│   ├── main_scraper_locked_pc.py  ← User monitoring service
│   ├── main_yap_scraper.py        ← YAP scraping service
│   ├── scraper_monitor.py          ← Core user monitoring logic
│   ├── yap_scraper.py             ← Core YAP scraping logic
│   ├── robust_notifier.py          ← Telegram notification system
│   ├── config.py                   ← Configuration management
│   ├── setup_individual_profiles.py
│   ├── setup_twitter_login_user.py
│   ├── setup_twitter_login_yap.py
│   ├── improve_profile_persistence.py
│   ├── clear_twitter_login.py
│   ├── cleanup_old_profiles.py
│   ├── countdown_timer.py
│   ├── test_windows_dual_services.py
│   ├── requirements.txt
│   ├── env_example.txt
│   ├── tweet-monitor-user.service
│   ├── tweet-monitor-yap.service
│   ├── tweet_monitor.log
│   ├── yap_links.txt
│   ├── users_tweetlinks.txt
│   ├── seen_tweets_scraper.json
│   └── README.md
└── windows/                        ← Windows-specific code
```

## 🔄 Monitoring and Maintenance

### Check Service Status

```bash
# Check if services are running
ps aux | grep python

# Check systemd services
sudo systemctl status tweet-monitor-user.service
sudo systemctl status tweet-monitor-yap.service
```

### Update Application

```bash
# Pull latest changes
git pull origin main

# Restart services
sudo systemctl restart tweet-monitor-user.service
sudo systemctl restart tweet-monitor-yap.service
```

### Backup Profiles

```bash
# Backup Chrome profiles
cp -r chrome_profile_user chrome_profile_user_backup
cp -r chrome_profile_yap chrome_profile_yap_backup
```

## 📊 Performance Monitoring

### Resource Usage

```bash
# Monitor CPU and memory usage
htop

# Monitor disk usage
df -h

# Monitor log file sizes
du -sh *.log
```

### Log Analysis

```bash
# Count successful checks
grep "Check #" tweet_monitor.log | wc -l

# Count notifications sent
grep "Notification sent" tweet_monitor.log | wc -l

# Check for errors
grep "ERROR" tweet_monitor.log
```

## 🆘 Support

If you encounter issues:

1. Check the logs for error messages
2. Verify Chrome and ChromeDriver versions match
3. Run profile persistence improvement if experiencing logouts
4. Ensure all environment variables are set correctly
5. Verify Telegram bot token and chat ID are correct

## 📝 Notes

- The application creates separate Chrome profiles for each service
- Profiles are stored in the `linux/` directory
- Services can run simultaneously without conflicts
- Logs are written to `tweet_monitor.log`
- The application is optimized for 24/7 VPS operation
