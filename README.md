# X User Tweet Monitor

A comprehensive Python application for monitoring Twitter/X users and scraping tweet URLs with Telegram notifications. Features individual Chrome profiles for simultaneous operation.

## 🚀 Features

### 📊 Dual Monitoring Modes

- **User Tweet Monitoring**: Monitor specific users for new tweets with Telegram notifications
- **YAP Search Scraping**: Scrape tweet URLs from custom search queries and send as file to Telegram

### 🔧 Enhanced Features

- **Individual Chrome Profiles**: Separate profiles for user monitoring and YAP scraping
- **Simultaneous Operation**: Both services can run at the same time without conflicts
- **Smart Scrolling**: Intelligent multi-scroll approach to get more tweets
- **Telegram Integration**: Send notifications and files directly to Telegram
- **Configurable Search**: Customize YAP search parameters via `.env` file
- **Robust Error Handling**: Retry logic, rate limiting, and graceful failures
- **Background Operation**: Optimized for running when PC is locked

## 📁 Project Structure

```
xUserTweetMonitor/
├── main_scraper_locked_pc.py    # User monitoring service
├── main_yap_scraper.py          # YAP scraping service
├── scraper_monitor.py           # Core user monitoring logic
├── yap_scraper.py              # Core YAP scraping logic
├── robust_notifier.py           # Telegram notification system
├── config.py                    # Configuration management
├── setup_individual_profiles.py # Setup individual Chrome profiles
├── setup_twitter_login_user.py  # Login to user monitoring profile
├── setup_twitter_login_yap.py   # Login to YAP scraping profile
├── clear_twitter_login.py       # Clear login data from profiles
├── cleanup_old_profiles.py      # Clean up old Chrome profiles
├── test_windows_dual_services.py # Test dual services on Windows
├── requirements.txt             # Python dependencies
├── .env                         # Environment configuration
├── env_example.txt              # Environment template
├── README.md                    # This file
└── .gitignore                  # Git ignore rules
```

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/xUserTweetMonitor.git
cd xUserTweetMonitor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Chrome Driver

#### Windows:

```bash
# Download ChromeDriver from https://chromedriver.chromium.org/
# Extract and add to PATH, or place in project directory
```

#### Linux/VPS:

```bash
# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb

# Install ChromeDriver (auto-matching version)
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1)
wget -O chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip"
unzip chromedriver.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
rm -rf chromedriver.zip chromedriver-linux64
```

### 4. Set Up Environment

```bash
# Copy example environment file
cp env_example.txt .env

# Edit .env with your settings
notepad .env  # Windows
# or
nano .env     # Linux/Mac
```

## ⚙️ Configuration

### Required Settings in `.env`:

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

### YAP Search Parameters

The YAP scraper supports extensive customization:

| Parameter             | Description            | Example                   |
| --------------------- | ---------------------- | ------------------------- |
| `YAP_SEARCH_KEYWORDS` | Main search terms      | `("cysic" OR @cysic_xyz)` |
| `YAP_FILTER_VERIFIED` | Only verified accounts | `true`                    |
| `YAP_MIN_REPLIES`     | Minimum reply count    | `20`                      |
| `YAP_LANGUAGE`        | Language filter        | `en`                      |
| `YAP_TIME_WINDOW`     | Time window (minutes)  | `1440`                    |

## 🔐 Setup Individual Chrome Profiles

### Step 1: Clean Up Old Profiles (if needed)

```bash
# Clean up old Chrome profiles and processes
python3 cleanup_old_profiles.py
```

### Step 2: Setup Individual Profiles

```bash
# Create individual Chrome profiles for both services
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
# Clear login data from both profiles
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

### Running Both Services Simultaneously

#### Windows (Separate Terminals)

```bash
# Terminal 1 - User Monitoring
python3 main_scraper_locked_pc.py

# Terminal 2 - YAP Scraping
python3 main_yap_scraper.py
```

#### Linux/VPS (Background)

```bash
# Start user monitoring in background
nohup python3 main_scraper_locked_pc.py > user_monitor.log 2>&1 &

# Start YAP scraping in background
nohup python3 main_yap_scraper.py > yap_scraper.log 2>&1 &
```

### Testing Dual Services

```bash
# Test both services on Windows
python3 test_windows_dual_services.py
```

## 📊 Features in Detail

### 🔍 YAP Search Scraping

- **Individual Chrome Profile**: Uses `chrome_profile_yap` directory
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
- **Robust Error Handling**: Retry logic, exponential backoff, rate limiting
- **Process Management**: Graceful shutdown and force termination options
- **Background Operation**: Optimized for running when PC is locked
- **Live Countdown**: Real-time countdown timer in terminal

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

- `test_windows_dual_services.py`: Test dual services on Windows
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

#### Telegram Notifications Not Working

1. Verify bot token and chat ID in `.env`
2. Start a conversation with your bot
3. Run `test_telegram_file.py` to test connection

### Process Management

```bash
# Stop gracefully
python3 stop_monitor.py

# Force stop if needed
python3 force_stop_monitor.py

# Check running processes
ps aux | grep python
```

## 🚀 VPS Deployment

### Complete VPS Setup

```bash
# 1. Install system dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip git wget unzip

# 2. Install Chrome and ChromeDriver
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb

CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1)
wget -O chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip"
unzip chromedriver.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

# 3. Clone repository
git clone https://github.com/yourusername/xUserTweetMonitor.git
cd xUserTweetMonitor

# 4. Install Python dependencies
pip3 install -r requirements.txt

# 5. Setup environment
cp env_example.txt .env
nano .env  # Edit with your settings

# 6. Setup individual profiles
python3 setup_individual_profiles.py

# 7. Login to both profiles
python3 setup_twitter_login_user.py
python3 setup_twitter_login_yap.py

# 8. Test configuration
python3 check_config.py

# 9. Run services in background
nohup python3 main_scraper_locked_pc.py > user_monitor.log 2>&1 &
nohup python3 main_yap_scraper.py > yap_scraper.log 2>&1 &
```

## 🔄 Recent Updates

### Latest Features (v3.0)

- ✅ **Individual Chrome Profiles**: Separate profiles for user monitoring and YAP scraping
- ✅ **Simultaneous Operation**: Both services can run at the same time without conflicts
- ✅ **Selective Process Management**: Only kills processes using specific profiles
- ✅ **Windows Compatibility**: Optimized for Windows dual-service operation
- ✅ **Separate Login Scripts**: Individual login processes for each profile
- ✅ **Profile Management Tools**: Setup, cleanup, and clear login data scripts

### Previous Features (v2.0)

- ✅ **YAP Search Scraping**: Custom search query scraping with file output
- ✅ **Telegram File Sending**: Automatic file delivery to Telegram
- ✅ **Smart Multi-Scroll**: Intelligent scrolling to get more tweets
- ✅ **Configurable Search**: All search parameters via `.env`
- ✅ **Enhanced Error Handling**: Robust retry logic and rate limiting
- ✅ **Background Operation**: Optimized for locked PC operation

## 📝 License

This project is for educational and personal use. Please respect Twitter's terms of service.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review the logs in `tweet_monitor.log`
3. Test individual components with test scripts
4. Create an issue with detailed error information
