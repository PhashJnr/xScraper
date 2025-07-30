# Windows Deployment

This directory contains Windows-specific scripts and configurations for the Twitter/X monitoring application.

## 📁 Directory Structure

```
windows/
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
├── test_windows_dual_services.py # Test dual services on Windows
├── requirements.txt            # Python dependencies
├── env_example.txt            # Environment template
└── .gitignore                # Git ignore rules
```

## 🚀 Quick Start

1. **Install Dependencies:**

   ```cmd
   pip install -r requirements.txt
   ```

2. **Setup Environment:**

   ```cmd
   copy env_example.txt .env
   notepad .env
   ```

3. **Setup Individual Profiles:**

   ```cmd
   python setup_individual_profiles.py
   ```

4. **Login to Twitter:**

   ```cmd
   python setup_twitter_login_user.py
   python setup_twitter_login_yap.py
   ```

5. **Run Services:**

   ```cmd
   # Terminal 1 - User Monitoring
   python main_scraper_locked_pc.py

   # Terminal 2 - YAP Scraping
   python main_yap_scraper.py
   ```

## 📖 Full Documentation

For complete Windows deployment instructions, see the main `README_WINDOWS.md` file in the project root.

## 🔧 Troubleshooting

- **ChromeDriver Issues**: Ensure ChromeDriver is in your PATH
- **Profile Conflicts**: Run `python cleanup_old_profiles.py`
- **Login Issues**: Run `python clear_twitter_login.py`
- **Dual Services**: Test with `python test_windows_dual_services.py`
