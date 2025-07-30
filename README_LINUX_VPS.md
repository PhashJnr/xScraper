# X User Tweet Monitor - Linux VPS Deployment Guide

A comprehensive guide for deploying the Twitter/X monitoring application on Linux VPS with individual Chrome profiles.

## 🚀 Features

- **Individual Chrome Profiles**: Separate profiles for user monitoring and YAP scraping
- **Simultaneous Operation**: Both services can run at the same time without conflicts
- **VPS Optimized**: Headless operation with background processes
- **Telegram Integration**: Send notifications and files directly to Telegram
- **24/7 Operation**: Designed for continuous VPS operation

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

### Step 4: Install ChromeDriver

```bash
# Get Chrome version
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1)

# Download matching ChromeDriver
wget -O chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip"

# Extract and install
unzip chromedriver.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# Clean up
rm -rf chromedriver.zip chromedriver-linux64

# Verify installation
chromedriver --version
google-chrome --version
```

### Step 5: Clone Repository

```bash
git clone https://github.com/yourusername/xUserTweetMonitor.git
cd xUserTweetMonitor
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

### Step 4: Clear Login Data (if needed)

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
```

#### Method 2: Using screen

```bash
# Install screen if not available
sudo apt install -y screen

# Start user monitoring in screen session
screen -dmS user_monitor python3 main_scraper_locked_pc.py

# Start YAP scraping in screen session
screen -dmS yap_scraper python3 main_yap_scraper.py

# List screen sessions
screen -ls

# Attach to a session (optional)
screen -r user_monitor
```

#### Method 3: Using tmux

```bash
# Install tmux if not available
sudo apt install -y tmux

# Create new tmux session
tmux new-session -d -s monitor

# Split window and run both services
tmux split-window -h
tmux send-keys -t 0 "python3 main_scraper_locked_pc.py" Enter
tmux send-keys -t 1 "python3 main_yap_scraper.py" Enter

# Attach to session (optional)
tmux attach-session -t monitor
```

### Testing Configuration

```bash
# Test configuration
python3 check_config.py

# Test dual services
python3 test_windows_dual_services.py
```

## 📊 Features in Detail

### 🔍 YAP Search Scraping

- **Individual Chrome Profile**: Uses `chrome_profile_yap` directory
- **Headless Operation**: Optimized for VPS without display
- **Smart Scrolling**: Up to 15 scroll iterations with intelligent stopping
- **Configurable Search**: All search parameters customizable via `.env`
- **File Output**: Saves URLs to `yap_links.txt`
- **Telegram Integration**: Automatically sends file to Telegram
- **Deduplication**: Avoids duplicate URLs automatically

### 👥 User Tweet Monitoring

- **Individual Chrome Profile**: Uses `chrome_profile_user` directory
- **Real-time Monitoring**: Checks for new tweets every interval
- **Telegram Notifications**: Sends formatted notifications for each tweet
- **Media Support**: Handles tweets with images/videos
- **URL Extraction**: Saves tweet URLs to `users_tweetlinks.txt`
- **Sequential Processing**: Processes users one by one

### 🔧 Technical Features

- **Individual Chrome Profiles**: Separate profiles prevent conflicts
- **Selective Process Killing**: Only kills processes using specific profiles
- **VPS Optimized**: Headless operation with minimal resource usage
- **Robust Error Handling**: Retry logic, exponential backoff, rate limiting
- **Background Operation**: Designed for 24/7 VPS operation
- **Log Management**: Comprehensive logging for monitoring

## 🛠️ Utility Scripts

### Profile Management

- `setup_individual_profiles.py`: Create individual Chrome profiles
- `setup_twitter_login_user.py`: Login to user monitoring profile
- `setup_twitter_login_yap.py`: Login to YAP scraping profile
- `clear_twitter_login.py`: Clear login data from profiles
- `cleanup_old_profiles.py`: Clean up old Chrome profiles

### Configuration & Setup

- `setup_env.py`: Interactive environment setup
- `check_config.py`: Display current configuration
- `check_yap_config.py`: Validate YAP search settings

### Testing & Debugging

- `test_windows_dual_services.py`: Test dual services
- `test_telegram_file.py`: Test Telegram file sending
- `test_simplified_yap.py`: Test YAP scraper functionality
- `test_url_extraction.py`: Test URL extraction logic

### Process Management

- `stop_monitor.py`: Graceful process termination
- `force_stop_monitor.py`: Force process termination
- `check_files.py`: Check output files

## 📁 Output Files

