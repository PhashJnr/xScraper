# X User Tweet Monitor

A comprehensive Python application for monitoring Twitter/X users and scraping tweet URLs with Telegram notifications.

## 🚀 Features

### 📊 Dual Monitoring Modes

- **User Tweet Monitoring**: Monitor specific users for new tweets with Telegram notifications
- **YAP Search Scraping**: Scrape tweet URLs from custom search queries and send as file to Telegram

### 🔧 Enhanced Features

- **Smart Scrolling**: Intelligent multi-scroll approach to get more tweets
- **Telegram Integration**: Send notifications and files directly to Telegram
- **Configurable Search**: Customize YAP search parameters via `.env` file
- **Robust Error Handling**: Retry logic, rate limiting, and graceful failures
- **Background Operation**: Optimized for running when PC is locked

## 📁 Project Structure

```
xUserTweetMonitor/
├── main_menu.py              # Main menu system
├── main_scraper.py           # User tweet monitoring
├── yap_scraper.py            # YAP search scraping
├── scraper_monitor.py        # Core scraping logic
├── robust_notifier.py        # Telegram notification system
├── config.py                 # Configuration management
├── countdown_timer.py        # Live countdown utility
├── stop_monitor.py           # Graceful process termination
├── force_stop_monitor.py     # Force process termination
├── requirements.txt          # Python dependencies
├── .env                      # Environment configuration
├── env_example.txt           # Environment template
├── README.md                 # This file
└── .gitignore               # Git ignore rules
```

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd xUserTweetMonitor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Chrome Driver

Download ChromeDriver from [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/) and add to your PATH.

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

# Monitoring Settings
CHECK_INTERVAL_MINUTES=5
MAX_TWEETS_TO_SCRAPE=50

# Users to Monitor (comma-separated)
USERS_TO_MONITOR=username1,username2,username3

# YAP Search Configuration
YAP_SEARCH_KEYWORDS=("cysic" OR @cysic_xyz)
YAP_FILTER_VERIFIED=true
YAP_MIN_REPLIES=20
YAP_LANGUAGE=en
YAP_TIME_WINDOW=1440
YAP_SEARCH_SOURCE=recent_search_click

# Logging
LOG_LEVEL=INFO
LOG_FILE=monitor.log
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

## 🚀 Usage

### Main Menu System

```bash
python main_menu.py
```

Choose between:

1. **YAP Link Scraping**: Scrape tweet URLs from search queries
2. **User Tweet Monitoring**: Monitor specific users for new tweets

### Direct Usage

#### YAP Search Scraping

```bash
python yap_scraper.py
```

#### User Tweet Monitoring

```bash
python main_scraper.py
```

### Background Operation

```bash
# Windows (PowerShell)
.\run_monitor_background.ps1

# Windows (Batch)
run_monitor_background.bat

# Linux/Mac
nohup python main_scraper_locked_pc.py &
```

## 📊 Features in Detail

### 🔍 YAP Search Scraping

- **Smart Scrolling**: Up to 15 scroll iterations with intelligent stopping
- **Configurable Search**: All search parameters customizable via `.env`
- **File Output**: Saves URLs to `yap_links.txt`
- **Telegram Integration**: Automatically sends file to Telegram
- **Deduplication**: Avoids duplicate URLs automatically

### 👥 User Tweet Monitoring

- **Real-time Monitoring**: Checks for new tweets every interval
- **Telegram Notifications**: Sends formatted notifications for each tweet
- **Media Support**: Handles tweets with images/videos
- **URL Extraction**: Saves tweet URLs to `users_tweetlinks.txt`
- **Sequential Processing**: Processes users one by one with single Chrome profile

### 🔧 Technical Features

- **Robust Error Handling**: Retry logic, exponential backoff, rate limiting
- **Process Management**: Graceful shutdown and force termination options
- **Chrome Profile**: Dedicated browser profile for persistent login
- **Background Operation**: Optimized for running when PC is locked
- **Live Countdown**: Real-time countdown timer in terminal

## 🛠️ Utility Scripts

### Configuration & Setup

- `setup_env.py`: Interactive environment setup
- `check_config.py`: Display current configuration
- `check_yap_config.py`: Validate YAP search settings

### Testing & Debugging

- `test_telegram_file.py`: Test Telegram file sending
- `test_simplified_yap.py`: Test YAP scraper functionality
- `test_url_extraction.py`: Test URL extraction logic
- `test_telegram_fix.py`: Test Telegram notifications

### Process Management

- `stop_monitor.py`: Graceful process termination
- `force_stop_monitor.py`: Force process termination
- `check_files.py`: Check output files

## 📁 Output Files

- `yap_links.txt`: YAP search tweet URLs
- `users_tweetlinks.txt`: User monitoring tweet URLs
- `seen_tweets.json`: Tracked tweet IDs for user monitoring
- `monitor.log`: Application logs

## 🔧 Troubleshooting

### Common Issues

#### Telegram Notifications Not Working

1. Verify bot token and chat ID in `.env`
2. Start a conversation with your bot
3. Run `test_telegram_fix.py` to test connection

#### Chrome Profile Issues

1. Delete `chrome_profile/` directory
2. Restart the application
3. Login to Twitter in the new browser window

#### Not Finding Enough Tweets

1. Increase `MAX_TWEETS_TO_SCRAPE` in `.env`
2. Adjust YAP search parameters
3. Check if search query is too restrictive

### Process Management

```bash
# Stop gracefully
python stop_monitor.py

# Force stop if needed
python force_stop_monitor.py
```

## 🔄 Recent Updates

### Latest Features (v2.0)

- ✅ **YAP Search Scraping**: Custom search query scraping with file output
- ✅ **Telegram File Sending**: Automatic file delivery to Telegram
- ✅ **Smart Multi-Scroll**: Intelligent scrolling to get more tweets
- ✅ **Configurable Search**: All search parameters via `.env`
- ✅ **Enhanced Error Handling**: Robust retry logic and rate limiting
- ✅ **Background Operation**: Optimized for locked PC operation
- ✅ **Menu System**: Easy selection between monitoring modes

### Previous Features

- ✅ User tweet monitoring with Telegram notifications
- ✅ Selenium-based scraping (no API limits)
- ✅ Persistent Chrome profile for login
- ✅ Sequential user processing
- ✅ Media tweet support
- ✅ URL extraction and saving

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
2. Review the logs in `monitor.log`
3. Test individual components with test scripts
4. Create an issue with detailed error information
