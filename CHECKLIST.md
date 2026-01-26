# Getting Started Checklist

Use this checklist to ensure you have everything set up correctly.

## ☑️ Prerequisites

- [ ] Python 3.8 or higher installed
- [ ] pip package manager available
- [ ] ffmpeg installed on your system
- [ ] Git installed (for cloning)

**Verify:**
```bash
python3 --version  # Should be 3.8+
pip --version
ffmpeg -version
git --version
```

---

## ☑️ Installation

- [ ] Clone the repository
  ```bash
  git clone https://github.com/S3OPS/youtube.git
  cd youtube
  ```

- [ ] Install Python dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Verify all packages installed
  ```bash
  python3 -c "import flask, openai, gtts, moviepy; print('✓ All packages installed')"
  ```

---

## ☑️ API Keys & Credentials

### OpenAI API Key

- [ ] Go to https://platform.openai.com/api-keys
- [ ] Create new secret key
- [ ] Copy the key (starts with `sk-`)
- [ ] Save it securely

### Amazon Affiliate Tag

- [ ] Sign up at https://affiliate-program.amazon.com/
- [ ] Complete account setup
- [ ] Get your affiliate tag (format: `yourname-20`)
- [ ] Save it securely

### YouTube API Credentials

- [ ] Go to https://console.cloud.google.com/
- [ ] Create a new project (or select existing)
- [ ] Enable "YouTube Data API v3"
- [ ] Create OAuth 2.0 Client ID credentials
- [ ] Configure consent screen
- [ ] Download credentials as JSON
- [ ] Rename to `client_secrets.json`
- [ ] Place in project root directory

---

## ☑️ Configuration

### Option 1: Setup Wizard (Recommended)

- [ ] Run the setup wizard
  ```bash
  python setup.py
  ```

- [ ] Follow prompts to enter:
  - OpenAI API key
  - Amazon affiliate tag
  - Content topic
  - Content frequency
  - Video privacy

### Option 2: Manual Configuration

- [ ] Copy the example file
  ```bash
  cp .env.example .env
  ```

- [ ] Edit `.env` file with your values:
  ```env
  OPENAI_API_KEY=sk-your-actual-key-here
  AMAZON_AFFILIATE_TAG=youraffid-20
  CONTENT_TOPIC=technology
  CONTENT_FREQUENCY=daily
  VIDEO_PRIVACY=public
  ```

- [ ] Verify `.env` file exists and has correct values
  ```bash
  cat .env
  ```

---

## ☑️ First Test

### Test 1: Check Dependencies

- [ ] Verify ffmpeg
  ```bash
  ffmpeg -version
  ```

- [ ] Verify Python modules
  ```bash
  python3 setup.py
  ```

### Test 2: Test Content Generation (No Upload)

- [ ] Create a test script (optional - requires OpenAI key)
  ```python
  python3 -c "
  from dotenv import load_dotenv
  import os
  load_dotenv()
  from content_generator import ContentGenerator
  gen = ContentGenerator(os.getenv('OPENAI_API_KEY'), 'technology')
  script = gen.generate_video_script()
  print('✓ Content generation working!')
  print('Script length:', len(script))
  "
  ```

### Test 3: Start Web Dashboard

- [ ] Start the Flask server
  ```bash
  python app.py
  ```

- [ ] Open browser to http://localhost:5000

- [ ] Verify dashboard loads

- [ ] Check that stats show zeros

- [ ] Click "Refresh Status" button

### Test 4: Create First Video (Full Test)

**Option A: Using Web Dashboard**

- [ ] Click "Create & Upload Video Now"
- [ ] Watch activity log for progress
- [ ] Wait for completion (2-5 minutes)
- [ ] Check for success message
- [ ] Verify video appears in "Recent Videos"
- [ ] Click YouTube link to view

**Option B: Using CLI**

- [ ] Run creation script
  ```bash
  python create_video.py
  ```

- [ ] Monitor console output

- [ ] Check for success message

