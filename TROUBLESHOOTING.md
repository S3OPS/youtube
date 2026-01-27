# Troubleshooting Guide

Common issues and their solutions.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Configuration Issues](#configuration-issues)
- [Content Generation Issues](#content-generation-issues)
- [Video Creation Issues](#video-creation-issues)
- [YouTube Upload Issues](#youtube-upload-issues)
- [Web Dashboard Issues](#web-dashboard-issues)
- [Performance Issues](#performance-issues)

---

## Installation Issues

### Python Version Error

**Problem:** "Python 3.12 or 3.13 is required"

**Solution:**
```bash
# Check your Python version
python3 --version

# Install Python 3.12 or 3.13 if needed (Pillow/lxml wheels are not available for 3.14 yet)
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install python3.12

# macOS:
brew install python@3.12

# Windows: Download from python.org
```

### Package Installation Fails

**Problem:** `pip install -r requirements.txt` fails

**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Try installing one by one to find the problematic package
pip install flask
pip install openai
pip install google-api-python-client
# etc.

# Use virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### ffmpeg Not Found

**Problem:** "ffmpeg: command not found"

**Solution:**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg

# Verify installation
ffmpeg -version
```

**macOS:**
```bash
brew install ffmpeg

# If brew is not installed:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install ffmpeg
```

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to PATH
4. Restart terminal and verify: `ffmpeg -version`

---

## Configuration Issues

### Missing .env File

**Problem:** "Environment variable not found"

**Solution:**
```bash
# Create .env from example
cp .env.example .env

# Or run setup wizard
python setup.py
```

### Invalid OpenAI API Key

**Problem:** "Invalid API key" or "Authentication failed"

**Solution:**
1. Check your key at https://platform.openai.com/api-keys
2. Ensure key starts with `sk-`
3. Make sure there are no spaces or quotes in `.env`:
   ```env
   # Wrong:
   OPENAI_API_KEY="sk-..."
   OPENAI_API_KEY = sk-...
   
   # Correct:
   OPENAI_API_KEY=sk-...
   ```
4. Verify you have credits/billing set up

### Amazon Affiliate Tag Issues

**Problem:** Links don't include affiliate tag

**Solution:**
```bash
# Check .env file
cat .env | grep AMAZON_AFFILIATE_TAG

# Should be format: yourname-20
# Example: mystore-20

# Update if needed
AMAZON_AFFILIATE_TAG=yourname-20
```

---

## Content Generation Issues

### OpenAI API Errors

**Problem:** "Rate limit exceeded" or "Insufficient quota"

**Solutions:**

**Rate Limit:**
- Wait a few seconds and try again
- Reduce frequency of requests
- Upgrade OpenAI plan

**Insufficient Quota:**
- Add payment method at https://platform.openai.com/billing
- Check usage at https://platform.openai.com/usage
- Top up credits

### Low-Quality Content

**Problem:** Generated scripts are poor quality

**Solutions:**
1. Adjust content topic to be more specific:
   ```env
   # Instead of:
   CONTENT_TOPIC=technology
   
   # Try:
   CONTENT_TOPIC=latest smartphone reviews
   ```

2. Modify prompt in `content_generator.py`:
   ```python
   prompt = f"""Create a highly engaging YouTube video script about {topic}.
   Focus on providing value and entertainment.
   Include specific examples and actionable advice.
   """
   ```

### Content Too Short/Long

**Problem:** Videos are wrong length

**Solution:**

Edit `content_generator.py`:
```python
# Change max_tokens for longer/shorter content
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[...],
    max_tokens=800,  # Increase for longer, decrease for shorter
    temperature=0.8
)
```

---

## Video Creation Issues

### Text-to-Speech Fails

**Problem:** "Error creating audio" or gTTS error

**Solutions:**

**Network Issue:**
```bash
# Test internet connection
ping google.com

# Try alternative TTS if needed
# Install pyttsx3 (offline TTS):
pip install pyttsx3
```

**Rate Limit:**
- Wait a few seconds
- gTTS has usage limits
- Consider upgrading to paid TTS service

### Video Rendering Fails

**Problem:** MoviePy errors or video creation fails

**Solutions:**

**Missing ffmpeg:**
```bash
# Verify ffmpeg
ffmpeg -version

# Reinstall if needed
```

**Insufficient Memory:**
```bash
# Check available memory
free -h  # Linux
vm_stat  # macOS

# Reduce video quality in video_creator.py:
final_video.write_videofile(
    output_file,
    fps=24,  # Reduce from 30
    codec='libx264',
    bitrate='500k'  # Add this to reduce size
)
```

**Font Issues (Text Overlay):**
```python
# If TextClip fails, video_creator falls back to simple mode
# This is normal and expected
# Video will be created without text overlay
```

### Video Quality Issues

**Problem:** Videos look poor quality

**Solution:**

Edit `video_creator.py`:
```python
# Increase resolution
img = Image.new('RGB', (1920, 1080), color)  # Already at max

# Increase bitrate
final_video.write_videofile(
    output_file,
    fps=30,  # Increase from 24
    codec='libx264',
    bitrate='5000k'  # Higher bitrate
)
```

---

## YouTube Upload Issues

### Missing client_secrets.json

**Problem:** "client_secrets.json not found"

**Solution:**
1. Go to https://console.cloud.google.com/
2. Select your project
3. APIs & Services → Credentials
4. Download OAuth 2.0 Client ID as JSON
5. Rename to `client_secrets.json`
6. Place in project root (same directory as `app.py`)

### OAuth Authentication Fails

**Problem:** Browser doesn't open or authentication fails

**Solutions:**

**Firewall/Headless Server:**
```python
# Manually set redirect URI in client_secrets.json
# Use urn:ietf:wg:oauth:2.0:oob for manual entry
```

**Port Issues:**
```bash
# Check if port is available
lsof -i :8080  # Or whatever port OAuth uses
```

**Clear Old Tokens:**
```bash
# Remove old authentication
rm token.pickle

# Re-authenticate
python create_video.py
```

### YouTube API Quota Exceeded

**Problem:** "Quota exceeded" error

**Solutions:**

**Check Quota:**
1. Go to https://console.cloud.google.com/
2. APIs & Services → YouTube Data API v3
3. Check quota usage

**Quota Limits:**
- Default: 10,000 units/day
- Upload: 1,600 units each
- Maximum: ~6 videos per day with default quota

**Increase Quota:**
1. Request quota increase from Google
2. Or wait until quota resets (midnight Pacific Time)

### Upload Fails Silently

**Problem:** No error but video not on YouTube

**Solutions:**

**Check Privacy Settings:**
```python
# Make sure video isn't private and you're looking at right channel
privacy_status='public'  # or 'unlisted' for testing
```

**Verify Channel Access:**
```bash
# Make sure OAuth credentials have correct channel access
# Re-authenticate if needed
rm token.pickle
python create_video.py
```

**Check Video File:**
```bash
# Verify video file exists and is valid
ls -lh generated_videos/
ffmpeg -i generated_videos/video_*.mp4
```

---

## Web Dashboard Issues

### Dashboard Won't Load

**Problem:** "Connection refused" or page doesn't load

**Solutions:**

**Check Server:**
```bash
# Verify server is running
python app.py

# Check the output for errors
# Should see: "Running on http://0.0.0.0:5000"
```

**Check Port:**
```bash
# See if port is in use
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Use different port
FLASK_PORT=8080 python app.py
```

**Check Firewall:**
```bash
# Allow port through firewall
sudo ufw allow 5000  # Linux
```

### Stats Not Updating

**Problem:** Dashboard shows old data

**Solutions:**

**Refresh Manually:**
- Click "Refresh Status" button
- Hard refresh browser: Ctrl+Shift+R (Cmd+Shift+R on Mac)

**Check History File:**
```bash
# Verify history file exists and is valid
cat automation_history.json
```

**Clear Browser Cache:**
- Open DevTools (F12)
- Disable cache
- Refresh page

### Create Button Doesn't Work

**Problem:** "Create & Upload Video Now" does nothing

**Solutions:**

**Check Browser Console:**
1. Open DevTools (F12)
2. Go to Console tab
3. Look for JavaScript errors

**Check Server Logs:**
- Look at terminal where `python app.py` is running
- Check for Python errors

**API Endpoint Test:**
```bash
# Test API directly
curl -X POST http://localhost:5000/api/create
```

---

## Performance Issues

### Video Creation Too Slow

**Problem:** Takes 10+ minutes per video

**Solutions:**

**Normal Times:**
- 2-5 minutes is normal
- AI generation: 10-30 seconds
- Video rendering: 1-3 minutes
- YouTube upload: 30-60 seconds

**Optimization:**
```python
# Use faster video creation method
video_file = creator.create_simple_video(script, title)

# Reduce video quality slightly
fps=24  # Instead of 30
```

### High Memory Usage

**Problem:** System running out of memory

**Solutions:**

```bash
# Monitor memory
top  # Linux/Mac
taskmgr  # Windows

# Close other applications
# Reduce video quality
# Process videos one at a time (don't batch)
```

### API Calls Too Slow

**Problem:** OpenAI API is slow

**Solutions:**

**Use Faster Model:**
```python
# In content_generator.py
model="gpt-3.5-turbo"  # Faster than gpt-4
```

**Reduce Token Count:**
```python
max_tokens=300  # Reduce from 500
```

**Check Network:**
```bash
# Test connection speed
ping platform.openai.com
```

---

## General Debugging

### Enable Debug Mode

**Flask App:**
```python
# In app.py
app.run(host=host, port=port, debug=True)
```

**Detailed Logging:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs

**Automation History:**
```bash
cat automation_history.json | python -m json.tool
```

**Generated Scripts:**
```bash
ls -la generated_scripts/
cat generated_scripts/script_*.txt
```

**Generated Videos:**
```bash
ls -lh generated_videos/
ffprobe generated_videos/video_*.mp4
```

### Test Components Individually

**Test Content Generation:**
```python
python -c "
from content_generator import ContentGenerator
gen = ContentGenerator('your-api-key', 'tech')
script = gen.generate_video_script()
print(script)
"
```

**Test Video Creation:**
```python
python -c "
from video_creator import VideoCreator
creator = VideoCreator()
video = creator.create_simple_video('Test script here', 'Test Title')
print(video)
"
```

**Test Amazon Links:**
```python
python -c "
from amazon_affiliate import AmazonAffiliate
amazon = AmazonAffiliate('youraffid-20')
link = amazon.generate_search_link('headphones')
print(link)
"
```

---

## Still Having Issues?

1. **Check Documentation:**
   - [README.md](README.md)
   - [QUICKSTART.md](QUICKSTART.md)
   - [EXAMPLES.md](EXAMPLES.md)

2. **Search Issues:**
   - Check GitHub issues
   - Search for error message

3. **Create Issue:**
   - Go to GitHub repository
   - Click "Issues" → "New Issue"
   - Provide:
     - Error message
     - Steps to reproduce
     - System info (OS, Python version)
     - Relevant logs

4. **Community Help:**
   - Stack Overflow
   - Reddit communities
   - Discord servers

---

**Remember:** Most issues are due to missing dependencies, incorrect configuration, or API quota limits. Double-check these first!
