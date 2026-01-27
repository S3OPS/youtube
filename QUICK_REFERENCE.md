# 🚀 Quick Reference - Installation Methods

**Choose the best installation method for your needs:**

---

## 🎯 Choose Your Path

```
┌─────────────────────────────────────────────────────────┐
│  What's your goal?                                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📝 Local Development / Testing                         │
│     ➜ Use: ./setup.sh                                  │
│     ⏱️  Time: 5 minutes                                 │
│     📖 Guide: SETUP_GUIDE.md                           │
│                                                         │
│  🐳 Production / Cloud Deployment                       │
│     ➜ Use: Docker                                      │
│     ⏱️  Time: 3 minutes                                 │
│     📖 Guide: INSTALLATION_GUIDE.md                    │
│                                                         │
│  🏢 Production Server (Always-On)                       │
│     ➜ Use: systemd Service                            │
│     ⏱️  Time: 7 minutes                                 │
│     📖 Guide: DEPLOYMENT_GUIDE.md                      │
│                                                         │
│  ☁️  AWS / GCP / Azure / Heroku                        │
│     ➜ Use: Docker                                      │
│     ⏱️  Time: 5 minutes                                 │
│     📖 Guide: INSTALLATION_GUIDE.md (Cloud section)    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## ⚡ Quick Commands

### Method 1: One-Command Setup (Local)
```bash
./setup.sh
python app.py
```

### Method 2: Docker (Production)
```bash
cp .env.example .env  # Edit with your API keys
docker-compose up -d
docker-compose logs -f
```

### Method 3: Manual Setup (Advanced)
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

### Method 4: System Service (Server)
```bash
./setup.sh
sudo cp youtube-automation.service /etc/systemd/system/
sudo systemctl enable --now youtube-automation
sudo systemctl status youtube-automation
```

---

## 📚 Documentation Map

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **INSTALLATION_RECOMMENDATIONS.md** | 👈 **START HERE** - Answers "what should I use?" | First time setup |
| **SETUP_GUIDE.md** | Original quick setup guide | Local development |
| **INSTALLATION_GUIDE.md** | Complete installation reference | All installation options |
| **DEPLOYMENT_GUIDE.md** | Production deployment guide | Production deployment |
| **QUICKSTART.md** | 5-minute quick start | Fastest overview |
| **README.md** | Project overview | Understanding the system |
| **TROUBLESHOOTING.md** | Common issues | When problems occur |
| **API.md** | API reference | Building integrations |
| **ARCHITECTURE.md** | System design | Understanding internals |

---

## ✅ Verification Commands

After installation, verify it works:

```bash
# Check service is running
curl http://localhost:5000/health

# Expected response:
# {"status": "healthy", "timestamp": "...", "version": "1.0.0"}

# Open web dashboard
# Visit: http://localhost:5000

# Create test video
python create_video.py
```

---

## 🆘 Quick Troubleshooting

### "Port 5000 already in use"
```bash
# Change port in .env
FLASK_PORT=5001
```

### "Python 3.12 not found"
```bash
# Use setup.sh which auto-installs it
./setup.sh
```

### "Docker not found"
```bash
# Install Docker
sudo apt-get install docker.io docker-compose
```

### "ffmpeg not found"
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

---

## 🔄 Update Commands

### Update Docker Deployment
```bash
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

### Update Manual Installation
```bash
git pull
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Update System Service
```bash
git pull
sudo systemctl restart youtube-automation
sudo systemctl status youtube-automation
```

---

## 🎓 Recommended Learning Path

**Week 1: Local Development**
1. Run `./setup.sh`
2. Create test videos with `python create_video.py`
3. Explore web dashboard at `http://localhost:5000`
4. Read ARCHITECTURE.md to understand the system

**Week 2: Docker (Optional)**
1. Install Docker
2. Run `docker-compose up -d`
3. Compare with local setup
4. Practice Docker commands

**Week 3: Production (When Ready)**
1. Read DEPLOYMENT_GUIDE.md
2. Set up nginx reverse proxy
3. Configure SSL with Let's Encrypt
4. Set up monitoring and backups

---

## 💡 Pro Tips

1. **Start Simple:** Use `./setup.sh` for local development
2. **Go Docker:** Switch to Docker when deploying to production
3. **Read Docs:** Each guide has specific use cases
4. **Test First:** Try locally before deploying to production
5. **Monitor:** Use `/health` endpoint for monitoring
6. **Backup:** Backup `.env` and `client_secrets.json` files
7. **Update:** Keep dependencies updated regularly

---

## 📞 Support

- **Installation Issues:** See INSTALLATION_GUIDE.md
- **Production Setup:** See DEPLOYMENT_GUIDE.md
- **General Problems:** See TROUBLESHOOTING.md
- **GitHub Issues:** https://github.com/S3OPS/youtube/issues

---

**Quick Start Command:**
```bash
# Clone and run in 2 commands!
git clone https://github.com/S3OPS/youtube.git && cd youtube && ./setup.sh
```

**Production Deploy:**
```bash
# Docker in 3 commands!
git clone https://github.com/S3OPS/youtube.git && cd youtube
cp .env.example .env  # Edit with your keys
docker-compose up -d
```

---

**Made with ❤️ to make installation as simple as possible**
