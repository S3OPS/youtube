# Quick Start Guide

Get your automated YouTube content system running in 5 minutes!

## 🚀 Super Fast Setup

### Step 1: Install Dependencies (2 minutes)

```bash
# Clone the repo
git clone https://github.com/S3OPS/youtube.git
cd youtube

# Install Python packages
pip install -r requirements.txt

# Install ffmpeg (choose your OS)
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows: Download from https://ffmpeg.org/download.html
```

### Step 2: Get API Keys (1 minute)

You need two things:

1. **OpenAI API Key** 
   - Go to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key

2. **Amazon Affiliate Tag**
   - Sign up at https://affiliate-program.amazon.com/
   - Get your affiliate tag (format: `yourname-20`)

### Step 3: Configure (1 minute)

Run the setup wizard:

```bash
python setup.py
```

Or manually create `.env`:

```env
OPENAI_API_KEY=sk-your-key-here
AMAZON_AFFILIATE_TAG=youraffid-20
CONTENT_TOPIC=technology
CONTENT_FREQUENCY=daily
```

### Step 4: YouTube Credentials (1 minute)

1. Go to https://console.cloud.google.com/
2. Create project → Enable "YouTube Data API v3"
3. Create OAuth credentials → Download as `client_secrets.json`
4. Place in project root

### Step 5: Run! (10 seconds)

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

**"ffmpeg not found"**
```bash
# Install ffmpeg first (see Step 1)
ffmpeg -version  # Test if installed
```

**"Invalid OpenAI API key"**
```bash
# Check your key in .env file
# Make sure there are no spaces or quotes
```

**"YouTube upload failed"**
```bash
# Make sure client_secrets.json is in the root directory
# Complete the OAuth flow when prompted
```

## 📚 Next Steps

- Read the full [README.md](README.md) for advanced features
- Customize your content in `.env`
- Set up automated scheduling
- Monitor your dashboard at http://localhost:5000

## 💡 Tips

- Start with `VIDEO_PRIVACY=unlisted` to test
- Check the activity log in the dashboard
- Review generated videos before making them public
- Adjust `CONTENT_TOPIC` to match your niche

---

**Need help?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or open an issue on GitHub!
