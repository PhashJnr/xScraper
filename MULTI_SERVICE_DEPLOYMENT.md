# Multi-Service Deployment Guide

## 🚀 **Complete Guide: Running Both Services Simultaneously on VPS**

### **📊 Service Overview**

| Service             | Interval         | Purpose                               | Output                                          |
| ------------------- | ---------------- | ------------------------------------- | ----------------------------------------------- |
| **👥 User Monitor** | Every 15 minutes | Monitor specific users for new tweets | Telegram notifications + `users_tweetlinks.txt` |
| **🔍 YAP Scraper**  | Every 18 hours   | Scrape YAP search queries             | Telegram file + `yap_links.txt`                 |

---

## **🎯 Quick Start (Recommended Method)**

### **Step 1: Prepare Your VPS**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip chromium-browser chromium-chromedriver git curl wget

# Verify installations
python3 --version
chromium-browser --version
chromedriver --version
```

### **Step 2: Deploy Application**

```bash
# Clone repository
git clone <your-repo-url>
cd xUserTweetMonitor

# Install Python dependencies
pip3 install -r requirements.txt

# Create environment file
cp env_example.txt .env
nano .env  # Configure your settings
```

### **Step 3: Setup Twitter Login**

```bash
# Run Twitter login setup
python3 setup_twitter_login.py

# Verify login works
python3 test_simplified_yap.py
```

### **Step 4: Create Service Files**

```bash
# Copy service files to systemd
sudo cp tweet-monitor-user.service /etc/systemd/system/
sudo cp tweet-monitor-yap.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload
```

### **Step 5: Enable and Start Services**

```bash
# Enable services (auto-start on boot)
sudo systemctl enable tweet-monitor-user
sudo systemctl enable tweet-monitor-yap

# Start services (run now)
sudo systemctl start tweet-monitor-user
sudo systemctl start tweet-monitor-yap

# Check status
sudo systemctl status tweet-monitor-user
sudo systemctl status tweet-monitor-yap
```

---

## **📋 Detailed Configuration**

### **Environment Configuration (.env)**

```bash
# Twitter Login Credentials (REQUIRED)
TWITTER_USERNAME=your_twitter_username_or_email
TWITTER_PASSWORD=your_twitter_password

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Monitoring Intervals (in minutes)
CHECK_INTERVAL_MINUTES=15                    # User monitoring (15 minutes)
YAP_CHECK_INTERVAL_MINUTES=1080             # YAP links (18 hours = 1080 minutes)

# Maximum tweets to scrape
MAX_TWEETS_TO_SCRAPE=50

# Users to Monitor (comma-separated usernames without @)
USERS_TO_MONITOR=username1,username2,username3

# YAP Search Configuration
YAP_SEARCH_KEYWORDS=("cysic" OR @cysic_xyz)
YAP_FILTER_VERIFIED=true
YAP_MIN_REPLIES=20
YAP_LANGUAGE=en
YAP_TIME_WINDOW=1440

# Logging
LOG_LEVEL=INFO
LOG_FILE=monitor.log
```

### **Service File: User Monitor**

```ini
[Unit]
Description=X User Tweet Monitor (User Monitoring)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/xUserTweetMonitor
ExecStart=/usr/bin/python3 main_scraper_locked_pc.py
Restart=always
RestartSec=10
Environment=DISPLAY=:99

[Install]
WantedBy=multi-user.target
```

### **Service File: YAP Scraper**

```ini
[Unit]
Description=X User Tweet Monitor (YAP Links)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/xUserTweetMonitor
ExecStart=/usr/bin/python3 main_yap_scraper.py
Restart=always
RestartSec=10
Environment=DISPLAY=:99

[Install]
WantedBy=multi-user.target
```

---

## **🔧 Service Management Commands**

### **Start Services**

```bash
# Start both services
sudo systemctl start tweet-monitor-user
sudo systemctl start tweet-monitor-yap

# Start with specific intervals
sudo systemctl set-environment CHECK_INTERVAL_MINUTES=10
sudo systemctl set-environment YAP_CHECK_INTERVAL_MINUTES=720
sudo systemctl restart tweet-monitor-user
sudo systemctl restart tweet-monitor-yap
```

### **Stop Services**

```bash
# Stop both services
sudo systemctl stop tweet-monitor-user
sudo systemctl stop tweet-monitor-yap

