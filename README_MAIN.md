# X User Tweet Monitor - Main Project

A comprehensive Python application for monitoring Twitter/X users and scraping tweet URLs with Telegram notifications. Features individual Chrome profiles for simultaneous operation.

## 🏗️ Project Structure

```
xUserTweetMonitor/
├── README_MAIN.md              # This file - Main project overview
├── README_WINDOWS.md           # Complete Windows deployment guide
├── README_LINUX_VPS.md         # Complete Linux VPS deployment guide
├── windows/                    # Windows-specific deployment
│   ├── README.md              # Windows quick start guide
│   ├── main_scraper_locked_pc.py
│   ├── main_yap_scraper.py
│   ├── scraper_monitor.py
│   ├── yap_scraper.py
│   ├── robust_notifier.py
│   ├── config.py
│   ├── setup_individual_profiles.py
│   ├── setup_twitter_login_user.py
│   ├── setup_twitter_login_yap.py
│   ├── clear_twitter_login.py
│   ├── cleanup_old_profiles.py
│   ├── test_windows_dual_services.py
│   ├── requirements.txt
│   └── env_example.txt
├── linux/                      # Linux VPS-specific deployment
│   ├── README.md              # Linux quick start guide
│   ├── main_scraper_locked_pc.py
│   ├── main_yap_scraper.py
│   ├── scraper_monitor.py
│   ├── yap_scraper.py
│   ├── robust_notifier.py
│   ├── config.py
│   ├── setup_individual_profiles.py
│   ├── setup_twitter_login_user.py
│   ├── setup_twitter_login_yap.py
│   ├── clear_twitter_login.py
│   ├── cleanup_old_profiles.py
│   ├── requirements.txt
│   ├── env_example.txt
│   ├── tweet-monitor-user.service
│   └── tweet-monitor-yap.service
├── requirements.txt            # Main requirements file
├── .gitignore                 # Git ignore rules
└── README.md                  # Legacy main README
```

## 🚀 Quick Start

### For Windows Users

1. **Navigate to Windows directory:**

   ```cmd
   cd windows
   ```

2. **Follow Windows deployment guide:**

   ```cmd
   # Install dependencies
   pip install -r requirements.txt

   # Setup environment
   copy env_example.txt .env
   notepad .env

   # Setup profiles and login
   python setup_individual_profiles.py
   python setup_twitter_login_user.py
   python setup_twitter_login_yap.py

   # Run services
   python main_scraper_locked_pc.py
   python main_yap_scraper.py
   ```

### For Linux VPS Users

1. **Navigate to Linux directory:**

   ```bash
   cd linux
   ```

2. **Follow Linux deployment guide:**

   ```bash
   # Install dependencies
   pip3 install -r requirements.txt

   # Setup environment
   cp env_example.txt .env
   nano .env

   # Setup profiles and login
   python3 setup_individual_profiles.py
   python3 setup_twitter_login_user.py
   python3 setup_twitter_login_yap.py

   # Run services (background)
   nohup python3 main_scraper_locked_pc.py > user_monitor.log 2>&1 &
   nohup python3 main_yap_scraper.py > yap_scraper.log 2>&1 &
   ```

## 📖 Documentation

### Complete Guides

- **Windows**: See `README_WINDOWS.md` for complete Windows deployment
- **Linux VPS**: See `README_LINUX_VPS.md` for complete Linux VPS deployment

### Quick Start Guides

- **Windows**: See `windows/README.md` for Windows quick start
- **Linux**: See `linux/README.md` for Linux quick start

## 🎯 Features

### Core Features

- **Individual Chrome Profiles**: Separate profiles for user monitoring and YAP scraping
- **Simultaneous Operation**: Both services can run at the same time without conflicts
- **Telegram Integration**: Send notifications and files directly to Telegram
- **Configurable Search**: Customize YAP search parameters via `.env` file
- **Robust Error Handling**: Retry logic, rate limiting, and graceful failures

### Platform-Specific Features

- **Windows**: Optimized for desktop operation with GUI support
- **Linux VPS**: Headless operation with systemd services and background processes

## 🔧 Development & Debugging

### Benefits of New Structure

- **Separation of Concerns**: Windows and Linux code are isolated
- **Easier Debugging**: Platform-specific issues are contained
- **Cleaner Organization**: No platform-specific files in root
- **Better Maintenance**: Each platform has its own configuration

### Development Workflow

1. **Make changes in appropriate directory** (windows/ or linux/)
2. **Test on target platform**
3. **Update documentation** if needed
4. **Commit changes**

## 📁 File Organization

### Shared Files (in both directories)

- Core application logic (`scraper_monitor.py`, `yap_scraper.py`)
- Configuration (`config.py`, `robust_notifier.py`)
- Profile management scripts
- Requirements and environment templates

### Platform-Specific Files

- **Windows**: `test_windows_dual_services.py`
- **Linux**: `tweet-monitor-*.service` files

### Root Directory Files

- Main documentation (`README_*.md`)
- Legacy files (for backward compatibility)
- Git configuration

## 🧹 Cleanup

### Files to Remove (Legacy)

- Old test files that are no longer needed
- Duplicate configuration files
- Outdated documentation

### Files to Keep (Root)

- Main documentation
- Git configuration
- Legacy README for reference

## 📞 Support

### Getting Help

1. **Check platform-specific README** in windows/ or linux/
2. **Review complete deployment guide** (README_WINDOWS.md or README_LINUX_VPS.md)
3. **Check troubleshooting sections** in respective guides
4. **Create issue** with platform and error details

### Platform-Specific Issues

- **Windows Issues**: Check `windows/README.md` troubleshooting
- **Linux Issues**: Check `linux/README.md` troubleshooting
- **General Issues**: Check main deployment guides

## 📝 License

This project is for educational and personal use. Please respect Twitter's terms of service.
