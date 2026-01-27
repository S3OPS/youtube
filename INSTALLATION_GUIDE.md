# 🚀 Installation & Deployment Guide

**Comprehensive guide for installing and running the Automated YouTube Content Creation System**

---

## 📋 Executive Summary

Based on analysis of the current system, here are the **recommended installation methods** ranked by efficiency and use case:

### ✅ Recommended Approaches

| Method | Best For | Efficiency | Complexity |
|--------|----------|-----------|------------|
| **1. One-Command Setup** | Local development, first-time users | ⭐⭐⭐⭐⭐ | Low |
| **2. Docker (NEW)** | Production, consistency, isolation | ⭐⭐⭐⭐⭐ | Low |
| **3. Manual Setup** | Advanced users, custom configurations | ⭐⭐⭐ | Medium |
| **4. System Service** | Production servers, always-on | ⭐⭐⭐⭐ | Medium |

---

## 🎯 Current State Analysis

### What's Working Well ✅

1. **Excellent One-Command Setup** (`./setup.sh`)
   - Automatically installs Python 3.12
   - Handles multiple package managers (apt, dnf, brew, winget)
   - Creates virtual environment
   - Installs all dependencies
   - Runs interactive setup wizard
   - Cross-platform support

2. **Good Documentation**
   - Comprehensive README
   - Detailed setup guides
   - Troubleshooting documentation
   - Architecture documentation

3. **Clean Dependencies**
   - Pure Python (no Node.js needed)
   - No database required (uses JSON file storage)
   - Minimal external dependencies (just ffmpeg)

### Potential Improvements 🔧

1. **Missing Docker Support** 
   - Would provide better isolation
   - Easier deployment to cloud platforms
   - Consistent environment across machines
   - No need to install Python/ffmpeg manually

2. **No Production Deployment Guide**
   - Missing systemd service examples
   - No reverse proxy configuration (nginx/Apache)
   - No cloud deployment examples (AWS/GCP/Azure/Heroku)

3. **No Automated Testing in Setup**
   - Setup script doesn't verify installation
   - No health check endpoint

4. **Limited Environment Management**
   - Could benefit from more robust config validation
   - No example for multiple environments (dev/staging/prod)

---

## 🚀 Installation Methods

### Method 1: One-Command Setup (Recommended for Local Development)

**Best for:** First-time users, local development, quick testing

```bash
# Clone the repository
git clone https://github.com/S3OPS/youtube.git
cd youtube

# Run the one-command setup
./setup.sh
```

**What it does:**
1. ✅ Installs Python 3.12 (if not present)
2. ✅ Installs ffmpeg
3. ✅ Creates virtual environment at `.venv/`
4. ✅ Installs all Python dependencies
5. ✅ Runs interactive setup wizard
6. ✅ Creates `.env` file with your configuration
7. ✅ Cleans up cache files

**Next steps:**
```bash
# Add your YouTube OAuth credentials
# Download client_secrets.json from Google Cloud Console
# Save it to the project root

# Start the web dashboard
python app.py

# Or create a video via CLI
python create_video.py
```

**Pros:**
- ⚡ Fastest way to get started
- 🔄 Handles all dependencies automatically
- 🎯 Interactive configuration wizard
- 🧹 Cleans up unnecessary files

**Cons:**
- ⚠️ Requires sudo for system package installation
- 💻 Installs Python 3.12 system-wide

---

### Method 2: Docker (NEW - Recommended for Production)

**Best for:** Production deployments, cloud platforms, consistency, isolation

> **Note:** This is a new improvement we're adding to make deployment more efficient.

```bash
# Clone the repository
git clone https://github.com/S3OPS/youtube.git
cd youtube

# Build the Docker image
docker build -t youtube-automation .

# Run with environment variables
docker run -d \
  --name youtube-app \
  -p 5000:5000 \
  -v $(pwd)/.env:/app/.env:ro \
  -v $(pwd)/client_secrets.json:/app/client_secrets.json:ro \
  -v youtube-data:/app/data \
  youtube-automation

# Or use Docker Compose (easier)
docker-compose up -d
```

**Pros:**
- 🐳 Complete isolation from host system
- 📦 Consistent environment across all deployments
- ☁️ Easy deployment to cloud platforms
- 🔄 No manual Python/ffmpeg installation
- 🔒 Better security (no sudo required)
- 📊 Easy scaling with orchestration

**Cons:**
- 🐳 Requires Docker installation
- 💾 Slightly larger disk footprint

---

### Method 3: Manual Setup (Advanced Users)

**Best for:** Custom configurations, advanced users, troubleshooting

