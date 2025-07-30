# Linux VPS Deployment

This directory contains Linux VPS-specific scripts and configurations for the Twitter/X monitoring application.

## 📁 Directory Structure

```
linux/
├── README.md                    # This file
├── main_scraper_locked_pc.py   # User monitoring service
├── main_yap_scraper.py         # YAP scraping service
├── scraper_monitor.py          # Core user monitoring logic
├── yap_scraper.py             # Core YAP scraping logic
├── robust_notifier.py         # Telegram notification system
├── config.py                  # Configuration management
├── setup_individual_profiles.py # Setup individual Chrome profiles
├── setup_twitter_login_user.py # Login to user monitoring profile
├── setup_twitter_login_yap.py  # Login to YAP scraping profile
├── clear_twitter_login.py      # Clear login data from profiles
├── cleanup_old_profiles.py     # Clean up old Chrome profiles
├── requirements.txt            # Python dependencies
├── env_example.txt            # Environment template
├── tweet-monitor-user.service  # Systemd service for user monitoring
├── tweet-monitor-yap.service   # Systemd service for YAP scraping
└── .gitignore                # Git ignore rules
```

## 🚀 Quick Start

1. **Install Dependencies:**

   ```bash
   pip3 install -r requirements.txt
   ```

2. **Setup Environment:**

   ```bash
   cp env_example.txt .env
   nano .env
   ```

3. **Setup Individual Profiles:**

   ```bash
   python3 setup_individual_profiles.py
   ```

4. **Login to Twitter:**

   ```bash
   python3 setup_twitter_login_user.py
   python3 setup_twitter_login_yap.py
   ```

5. **Run Services (Background):**

   ```bash
   # Method 1: Using nohup
   nohup python3 main_scraper_locked_pc.py > user_monitor.log 2>&1 &
   nohup python3 main_yap_scraper.py > yap_scraper.log 2>&1 &

   # Method 2: Using systemd services
   sudo cp tweet-monitor-user.service /etc/systemd/system/
   sudo cp tweet-monitor-yap.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable tweet-monitor-user.service
   sudo systemctl enable tweet-monitor-yap.service
   sudo systemctl start tweet-monitor-user.service
   sudo systemctl start tweet-monitor-yap.service
   ```

## 📖 Full Documentation

For complete Linux VPS deployment instructions, see the main `README_LINUX_VPS.md` file in the project root.

## 🔧 Troubleshooting

- **Chrome Issues**: Run `sudo pkill chrome && sudo pkill chromedriver`
- **Profile Conflicts**: Run `python3 cleanup_old_profiles.py`
- **Login Issues**: Run `python3 clear_twitter_login.py`
- **Service Issues**: Check with `sudo systemctl status tweet-monitor-*.service`
- **Logs**: View with `tail -f tweet_monitor.log`
