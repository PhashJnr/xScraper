# Multi-Service Deployment Guide

## 🚀 **Running Both Services Simultaneously on VPS**

### **📊 Service Overview**

- **👥 User Monitor:** Every 15 minutes
- **🔍 YAP Scraper:** Every 18 hours (1080 minutes)
- **📁 Shared Chrome Profile:** Both services use the same profile
- **📊 Separate Logs:** Each service has its own logging

---

## **Option 1: 🎛️ Separate Systemd Services (Recommended)**

### **Setup Steps:**

#### **1. Create Service Files**

**User Monitor Service:**

```bash
sudo nano /etc/systemd/system/tweet-monitor-user.service
```

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

**YAP Scraper Service:**

```bash
sudo nano /etc/systemd/system/tweet-monitor-yap.service
```

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

#### **2. Enable and Start Services**

```bash
# Enable both services
sudo systemctl enable tweet-monitor-user
sudo systemctl enable tweet-monitor-yap

# Start both services
sudo systemctl start tweet-monitor-user
sudo systemctl start tweet-monitor-yap

# Check status
sudo systemctl status tweet-monitor-user
sudo systemctl status tweet-monitor-yap
```

#### **3. Monitor Services**

```bash
# View logs for user monitor
sudo journalctl -u tweet-monitor-user -f

# View logs for YAP scraper
sudo journalctl -u tweet-monitor-yap -f

# Check both services
sudo systemctl is-active tweet-monitor-user
sudo systemctl is-active tweet-monitor-yap
```

#### **4. Service Management**

```bash
# Stop both services
sudo systemctl stop tweet-monitor-user
sudo systemctl stop tweet-monitor-yap

# Restart both services
sudo systemctl restart tweet-monitor-user
sudo systemctl restart tweet-monitor-yap

# Disable services
sudo systemctl disable tweet-monitor-user
sudo systemctl disable tweet-monitor-yap
```

---

## **Option 2: 🎯 Combined Service Script**

### **Setup Steps:**

#### **1. Use the Combined Runner**

```bash
# Run both services in one script
python3 run_both_services.py
```

#### **2. Create Systemd Service for Combined Runner**

```bash
sudo nano /etc/systemd/system/tweet-monitor-combined.service
```

```ini
[Unit]
Description=X User Tweet Monitor (Combined Services)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/xUserTweetMonitor
ExecStart=/usr/bin/python3 run_both_services.py
Restart=always
RestartSec=10
Environment=DISPLAY=:99

[Install]
WantedBy=multi-user.target
```

#### **3. Enable Combined Service**

```bash
sudo systemctl enable tweet-monitor-combined
sudo systemctl start tweet-monitor-combined
sudo systemctl status tweet-monitor-combined
```

---

## **Option 3: 🐳 Docker Compose**

### **Setup Steps:**

#### **1. Create Dockerfile**

```dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create volume for Chrome profile
VOLUME /app/chrome_profile

CMD ["python", "main_scraper_locked_pc.py"]
```

#### **2. Run with Docker Compose**

```bash
# Start both services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## **📊 Monitoring and Management**

### **Service Status Commands:**

```bash
# Check all services
sudo systemctl list-units --type=service | grep tweet-monitor

# View all logs
sudo journalctl -u tweet-monitor-* -f

# Check resource usage
htop
ps aux | grep python
```

### **Log Management:**

```bash
# Create log rotation
sudo nano /etc/logrotate.d/tweet-monitor

# Add configuration
/root/xUserTweetMonitor/monitor.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

### **Resource Monitoring:**

```bash
# Monitor memory usage
free -h

# Monitor disk usage
df -h

# Monitor CPU usage
top

# Monitor Chrome processes
ps aux | grep chrome
```

---

## **🔧 Configuration Management**

### **Shared Configuration:**

Both services use the same `.env` file:

```bash
# .env file
TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id

# Intervals
CHECK_INTERVAL_MINUTES=15
YAP_CHECK_INTERVAL_MINUTES=1080

# Other settings...
MAX_TWEETS_TO_SCRAPE=50
USERS_TO_MONITOR=username1,username2,username3
```

### **Service-Specific Configuration:**

You can override settings per service:

```bash
# For user monitor service
sudo systemctl set-environment CHECK_INTERVAL_MINUTES=10

# For YAP scraper service
sudo systemctl set-environment YAP_CHECK_INTERVAL_MINUTES=720
```

---

## **🚨 Troubleshooting**

### **Common Issues:**

#### **1. Chrome Profile Conflicts**

```bash
# Check if Chrome is running
ps aux | grep chrome

# Kill conflicting processes
pkill chrome
pkill chromedriver

# Restart services
sudo systemctl restart tweet-monitor-user
sudo systemctl restart tweet-monitor-yap
```

#### **2. Memory Issues**

```bash
# Check memory usage
free -h

# If low memory, restart services
sudo systemctl restart tweet-monitor-user
sudo systemctl restart tweet-monitor-yap
```

#### **3. Login Expired**

```bash
# Re-run login setup
python3 setup_twitter_login.py

# Restart services
sudo systemctl restart tweet-monitor-user
sudo systemctl restart tweet-monitor-yap
```

#### **4. Service Not Starting**

```bash
# Check service logs
sudo journalctl -u tweet-monitor-user -n 50
sudo journalctl -u tweet-monitor-yap -n 50

# Check configuration
python3 check_config.py
```

---

## **📈 Performance Optimization**

### **Resource Allocation:**

```bash
# Monitor resource usage
htop

# Set process priorities
sudo renice -n -10 -p $(pgrep -f main_scraper_locked_pc.py)
sudo renice -n -10 -p $(pgrep -f main_yap_scraper.py)
```

### **Chrome Optimization:**

```bash
# Limit Chrome memory usage
# Add to Chrome options in scraper files:
chrome_options.add_argument('--memory-pressure-off')
chrome_options.add_argument('--max_old_space_size=512')
```

---

## **✅ Deployment Checklist**

- [ ] Both service files created
- [ ] Services enabled and started
- [ ] Twitter login setup completed
- [ ] Configuration verified
- [ ] Logs being generated
- [ ] Telegram notifications working
- [ ] Resource usage monitored
- [ ] Backup strategy in place

---

## **🎯 Recommended Approach**

**For Production VPS:**

1. **Use Separate Systemd Services** (Option 1)
   - ✅ Better isolation
   - ✅ Independent restart
   - ✅ Easier monitoring
   - ✅ Better resource management

**For Development/Testing:** 2. **Use Combined Service Script** (Option 2)

- ✅ Simpler setup
- ✅ Single log file
- ✅ Easier debugging

**For Containerized Deployment:** 3. **Use Docker Compose** (Option 3)

- ✅ Isolated environments
- ✅ Easy scaling
- ✅ Portable deployment

Both services will run simultaneously with their respective intervals! 🚀