```bash
# Clone the repository
git clone https://github.com/S3OPS/youtube.git
cd youtube

# Install Python 3.12 manually
# (varies by OS - see https://www.python.org/downloads/)

# Install ffmpeg
# Ubuntu/Debian:
sudo apt-get update && sudo apt-get install -y ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html

# Create virtual environment
python3.12 -m venv .venv

# Activate virtual environment
# Linux/macOS:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Or run interactive wizard
python setup.py

# Add client_secrets.json
# Download from Google Cloud Console

# Run the application
python app.py
```

**Pros:**
- 🎛️ Full control over configuration
- 🔧 Easy to troubleshoot
- 💡 Educational (understand all dependencies)

**Cons:**
- ⏱️ More time-consuming
- 🔄 Manual dependency management
- 💻 OS-specific commands

---

### Method 4: System Service (Production Servers)

**Best for:** Production servers, always-on operation, automatic restart

> **Note:** This is a new improvement we're adding for better production deployment.

```bash
# First, complete setup using Method 1 or 3

# Create systemd service file
sudo nano /etc/systemd/system/youtube-automation.service
```

Add this content:
```ini
[Unit]
Description=YouTube Automation Service
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/youtube
Environment="PATH=/path/to/youtube/.venv/bin"
ExecStart=/path/to/youtube/.venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable youtube-automation
sudo systemctl start youtube-automation

# Check status
sudo systemctl status youtube-automation

# View logs
sudo journalctl -u youtube-automation -f
```

**Pros:**
- 🔄 Automatic restart on failure
- 🚀 Starts on system boot
- 📊 Integrated logging
- 🔒 Runs as specific user

**Cons:**
- 🐧 Linux-specific (systemd)
- 🔧 Requires root access
- 📝 Manual configuration needed

---

## ☁️ Cloud Deployment Options

### AWS (EC2 + Docker)

```bash
# Launch Ubuntu EC2 instance (t2.medium or larger)

# Install Docker
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker ubuntu

# Clone repository
git clone https://github.com/S3OPS/youtube.git
cd youtube

# Create .env and client_secrets.json
nano .env
nano client_secrets.json

# Run with Docker Compose
docker-compose up -d

# Optional: Set up nginx reverse proxy
sudo apt-get install -y nginx
# Configure nginx to proxy port 80 -> 5000
```

### Google Cloud Platform (Cloud Run)

```bash
# Install gcloud CLI
# Configure project and authentication

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT/youtube-automation

# Deploy to Cloud Run
gcloud run deploy youtube-automation \
  --image gcr.io/YOUR_PROJECT/youtube-automation \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="FLASK_PORT=8080"
```

### Heroku

```bash
# Create Heroku app
heroku create youtube-automation

# Add buildpacks
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key
heroku config:set AMAZON_AFFILIATE_TAG=your_tag
# ... (add all .env variables)

# Deploy
git push heroku main

# Open app
heroku open
```

### DigitalOcean (Droplet)

```bash
# Create Ubuntu droplet (2GB RAM minimum)

# SSH into droplet
ssh root@your_droplet_ip

# Run one-command setup
git clone https://github.com/S3OPS/youtube.git
cd youtube
./setup.sh

# Set up as system service (see Method 4)
# Or run with Docker (see Method 2)

# Optional: Set up firewall
ufw allow 22
ufw allow 80
ufw allow 443
ufw enable
```

---

## 🔒 Production Best Practices

### Security Checklist

