# Quick Start Guide

Get your automated YouTube content system running in 5 minutes!

## 🚀 Super Fast Setup

### Step 1: Install Dependencies (2 minutes)

```bash
# Clone the repo
git clone https://github.com/S3OPS/youtube.git
cd youtube

# Install Python packages (use Python 3.12 or 3.13)
pip install -r requirements.txt

# Install ffmpeg (choose your OS)
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows: Download from https://ffmpeg.org/download.html
```

### Step 2: Configure (1 minute)

Run the setup wizard:

```bash
python setup.py
```

If you prefer manual setup, copy `.env.example` and fill in the required keys.

### Step 3: YouTube Credentials (1 minute)

Create OAuth credentials in Google Cloud and download `client_secrets.json` to the project root.

### Step 4: Run! (10 seconds)

**Option A: Web Dashboard**
```bash
python app.py
# Open http://localhost:5000
```

**Option B: Create Video Now**
```bash
python create_video.py
```

## 🎉 That's It!

Your first video will be:
1. ✅ Generated with AI
2. ✅ Created with audio and visuals
3. ✅ Enhanced with Amazon affiliate links
4. ✅ Uploaded to YouTube

## 🆘 Common Issues

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed fixes.

## 📚 Next Steps

- Read the full [README.md](README.md) for advanced features
- Customize your content in `.env`
- Set up automated scheduling
- Monitor your dashboard at http://localhost:5000

## 💡 Tips

- Start with `VIDEO_PRIVACY=unlisted` to test
- Review generated videos before making them public

---

**Need help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or open an issue on GitHub!