- `yap_links.txt`: YAP search tweet URLs
- `users_tweetlinks.txt`: User monitoring tweet URLs
- `seen_tweets_scraper.json`: Tracked tweet IDs for user monitoring
- `tweet_monitor.log`: Application logs
- `chrome_profile_user/`: User monitoring Chrome profile
- `chrome_profile_yap/`: YAP scraping Chrome profile

## 🔧 Troubleshooting

### Common Issues

#### Chrome Profile Conflicts

```bash
# Clear all Chrome processes
sudo pkill chrome
sudo pkill chromedriver

# Clean up old profiles
python3 cleanup_old_profiles.py

# Setup individual profiles
python3 setup_individual_profiles.py
```

#### Login Issues

```bash
# Clear login data
python3 clear_twitter_login.py

# Re-login to both profiles
python3 setup_twitter_login_user.py
python3 setup_twitter_login_yap.py
```

#### Services Not Running Simultaneously

```bash
# Test dual services
python3 test_windows_dual_services.py

# Check if profiles are separate
ls -la chrome_profile_*
```

#### ChromeDriver Version Mismatch

```bash
# Remove old ChromeDriver
sudo rm /usr/local/bin/chromedriver

# Get current Chrome version
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1)

# Download matching ChromeDriver
wget -O chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip"
unzip chromedriver.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm -rf chromedriver.zip chromedriver-linux64
```

#### Telegram Notifications Not Working

1. Verify bot token and chat ID in `.env`
2. Start a conversation with your bot
3. Run `python3 test_telegram_file.py` to test connection

### Process Management

```bash
# Stop gracefully
python3 stop_monitor.py

# Force stop if needed
python3 force_stop_monitor.py

# Check running processes
ps aux | grep python

# Kill specific processes
sudo pkill -f main_scraper_locked_pc.py
sudo pkill -f main_yap_scraper.py
```

## 🚀 Advanced VPS Setup

### Systemd Service Setup

Create service files for automatic startup:

```bash
# Create user monitoring service
sudo nano /etc/systemd/system/tweet-monitor-user.service
```

Add content:

```ini
[Unit]
Description=Twitter User Monitor
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/xUserTweetMonitor
ExecStart=/usr/bin/python3 main_scraper_locked_pc.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Create YAP scraping service
sudo nano /etc/systemd/system/tweet-monitor-yap.service
```

Add content:

```ini
[Unit]
Description=Twitter YAP Scraper
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/xUserTweetMonitor
ExecStart=/usr/bin/python3 main_yap_scraper.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start services:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable tweet-monitor-user.service
sudo systemctl enable tweet-monitor-yap.service

# Start services
sudo systemctl start tweet-monitor-user.service
sudo systemctl start tweet-monitor-yap.service

# Check status
sudo systemctl status tweet-monitor-user.service
sudo systemctl status tweet-monitor-yap.service
```

### Log Management

```bash
# View logs in real-time
tail -f tweet_monitor.log

# View service logs
sudo journalctl -u tweet-monitor-user.service -f
sudo journalctl -u tweet-monitor-yap.service -f

# Rotate logs
sudo logrotate /etc/logrotate.d/tweet-monitor
```

### Resource Monitoring

```bash
# Monitor CPU and memory usage
htop

# Monitor disk usage
df -h

# Monitor network usage
iftop
```

## 📋 Quick Start Checklist

- [ ] Update system packages
- [ ] Install Python 3.8+
- [ ] Install Git
- [ ] Install Google Chrome
- [ ] Install ChromeDriver
- [ ] Clone repository
- [ ] Install Python dependencies
- [ ] Create and configure `.env` file
- [ ] Setup individual Chrome profiles
- [ ] Login to Twitter for both profiles
- [ ] Test configuration
- [ ] Run services in background
- [ ] Setup systemd services (optional)

## 🎯 Performance Tips

### For Better Performance

1. **Adequate Resources**: Ensure at least 2GB RAM and 2 CPU cores
2. **SSD Storage**: Use SSD for faster file operations
3. **Stable Network**: Use reliable internet connection
4. **Regular Cleanup**: Clear old profiles and logs periodically
5. **Resource Monitoring**: Monitor CPU, memory, and disk usage

### For 24/7 Operation

1. **Automatic Restart**: Use systemd services for automatic restart
2. **Log Rotation**: Implement log rotation to prevent disk space issues
3. **Monitoring**: Set up monitoring for service health
4. **Backup**: Regular backup of configuration and data files
5. **Security**: Keep system updated and secure

## 📞 Support

For VPS-specific issues:

1. Check the troubleshooting section
2. Review the logs in `tweet_monitor.log`
3. Test individual components with test scripts
4. Create an issue with detailed error information
5. Include VPS provider, OS version, and Python version in reports

## 📝 License

This project is for educational and personal use. Please respect Twitter's terms of service.