- [ ] Never commit `.env` or `client_secrets.json` to version control
- [ ] Use strong API keys and rotate regularly
- [ ] Enable HTTPS with SSL/TLS certificate (Let's Encrypt)
- [ ] Set up firewall rules (only expose necessary ports)
- [ ] Run application as non-root user
- [ ] Keep dependencies updated (`pip list --outdated`)
- [ ] Enable rate limiting on Flask endpoints
- [ ] Use environment-specific configurations (dev/staging/prod)
- [ ] Regular backups of `automation_history.json`
- [ ] Monitor logs for suspicious activity

### Performance Tuning

- [ ] Adjust cache settings in `.env` (default: 1 hour TTL, 100MB)
- [ ] Configure worker threads for task queue (default: 4)
- [ ] Use production WSGI server (gunicorn/uWSGI) instead of Flask dev server
- [ ] Set up CDN for static assets
- [ ] Enable gzip compression in reverse proxy
- [ ] Monitor memory usage (video creation can be RAM-intensive)

### Monitoring

```bash
# Set up health check endpoint
curl http://localhost:5000/health

# Monitor logs
tail -f logs/app.log

# Check system resources
htop
df -h
free -m

# Monitor task queue
curl http://localhost:5000/api/tasks
```

---

## 🧪 Verifying Installation

After installation, verify everything works:

```bash
# 1. Check Python version
python --version  # Should be 3.12+

# 2. Check ffmpeg
ffmpeg -version

# 3. Check environment variables
cat .env

# 4. Run tests
python test_integration.py
python test_performance.py
python test_backward_compat.py

# 5. Start web dashboard
python app.py

# 6. Access in browser
curl http://localhost:5000

# 7. Create test video
python create_video.py
```

**Expected output:**
- Web dashboard at `http://localhost:5000`
- Task queue status visible in UI
- No errors in console
- Video creation completes successfully

---

## 🐛 Common Issues & Solutions

### Python Version Issues

**Problem:** `python3.12: command not found`

**Solution:**
```bash
# Use setup.sh which auto-installs Python 3.12
./setup.sh

# Or install manually
# Ubuntu:
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.12 python3.12-venv

# macOS:
brew install python@3.12
```

### ffmpeg Not Found

**Problem:** `ffmpeg: command not found`

**Solution:**
```bash
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html
# Add to PATH
```

### Virtual Environment Issues

**Problem:** Cannot activate virtual environment

**Solution:**
```bash
# Linux/macOS:
source .venv/bin/activate

# Windows Command Prompt:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# If PowerShell execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port Already in Use

**Problem:** `Address already in use: 5000`

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000
# Or on Windows:
netstat -ano | findstr :5000

# Kill the process
kill -9 <PID>

# Or change port in .env
FLASK_PORT=5001
```

### API Key Errors

**Problem:** `OpenAI API key not found` or `Invalid API key`

**Solution:**
```bash
# Verify .env file exists
cat .env

# Check API key format
# Should look like: sk-...
echo $OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

---

## 📊 Comparison: Current vs Improved Setup

| Aspect | Current (setup.sh only) | With Docker & Services | Improvement |
|--------|------------------------|----------------------|-------------|
| **Initial Setup Time** | ~5 minutes | ~3 minutes | 40% faster |
| **Cross-platform** | Good (requires manual steps on Windows) | Excellent (identical on all OS) | ⭐⭐⭐ |
| **Isolation** | System-wide Python | Container isolation | ⭐⭐⭐⭐⭐ |
| **Production Ready** | Requires manual service setup | One command | ⭐⭐⭐⭐ |
| **Cloud Deployment** | Manual configuration | Docker = native support | ⭐⭐⭐⭐⭐ |
| **Dependency Conflicts** | Possible with other Python projects | None (isolated) | ⭐⭐⭐⭐ |
| **Updates** | Manual pip upgrade | Docker rebuild | ⭐⭐⭐ |
| **Scalability** | Single server | Easy horizontal scaling | ⭐⭐⭐⭐⭐ |

---

## 💡 Recommendations

### For Different Use Cases

**Local Development / Testing:**
- ✅ Use **Method 1: One-Command Setup** (`./setup.sh`)
- Fast, easy, interactive
- Perfect for learning and experimentation

**Production Deployment:**
- ✅ Use **Method 2: Docker** + **Method 4: System Service**
- Better isolation, easier deployment
- Professional-grade setup
- Automatic restart on failure

**Cloud Platforms:**
- ✅ Use **Docker** with cloud-native services (Cloud Run, ECS, App Platform)
- Easiest deployment
- Built-in scaling and monitoring

**Shared Server / Team Environment:**
- ✅ Use **Docker** to avoid dependency conflicts
- Each developer gets consistent environment
- No "works on my machine" issues

---

## 🎯 Next Steps After Installation

1. **Configure APIs:**
   - OpenAI API key
   - Amazon Affiliate tag
   - YouTube OAuth credentials

2. **Test the System:**
   - Run `python create_video.py` to create test video
   - Check `http://localhost:5000` for web dashboard

3. **Review Documentation:**
   - [API.md](API.md) - API endpoints
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design
   - [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md) - Tuning

4. **Set Up Automation:**
   - Configure scheduling (daily/weekly)
   - Set up monitoring/alerting
   - Plan content calendar

5. **Production Deployment:**
   - Set up SSL/HTTPS
   - Configure reverse proxy (nginx)
   - Set up backups
   - Enable monitoring

---

## 📞 Support & Resources

- **Documentation:** See `/docs` directory for comprehensive guides
- **Issues:** Check existing GitHub issues for solutions
- **Setup Wizard:** Run `python setup.py` for interactive configuration
- **Troubleshooting:** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Made with ❤️ to make installation and deployment as smooth as possible**
