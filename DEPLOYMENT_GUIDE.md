# 🚀 Production Deployment Guide

This guide covers deploying the YouTube Automation System to production with best practices.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Deployment Methods](#deployment-methods)
3. [Systemd Service Setup](#systemd-service-setup)
4. [Nginx Reverse Proxy](#nginx-reverse-proxy)
5. [SSL/HTTPS Configuration](#ssl-https-configuration)
6. [Docker Production Deployment](#docker-production-deployment)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Backup and Recovery](#backup-and-recovery)
9. [Security Hardening](#security-hardening)

---

## Prerequisites

Before deploying to production:

- [ ] Linux server (Ubuntu 20.04+ or similar)
- [ ] Domain name pointed to your server (for SSL)
- [ ] Firewall configured (ports 80, 443, 22)
- [ ] All API credentials ready (OpenAI, YouTube, Amazon)
- [ ] Minimum 2GB RAM, 2 CPU cores
- [ ] 20GB+ disk space

---

## Deployment Methods

### Option 1: Docker (Recommended)

**Pros:**
- Consistent environment
- Easy updates
- Better isolation
- Simple rollback

**Cons:**
- Requires Docker knowledge
- Slightly more resource usage

### Option 2: Systemd Service

**Pros:**
- Direct system integration
- Lower overhead
- Fine-grained control

**Cons:**
- Manual dependency management
- OS-specific

---

## Systemd Service Setup

### Step 1: Complete Installation

```bash
# Clone repository
cd /opt
sudo git clone https://github.com/S3OPS/youtube.git
cd youtube

# Run setup
sudo ./setup.sh
```

### Step 2: Create System User

```bash
# Create dedicated user (better security)
sudo useradd -r -s /bin/false youtube-automation

# Set ownership
sudo chown -R youtube-automation:youtube-automation /opt/youtube
```

### Step 3: Configure Service

```bash
# Copy service file
sudo cp youtube-automation.service /etc/systemd/system/

# Edit to match your paths
sudo nano /etc/systemd/system/youtube-automation.service
```

Update these lines:
```ini
User=youtube-automation
Group=youtube-automation
WorkingDirectory=/opt/youtube
Environment="PATH=/opt/youtube/.venv/bin:/usr/local/bin:/usr/bin:/bin"
EnvironmentFile=/opt/youtube/.env
ExecStart=/opt/youtube/.venv/bin/python app.py
ReadWritePaths=/opt/youtube/data /opt/youtube/.cache /opt/youtube/logs
```

### Step 4: Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable on boot
sudo systemctl enable youtube-automation

# Start service
sudo systemctl start youtube-automation

# Check status
sudo systemctl status youtube-automation
```

### Step 5: Verify Service

```bash
# Check if running
sudo systemctl is-active youtube-automation

# View logs
sudo journalctl -u youtube-automation -f

# Test endpoint
curl http://localhost:5000/health
```

---

## Nginx Reverse Proxy

### Why Use Nginx?

- SSL/TLS termination
- Static file serving
- Rate limiting
- Load balancing
- Better security headers

### Step 1: Install Nginx

```bash
sudo apt-get update
sudo apt-get install -y nginx
```

### Step 2: Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/youtube-automation
```

Add this configuration:

```nginx
# Upstream to Flask application
upstream youtube_app {
    server 127.0.0.1:5000;
}

# HTTP server (redirects to HTTPS)
server {
    listen 80;
    listen [::]:80;
    server_name your-domain.com www.your-domain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL configuration (will be added by Certbot)
    # ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/youtube-automation-access.log;
    error_log /var/log/nginx/youtube-automation-error.log;

    # Max upload size for video files
    client_max_body_size 500M;

    # Proxy settings
    location / {
        proxy_pass http://youtube_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeouts for long-running requests
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://youtube_app/health;
        access_log off;
    }

    # Rate limiting for API endpoints
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://youtube_app;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files (if any)
    location /static/ {
        alias /opt/youtube/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}

# Rate limiting zone
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
```

### Step 3: Enable Configuration

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/youtube-automation /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

---

## SSL/HTTPS Configuration

### Using Let's Encrypt (Free SSL)

```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

Certbot will automatically:
- Obtain SSL certificate
- Update nginx configuration
- Set up auto-renewal

### Manual SSL Certificate

If using a purchased SSL certificate:

```bash
# Copy certificates to server
sudo mkdir -p /etc/ssl/youtube-automation
sudo cp your-cert.crt /etc/ssl/youtube-automation/
sudo cp your-key.key /etc/ssl/youtube-automation/
sudo chmod 600 /etc/ssl/youtube-automation/your-key.key
```

Update nginx configuration:
```nginx
ssl_certificate /etc/ssl/youtube-automation/your-cert.crt;
ssl_certificate_key /etc/ssl/youtube-automation/your-key.key;
```

---

## Docker Production Deployment

### Step 1: Prepare Environment

```bash
# Create project directory
sudo mkdir -p /opt/youtube-automation
cd /opt/youtube-automation

# Clone repository
sudo git clone https://github.com/S3OPS/youtube.git .

# Create .env file
sudo nano .env
# Add your configuration
```

### Step 2: Build and Run with Docker Compose

```bash
# Build image
sudo docker-compose build

# Start in detached mode
sudo docker-compose up -d

# Check logs
sudo docker-compose logs -f

# Check status
sudo docker-compose ps
```

### Step 3: Configure Nginx for Docker

Update nginx upstream:
```nginx
upstream youtube_app {
    server 127.0.0.1:5000;  # Docker exposes on host port
}
```

### Step 4: Update and Restart

```bash
# Pull latest changes
git pull

# Rebuild and restart
sudo docker-compose down
sudo docker-compose build
sudo docker-compose up -d
```

---

## Monitoring and Logging

### System Logs (Systemd)

```bash
# View logs
sudo journalctl -u youtube-automation -f

# Last 100 lines
sudo journalctl -u youtube-automation -n 100

# Logs since yesterday
sudo journalctl -u youtube-automation --since yesterday

# Export logs
sudo journalctl -u youtube-automation > youtube-logs.txt
```

### Docker Logs

```bash
# View logs
sudo docker-compose logs -f

# Last 100 lines
sudo docker-compose logs --tail=100

# Specific service
sudo docker-compose logs youtube-automation
```

### Application Logs

```bash
# Application logs
tail -f /opt/youtube/logs/app.log

# Error logs only
grep ERROR /opt/youtube/logs/app.log
```

### Health Monitoring

Create monitoring script:

```bash
#!/bin/bash
# save as /opt/youtube/monitor.sh

ENDPOINT="http://localhost:5000/health"
LOG_FILE="/var/log/youtube-health.log"

while true; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" $ENDPOINT)
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    if [ $STATUS -eq 200 ]; then
        echo "[$TIMESTAMP] OK - Health check passed" >> $LOG_FILE
    else
        echo "[$TIMESTAMP] FAIL - Health check failed (HTTP $STATUS)" >> $LOG_FILE
        # Send alert (email, Slack, etc.)
    fi
    
    sleep 60
done
```

### Set Up Monitoring Cron

```bash
# Make executable
chmod +x /opt/youtube/monitor.sh

# Add to crontab
crontab -e
```

Add:
```cron
@reboot /opt/youtube/monitor.sh &
```

---

## Backup and Recovery

### What to Backup

1. **Configuration files:**
   - `.env`
   - `client_secrets.json`
   - `config.py`

2. **Data files:**
   - `data/automation_history.json`
   - Any generated videos
   - Cache files (optional)

### Automated Backup Script

```bash
#!/bin/bash
# save as /opt/youtube/backup.sh

BACKUP_DIR="/backup/youtube"
DATE=$(date +%Y%m%d_%H%M%S)
SOURCE_DIR="/opt/youtube"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup configuration
tar -czf $BACKUP_DIR/config_$DATE.tar.gz \
    $SOURCE_DIR/.env \
    $SOURCE_DIR/client_secrets.json

# Backup data
tar -czf $BACKUP_DIR/data_$DATE.tar.gz \
    $SOURCE_DIR/data/

# Keep only last 30 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

### Schedule Backups

```bash
# Make executable
chmod +x /opt/youtube/backup.sh

# Add to crontab (daily at 2 AM)
crontab -e
```

Add:
```cron
0 2 * * * /opt/youtube/backup.sh >> /var/log/youtube-backup.log 2>&1
```

### Restore from Backup

```bash
# Stop service
sudo systemctl stop youtube-automation

# Restore configuration
cd /opt/youtube
tar -xzf /backup/youtube/config_YYYYMMDD_HHMMSS.tar.gz

# Restore data
tar -xzf /backup/youtube/data_YYYYMMDD_HHMMSS.tar.gz

# Start service
sudo systemctl start youtube-automation
```

---

## Security Hardening

### Firewall Configuration

```bash
# Install UFW (if not installed)
sudo apt-get install -y ufw

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (important!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status verbose
```

### Secure API Keys

```bash
# Set proper permissions on .env
chmod 600 /opt/youtube/.env
chown youtube-automation:youtube-automation /opt/youtube/.env

# Same for client_secrets.json
chmod 600 /opt/youtube/client_secrets.json
chown youtube-automation:youtube-automation /opt/youtube/client_secrets.json
```

### Rate Limiting in Nginx

Already configured in nginx example above:
```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
```

### Fail2ban for SSH Protection

```bash
# Install fail2ban
sudo apt-get install -y fail2ban

# Configure
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
```

Enable SSH protection:
```ini
[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

```bash
# Restart fail2ban
sudo systemctl restart fail2ban
```

### Keep System Updated

```bash
# Create update script
sudo nano /opt/youtube/update.sh
```

```bash
#!/bin/bash
# Automatic security updates

# Update system packages
apt-get update
apt-get upgrade -y

# Update Python packages
cd /opt/youtube
source .venv/bin/activate
pip list --outdated --format=freeze | cut -d= -f1 | xargs -n1 pip install -U

# Restart service
systemctl restart youtube-automation

echo "Update completed: $(date)"
```

Schedule weekly:
```cron
0 3 * * 0 /opt/youtube/update.sh >> /var/log/youtube-update.log 2>&1
```

---

## Performance Tuning

### Optimize Flask for Production

Instead of Flask's development server, use Gunicorn:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Update systemd service:
```ini
ExecStart=/opt/youtube/.venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

### Cache Configuration

In `.env`:
```env
# Increase cache for better performance
CACHE_TTL_SECONDS=3600
CACHE_MAX_SIZE_MB=500
```

### Database for Production (Optional)

For high-volume usage, consider replacing JSON file storage with PostgreSQL or MongoDB.

---

## Troubleshooting

### Service Won't Start

```bash
# Check service status
sudo systemctl status youtube-automation

# Check logs
sudo journalctl -u youtube-automation -n 50

# Common issues:
# - Wrong paths in service file
# - Missing .env file
# - Permission issues
# - Port already in use
```

### Nginx 502 Bad Gateway

```bash
# Check if app is running
curl http://localhost:5000/health

# Check nginx error log
sudo tail -f /var/log/nginx/error.log

# Restart both services
sudo systemctl restart youtube-automation
sudo systemctl restart nginx
```

### SSL Certificate Issues

```bash
# Check certificate
sudo certbot certificates

# Renew manually
sudo certbot renew

# Check nginx config
sudo nginx -t
```

---

## Maintenance Checklist

### Daily
- [ ] Check service status: `systemctl status youtube-automation`
- [ ] Monitor logs for errors: `journalctl -u youtube-automation --since today`
- [ ] Verify health endpoint: `curl http://localhost/health`

### Weekly
- [ ] Review disk space: `df -h`
- [ ] Check backup status
- [ ] Review application logs
- [ ] Check for security updates

### Monthly
- [ ] Update system packages
- [ ] Update Python dependencies
- [ ] Review and rotate logs
- [ ] Test backup restoration
- [ ] Review API usage and costs

---

## Support

For production deployment issues:
- Review logs first
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Open GitHub issue with logs
- Contact your system administrator

---

**Production deployment complete! Your YouTube Automation System is now running securely and reliably.**