# Stop all tweet-monitor services
sudo systemctl stop tweet-monitor-*
```

### **Restart Services**

```bash
# Restart both services
sudo systemctl restart tweet-monitor-user
sudo systemctl restart tweet-monitor-yap

# Restart all tweet-monitor services
sudo systemctl restart tweet-monitor-*
```

### **Check Service Status**

```bash
# Check individual services
sudo systemctl status tweet-monitor-user
sudo systemctl status tweet-monitor-yap

# Check if services are active
sudo systemctl is-active tweet-monitor-user
sudo systemctl is-active tweet-monitor-yap

# List all tweet-monitor services
sudo systemctl list-units --type=service | grep tweet-monitor
```

---

## **📊 Monitoring and Logs**

### **View Service Logs**

```bash
# View logs for user monitor
sudo journalctl -u tweet-monitor-user -f

# View logs for YAP scraper
sudo journalctl -u tweet-monitor-yap -f

# View logs for both services
sudo journalctl -u tweet-monitor-* -f

# View recent logs (last 100 lines)
sudo journalctl -u tweet-monitor-user -n 100
sudo journalctl -u tweet-monitor-yap -n 100
```

### **Application Logs**

```bash
# View application logs
tail -f monitor.log

# View specific log sections
grep "User monitoring" monitor.log
grep "YAP scraping" monitor.log
grep "Telegram" monitor.log
```

### **Resource Monitoring**

```bash
# Monitor system resources
htop

# Monitor memory usage
free -h

# Monitor disk usage
df -h

# Monitor Chrome processes
ps aux | grep chrome
ps aux | grep python
```

---

## **🚨 Troubleshooting**

### **Common Issues and Solutions**

#### **1. Service Not Starting**

```bash
# Check service logs
sudo journalctl -u tweet-monitor-user -n 50
sudo journalctl -u tweet-monitor-yap -n 50

# Check configuration
python3 check_config.py

# Test individual components
python3 test_simplified_yap.py
python3 test_telegram_file.py
```

#### **2. Chrome Profile Issues**

```bash
# Remove old profile
rm -rf chrome_profile/

# Re-run login setup
python3 setup_twitter_login.py

# Restart services
sudo systemctl restart tweet-monitor-user
sudo systemctl restart tweet-monitor-yap
```

#### **3. Memory Issues**

```bash
# Check memory usage
free -h

# Kill Chrome processes if needed
pkill chrome
pkill chromedriver

# Restart services
sudo systemctl restart tweet-monitor-*
```

#### **4. Login Expired**

```bash
# Re-authenticate
python3 setup_twitter_login.py

# Restart services
sudo systemctl restart tweet-monitor-user
sudo systemctl restart tweet-monitor-yap
```

#### **5. Telegram Notifications Not Working**

```bash
# Test Telegram connection
python3 test_telegram_file.py

# Check bot token and chat ID
python3 check_config.py
```

### **Debug Commands**

```bash
# Check if Chrome is running
ps aux | grep chrome

# Check if Python processes are running
ps aux | grep python

# Check file permissions
ls -la chrome_profile/
ls -la .env

# Check disk space
df -h

# Check memory usage
free -h
```

---

## **📈 Performance Optimization**

### **Resource Allocation**

```bash
# Set process priorities
sudo renice -n -10 -p $(pgrep -f main_scraper_locked_pc.py)
sudo renice -n -10 -p $(pgrep -f main_yap_scraper.py)

# Monitor resource usage
htop
iotop
```

### **Chrome Optimization**

```bash
# Add to Chrome options in scraper files:
chrome_options.add_argument('--memory-pressure-off')
chrome_options.add_argument('--max_old_space_size=512')
chrome_options.add_argument('--disable-dev-shm-usage')
```

### **Log Rotation**

```bash
# Create log rotation configuration
sudo nano /etc/logrotate.d/tweet-monitor

