# X User Tweet Monitor - Windows Deployment Guide

A comprehensive guide for deploying the Twitter/X monitoring application on Windows with individual Chrome profiles.

## 🚀 Features

- **Individual Chrome Profiles**: Separate profiles for user monitoring and YAP scraping
- **Simultaneous Operation**: Both services can run at the same time without conflicts
- **Windows Optimized**: Selective process management for Windows compatibility
- **Telegram Integration**: Send notifications and files directly to Telegram
- **Background Operation**: Optimized for running when PC is locked

## 📋 Prerequisites

### System Requirements

- Windows 10/11
- Python 3.8 or higher
- Google Chrome browser
- Git for Windows

### Required Accounts

- Twitter account (for login)
- Telegram bot token and chat ID

## 🛠️ Installation

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Install with "Add Python to PATH" checked
3. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

### Step 2: Install Git

1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Install with default settings
3. Verify installation:
   ```cmd
   git --version
   ```

### Step 3: Install Chrome

1. Download Chrome from [google.com/chrome](https://www.google.com/chrome/)
2. Install with default settings

### Step 4: Install ChromeDriver

1. Check your Chrome version:

   - Open Chrome
   - Go to `chrome://version/`
   - Note the version number (e.g., 138.0.7204.183)

2. Download ChromeDriver:

   - Go to [chromedriver.chromium.org](https://chromedriver.chromium.org/)
   - Download the version matching your Chrome version
   - Extract the `chromedriver.exe` file

3. Add ChromeDriver to PATH:
   - Create folder: `C:\chromedriver`
   - Copy `chromedriver.exe` to `C:\chromedriver`
   - Add `C:\chromedriver` to your system PATH

### Step 5: Clone Repository

```cmd
git clone https://github.com/yourusername/xUserTweetMonitor.git
cd xUserTweetMonitor
```

### Step 6: Install Python Dependencies

```cmd
pip install -r requirements.txt
```

## ⚙️ Configuration

### Step 1: Create Environment File

```cmd
copy env_example.txt .env
```

### Step 2: Edit Environment File

Open `.env` in Notepad or your preferred editor:

```cmd
notepad .env
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

```cmd
python cleanup_old_profiles.py
```

### Step 2: Setup Individual Profiles

```cmd
python setup_individual_profiles.py
```

### Step 3: Login to Twitter for Both Profiles

```cmd
# Login to Twitter for user monitoring profile
python setup_twitter_login_user.py

# Login to Twitter for YAP scraping profile
python setup_twitter_login_yap.py
```

### Step 4: Clear Login Data (if needed)

```cmd
python clear_twitter_login.py
```

## 🚀 Usage

### Running Services Separately

#### User Tweet Monitoring

```cmd
# Start user monitoring service
python main_scraper_locked_pc.py
```

#### YAP Search Scraping

```cmd
# Start YAP scraping service
python main_yap_scraper.py
```

### Running Both Services Simultaneously

#### Method 1: Separate Command Prompts

1. **Open First Command Prompt:**

   ```cmd
   cd C:\path\to\xUserTweetMonitor
   python main_scraper_locked_pc.py
   ```

2. **Open Second Command Prompt:**
   ```cmd
   cd C:\path\to\xUserTweetMonitor
   python main_yap_scraper.py
   ```

#### Method 2: PowerShell Windows

1. **Open First PowerShell Window:**

   ```powershell
   cd C:\path\to\xUserTweetMonitor
   python main_scraper_locked_pc.py
   ```

2. **Open Second PowerShell Window:**
   ```powershell
   cd C:\path\to\xUserTweetMonitor
   python main_yap_scraper.py
   ```

### Testing Dual Services

```cmd
# Test both services on Windows
python test_windows_dual_services.py
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
- **Windows Compatibility**: Optimized for Windows dual-service operation
- **Robust Error Handling**: Retry logic, exponential backoff, rate limiting
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

```cmd
# Clear all Chrome processes
taskkill /f /im chrome.exe
taskkill /f /im chromedriver.exe

# Clean up old profiles
python cleanup_old_profiles.py

# Setup individual profiles
python setup_individual_profiles.py
```

#### Login Issues

```cmd
# Clear login data
python clear_twitter_login.py

# Re-login to both profiles
python setup_twitter_login_user.py
python setup_twitter_login_yap.py
```

#### Services Not Running Simultaneously

```cmd
# Test dual services
python test_windows_dual_services.py

# Check if profiles are separate
dir chrome_profile_*
```

#### ChromeDriver Not Found

1. Verify ChromeDriver is in PATH:

   ```cmd
   chromedriver --version
   ```

2. If not found, add to PATH manually:
   - Copy `chromedriver.exe` to `C:\chromedriver`
   - Add `C:\chromedriver` to system PATH
   - Restart Command Prompt

#### Telegram Notifications Not Working

1. Verify bot token and chat ID in `.env`
2. Start a conversation with your bot
3. Run `python test_telegram_file.py` to test connection

### Process Management

```cmd
# Stop gracefully
python stop_monitor.py

# Force stop if needed
python force_stop_monitor.py

# Check running processes
tasklist | findstr python
```

## 📋 Quick Start Checklist

- [ ] Install Python 3.8+
- [ ] Install Git for Windows
- [ ] Install Google Chrome
- [ ] Install ChromeDriver and add to PATH
- [ ] Clone repository
- [ ] Install Python dependencies
- [ ] Create and configure `.env` file
- [ ] Setup individual Chrome profiles
- [ ] Login to Twitter for both profiles
- [ ] Test configuration
- [ ] Run services

## 🎯 Performance Tips

### For Better Performance

1. **Close Unnecessary Programs**: Close other Chrome instances
2. **Use SSD**: Install on SSD for faster file operations
3. **Adequate RAM**: Ensure at least 4GB free RAM
4. **Stable Internet**: Use wired connection if possible
5. **Regular Cleanup**: Clear old profiles periodically

### For Background Operation

1. **Power Settings**: Disable sleep mode
2. **Screen Saver**: Disable screen saver
3. **Windows Updates**: Schedule updates during off-hours
4. **Antivirus**: Add project folder to exclusions

## 📞 Support

For Windows-specific issues:

1. Check the troubleshooting section
2. Review the logs in `tweet_monitor.log`
3. Test individual components with test scripts
4. Create an issue with detailed error information
5. Include Windows version and Python version in reports

## 📝 License

This project is for educational and personal use. Please respect Twitter's terms of service.
