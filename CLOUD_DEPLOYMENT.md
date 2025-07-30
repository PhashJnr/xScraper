# Cloud VPS Deployment Guide

## 🚀 **Deploying to Cloud VPS with Twitter Login**

### **📋 Prerequisites**

1. **Cloud VPS Provider:**

   - DigitalOcean, AWS, Vultr, etc.
   - Ubuntu 20.04 LTS recommended
   - 2GB RAM, 1 CPU minimum

2. **Domain/Subdomain (Optional):**
   - For SSL certificates
   - For easier access

### **🔧 Step-by-Step Deployment**

#### **1. Server Setup**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip chromium-browser chromium-chromedriver git curl wget

# Verify Chrome installation
chromium-browser --version
chromedriver --version
```

#### **2. Clone and Setup Project**

```bash
# Clone your repository
git clone <your-repo-url>
cd xUserTweetMonitor

# Install Python dependencies
pip3 install -r requirements.txt

# Create environment file
cp env_example.txt .env
nano .env  # Edit with your settings
```

#### **3. Configure Environment Variables**

```bash
# Edit .env file
nano .env
```

**Required settings:**

```bash
# Twitter Login Credentials (REQUIRED for cloud VPS)
TWITTER_USERNAME=your_twitter_username_or_email
TWITTER_PASSWORD=your_twitter_password

# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Monitoring Intervals
CHECK_INTERVAL_MINUTES=15
YAP_CHECK_INTERVAL_MINUTES=1080

# Other settings...
MAX_TWEETS_TO_SCRAPE=50
USERS_TO_MONITOR=username1,username2,username3
```

#### **4. Setup Twitter Login**

```bash
# Run the Twitter login setup
python3 setup_twitter_login.py
```

This will:

- ✅ Create a Chrome profile with your login
- ✅ Save the profile for future use
- ✅ Verify login is working

#### **5. Test the Setup**

```bash
# Test configuration
python3 check_config.py

# Test YAP scraper
python3 test_simplified_yap.py

# Test user monitoring
python3 main_scraper.py
```

#### **6. Create Systemd Service**

```bash
# Create service file
sudo nano /etc/systemd/system/tweet-monitor.service
```

**Service configuration:**

```ini
[Unit]
Description=X User Tweet Monitor
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

**Enable and start:**

```bash
sudo systemctl enable tweet-monitor
sudo systemctl start tweet-monitor
sudo systemctl status tweet-monitor
```

### **🔐 Twitter Login Solutions**

#### **Option 1: Automated Login (Recommended)**

**Pros:**

- ✅ Fully automated
- ✅ No manual intervention needed
- ✅ Works with headless Chrome
- ✅ Secure credential storage

**Setup:**

```bash
# Add credentials to .env
TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password

# Run login setup
python3 setup_twitter_login.py
```

#### **Option 2: Manual Profile Upload**

**Pros:**

- ✅ No credentials in code
- ✅ Uses your existing profile
- ✅ More secure

**Setup:**

```bash
# 1. Create profile on your local machine
# 2. Compress the chrome_profile folder
tar -czf chrome_profile.tar.gz chrome_profile/

# 3. Upload to server
scp chrome_profile.tar.gz root@your-server-ip:~/

# 4. Extract on server
cd xUserTweetMonitor
tar -xzf ~/chrome_profile.tar.gz
```

#### **Option 3: Docker with Volume Mount**

**Pros:**

- ✅ Isolated environment
- ✅ Easy to manage
- ✅ Portable

**Setup:**

```dockerfile
# Dockerfile
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

### **🔒 Security Considerations**

#### **1. Credential Security**

```bash
# Set proper file permissions
chmod 600 .env
chown root:root .env

# Use environment variables in production
export TWITTER_USERNAME="your_username"
export TWITTER_PASSWORD="your_password"
```

#### **2. Chrome Profile Security**

```bash
# Set proper permissions for Chrome profile
chmod 700 chrome_profile/
chown root:root chrome_profile/
```

#### **3. Firewall Setup**

```bash
# Allow only necessary ports
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### **📊 Monitoring and Logs**

#### **View Logs:**

```bash
# Systemd logs
sudo journalctl -u tweet-monitor -f

# Application logs
tail -f monitor.log

# Check service status
sudo systemctl status tweet-monitor
```

#### **Health Monitoring:**

```bash
# Check if service is running
sudo systemctl is-active tweet-monitor

# Restart if needed
sudo systemctl restart tweet-monitor
```

### **🔄 Maintenance**

#### **Update Application:**

```bash
cd xUserTweetMonitor
git pull origin main
pip3 install -r requirements.txt
sudo systemctl restart tweet-monitor
```

#### **Update Chrome Profile:**

```bash
# If login expires, re-run setup
python3 setup_twitter_login.py
```

### **🚨 Troubleshooting**

#### **Common Issues:**

1. **Chrome Profile Issues:**

   ```bash
   # Remove old profile
   rm -rf chrome_profile/
   # Re-run login setup
   python3 setup_twitter_login.py
   ```

2. **Login Expired:**

   ```bash
   # Re-authenticate
   python3 setup_twitter_login.py
   ```

3. **Service Not Starting:**

   ```bash
   # Check logs
   sudo journalctl -u tweet-monitor -n 50
   # Check configuration
   python3 check_config.py
   ```

4. **Memory Issues:**
   ```bash
   # Monitor memory usage
   htop
   # Restart service if needed
   sudo systemctl restart tweet-monitor
   ```

### **💰 Cost Optimization**

#### **Recommended VPS Specs:**

- **DigitalOcean:** $5-10/month (1GB RAM, 1 CPU)
- **AWS EC2:** $10-15/month (t3.small)
- **Vultr:** $5-10/month (1GB RAM, 1 CPU)

#### **Resource Monitoring:**

```bash
# Install monitoring tools
sudo apt install htop iotop

# Monitor resources
htop
df -h
free -h
```

### **✅ Deployment Checklist**

- [ ] Server setup completed
- [ ] Project cloned and dependencies installed
- [ ] Environment variables configured
- [ ] Twitter login setup completed
- [ ] Tests passing
- [ ] Systemd service created and enabled
- [ ] Service running and monitored
- [ ] Logs being generated
- [ ] Telegram notifications working

### **🎯 Next Steps**

1. **Deploy to your chosen VPS provider**
2. **Follow the setup steps above**
3. **Test the deployment**
4. **Monitor logs and performance**
5. **Set up automated backups if needed**

The application is now ready for 24/7 cloud deployment! 🚀