- [ ] Note the YouTube URL

- [ ] Verify video file in `generated_videos/`

---

## ☑️ Verify Output

- [ ] Generated script file exists in `generated_scripts/`

- [ ] Generated video file exists in `generated_videos/`

- [ ] Video uploaded to YouTube successfully

- [ ] Video has title and description

- [ ] Description contains Amazon affiliate links

- [ ] Affiliate links include your tag

- [ ] Video is playable on YouTube

---

## ☑️ Post-Setup

### Security

- [ ] Verify `.env` is in `.gitignore`

- [ ] Verify `client_secrets.json` is in `.gitignore`

- [ ] Never commit API keys to git

- [ ] Keep `token.pickle` local (in `.gitignore`)

### Customization

- [ ] Adjust `CONTENT_TOPIC` if needed

- [ ] Set `VIDEO_PRIVACY` (public/unlisted/private)

- [ ] Configure `CONTENT_FREQUENCY` for scheduling

### Monitoring

- [ ] Bookmark dashboard URL: http://localhost:5000

- [ ] Check `automation_history.json` for logs

- [ ] Monitor YouTube channel for uploads

---

## ☑️ Optional: Scheduling

If you want automated creation:

- [ ] Test manual creation works first

- [ ] Set desired frequency in `.env`

- [ ] Use one of these methods:

**Method 1: Cron Job (Linux/Mac)**
```bash
crontab -e
# Add: 0 9 * * * cd /path/to/youtube && python3 create_video.py
```

**Method 2: Python Scheduler**
```python
from automation_engine import AutomationEngine
automation = AutomationEngine(config)
automation.schedule_automation(frequency='daily')
```

**Method 3: System Service**
- Create a systemd service (Linux)
- Create a launchd service (Mac)
- Use Task Scheduler (Windows)

---

## ✅ Troubleshooting

If something doesn't work, check:

### Common Issues

**"ffmpeg not found"**
- [ ] Install ffmpeg for your OS
- [ ] Verify with `ffmpeg -version`

**"Invalid API key"**
- [ ] Check `.env` file for typos
- [ ] Ensure no quotes around the key
- [ ] Verify key at https://platform.openai.com/api-keys

**"YouTube upload failed"**
- [ ] Verify `client_secrets.json` exists
- [ ] Check file is valid JSON
- [ ] Complete OAuth flow when prompted
- [ ] Check YouTube API is enabled

**"Module not found"**
- [ ] Run `pip install -r requirements.txt`
- [ ] Use virtual environment if needed
- [ ] Check Python version (3.8+)

**Video creation is slow**
- [ ] This is normal (2-5 minutes per video)
- [ ] AI generation takes time
- [ ] Video rendering requires processing
- [ ] YouTube upload depends on connection

### Getting Help

- [ ] Check the documentation:
  - [README.md](README.md) - Main docs
  - [QUICKSTART.md](QUICKSTART.md) - Quick start
  - [API.md](API.md) - API reference
  - [EXAMPLES.md](EXAMPLES.md) - Usage examples
  - [ARCHITECTURE.md](ARCHITECTURE.md) - System design

- [ ] Review the activity log in dashboard

- [ ] Check console output for errors

- [ ] Open an issue on GitHub

---

## 🎉 Success!

Once all items are checked:

✅ Your automated YouTube content system is ready!

You can now:
- Create videos on demand
- Schedule automatic uploads
- Monitor from the dashboard
- Earn from Amazon affiliate links

**Next Steps:**
1. Create your first few videos
2. Review and refine your content topic
3. Set up scheduling if desired
4. Monitor your YouTube analytics
5. Track affiliate link performance

---

**Pro Tips:**

💡 Start with `VIDEO_PRIVACY=unlisted` for testing

💡 Review generated content before making it public

💡 Monitor your OpenAI API usage/costs

💡 Check YouTube upload quotas (10,000/day)

💡 Track which topics perform best

💡 Adjust content based on audience feedback

---

Enjoy your automated content creation system! 🚀