# Add configuration
/root/xUserTweetMonitor/monitor.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    postrotate
        sudo systemctl reload tweet-monitor-user
        sudo systemctl reload tweet-monitor-yap
    endscript
}
```

---

## **🔒 Security Considerations**

### **File Permissions**

```bash
# Set proper permissions
chmod 600 .env
chmod 700 chrome_profile/
chown root:root .env
chown root:root chrome_profile/
```

### **Firewall Setup**

```bash
# Allow only necessary ports
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### **Credential Security**

```bash
# Use environment variables in production
export TWITTER_USERNAME="your_username"
export TWITTER_PASSWORD="your_password"
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

---

## **🔄 Maintenance and Updates**

### **Update Application**

```bash
# Pull latest changes
cd xUserTweetMonitor
git pull origin main

# Install new dependencies
pip3 install -r requirements.txt

# Restart services
sudo systemctl restart tweet-monitor-user
sudo systemctl restart tweet-monitor-yap
```

### **Update Chrome Profile**

```bash
# If login expires, re-run setup
python3 setup_twitter_login.py

# Restart services
sudo systemctl restart tweet-monitor-*
```

### **Backup Configuration**

```bash
# Backup important files
cp .env .env.backup
cp -r chrome_profile/ chrome_profile_backup/

# Restore if needed
cp .env.backup .env
cp -r chrome_profile_backup/ chrome_profile/
```

---

## **📊 Monitoring Dashboard**

### **Health Check Script**

```bash
#!/bin/bash
# health_check.sh

echo "=== Tweet Monitor Health Check ==="
echo "Date: $(date)"
echo ""

# Check services
echo "Service Status:"
sudo systemctl is-active tweet-monitor-user
sudo systemctl is-active tweet-monitor-yap
echo ""

# Check processes
echo "Process Status:"
ps aux | grep -E "(main_scraper|main_yap_scraper)" | grep -v grep
echo ""

# Check logs
echo "Recent Logs:"
tail -n 5 monitor.log
echo ""

# Check disk space
echo "Disk Usage:"
df -h | grep -E "(/$|/home)"
echo ""

# Check memory
echo "Memory Usage:"
free -h
echo ""
```

### **Automated Health Check**

```bash
# Add to crontab
crontab -e

# Add this line to run health check every hour
0 * * * * /root/xUserTweetMonitor/health_check.sh >> /var/log/tweet-monitor-health.log
```

---

## **✅ Deployment Checklist**

### **Pre-Deployment**

- [ ] VPS server ready (2GB RAM, Ubuntu 20.04+)
- [ ] Dependencies installed (Python, Chrome, Git)
- [ ] Repository cloned
- [ ] Environment configured (.env file)
- [ ] Twitter login tested
- [ ] Telegram notifications tested

### **Service Setup**

- [ ] Service files created
- [ ] Services enabled
- [ ] Services started
- [ ] Status verified
- [ ] Logs being generated

### **Monitoring Setup**

- [ ] Log rotation configured
- [ ] Health check script created
- [ ] Resource monitoring active
- [ ] Backup strategy in place

### **Security Setup**

- [ ] File permissions set
- [ ] Firewall configured
- [ ] Credentials secured
- [ ] SSH keys configured

---

## **🎯 Expected Results**

### **User Monitor Service:**

- ✅ Runs every 15 minutes
- ✅ Sends Telegram notifications for new tweets
- ✅ Saves tweet URLs to `users_tweetlinks.txt`
- ✅ Sends file to Telegram

### **YAP Scraper Service:**

- ✅ Runs every 18 hours
- ✅ Scrapes YAP search queries
- ✅ Saves URLs to `yap_links.txt`
- ✅ Sends file to Telegram

### **System Performance:**

- ✅ Memory usage: ~800MB total
- ✅ CPU usage: Low during idle
- ✅ Disk usage: ~2GB total
- ✅ Network: ~6GB/month

---

## **🚀 Ready for Production**

Your multi-service deployment is now ready for 24/7 operation! Both services will run independently with their respective intervals, providing comprehensive Twitter monitoring and YAP link scraping with Telegram notifications.

**Next Steps:**

1. Monitor logs for the first few hours
2. Verify Telegram notifications are working
3. Adjust intervals if needed
4. Set up automated backups
5. Configure monitoring alerts

Happy monitoring! 🎉
