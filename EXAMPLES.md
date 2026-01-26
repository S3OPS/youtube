# Usage Examples

This document provides practical examples for using the Automated YouTube Content Creation System.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Customization](#customization)
3. [Scheduling](#scheduling)
4. [Integration Examples](#integration-examples)
5. [Advanced Workflows](#advanced-workflows)

---

## Basic Usage

### Example 1: Create Your First Video

```bash
# Make sure .env is configured
python create_video.py
```

**Expected Output:**
```
Starting automated content creation...
Step 1: Generating video script...
Script generated (450 characters)
Step 2: Generating title and description...
Title: Top 5 Tech Gadgets That Will Change Your Life
Step 3: Generating Amazon affiliate links...
Keywords: smart watch, wireless earbuds, portable charger
Step 4: Creating video...
Video created: generated_videos/video_20240126_103000.mp4
Step 5: Uploading to YouTube...
Video uploaded successfully! Video ID: dQw4w9WgXcQ
✓ Success! Video uploaded: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Example 2: Using the Web Dashboard

```bash
# Start the server
python app.py

# Open browser to http://localhost:5000
# Click "Create & Upload Video Now"
# Monitor progress in real-time
```

---

## Customization

### Example 3: Custom Topic

Create videos about fitness instead of technology:

```python
# Option 1: Update .env file
# CONTENT_TOPIC=fitness

# Option 2: Programmatically
from automation_engine import AutomationEngine

config = {
    'openai_api_key': 'your_key',
    'amazon_affiliate_tag': 'youraffid-20',
    'content_topic': 'fitness',  # Custom topic
}

automation = AutomationEngine(config)
result = automation.create_and_upload_video()
```

### Example 4: Generate Multiple Videos

```python
from automation_engine import AutomationEngine
import os
from dotenv import load_dotenv

load_dotenv()

topics = ['fitness', 'cooking', 'gaming', 'travel']

config = {
    'openai_api_key': os.getenv('OPENAI_API_KEY'),
    'amazon_affiliate_tag': os.getenv('AMAZON_AFFILIATE_TAG'),
}

for topic in topics:
    print(f"\n Creating video about {topic}...")
    config['content_topic'] = topic
    automation = AutomationEngine(config)
    result = automation.create_and_upload_video()
    
    if result['status'] == 'success':
        print(f"✓ {topic}: {result['video_url']}")
    else:
        print(f"✗ {topic} failed")
```

### Example 5: Custom Video Privacy Settings

```python
from automation_engine import AutomationEngine

# Create unlisted videos for testing
config = {
    'openai_api_key': 'your_key',
    'amazon_affiliate_tag': 'youraffid-20',
    'content_topic': 'technology',
    'video_privacy': 'unlisted',  # or 'private' or 'public'
}

automation = AutomationEngine(config)
automation.create_and_upload_video()
```

---

## Scheduling

### Example 6: Daily Automation

```python
from automation_engine import AutomationEngine
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    'openai_api_key': os.getenv('OPENAI_API_KEY'),
    'amazon_affiliate_tag': os.getenv('AMAZON_AFFILIATE_TAG'),
    'content_topic': 'technology',
}

automation = AutomationEngine(config)

# Run daily at 9 AM
automation.schedule_automation(frequency='daily')
```

### Example 7: Custom Schedule with Python Schedule

```python
import schedule
import time
from automation_engine import AutomationEngine

automation = AutomationEngine(config)

# Every Monday at 10 AM
schedule.every().monday.at("10:00").do(
    automation.create_and_upload_video
)

# Every day at 2 PM
schedule.every().day.at("14:00").do(
    automation.create_and_upload_video
)

# Every 6 hours
schedule.every(6).hours.do(
    automation.create_and_upload_video
)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Example 8: Cron Job (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add these lines:

# Every day at 9 AM
0 9 * * * cd /path/to/youtube && /usr/bin/python3 create_video.py

# Every Monday at 10 AM
0 10 * * 1 cd /path/to/youtube && /usr/bin/python3 create_video.py

# Every 6 hours
0 */6 * * * cd /path/to/youtube && /usr/bin/python3 create_video.py
```

---

## Integration Examples

### Example 9: Webhook Integration

Send notification to Slack when video is created:

```python
from automation_engine import AutomationEngine
import requests

def send_slack_notification(video_url, title):
    webhook_url = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    
    message = {
        "text": f"🎥 New video uploaded!\n*{title}*\n{video_url}"
    }
    
    requests.post(webhook_url, json=message)

# Create video
config = {...}
automation = AutomationEngine(config)
result = automation.create_and_upload_video()

# Send notification
if result['status'] == 'success':
    send_slack_notification(
        result['video_url'],
        result['title']
    )
```

### Example 10: Email Notification

```python
import smtplib
from email.mime.text import MIMEText
from automation_engine import AutomationEngine

def send_email_notification(video_url, title):
    sender = "your-email@gmail.com"
    recipient = "recipient@example.com"
    
    msg = MIMEText(f"New video uploaded!\n\nTitle: {title}\nURL: {video_url}")
    msg['Subject'] = 'New YouTube Video Published'
    msg['From'] = sender
    msg['To'] = recipient
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, 'your-app-password')
        smtp.send_message(msg)

# Use after video creation
automation = AutomationEngine(config)
result = automation.create_and_upload_video()

if result['status'] == 'success':
    send_email_notification(result['video_url'], result['title'])
```

### Example 11: Save to Database

```python
import sqlite3
from automation_engine import AutomationEngine
from datetime import datetime

# Create database
conn = sqlite3.connect('videos.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS videos
    (id INTEGER PRIMARY KEY, title TEXT, video_url TEXT, 
     created_at TEXT, status TEXT)
''')
conn.commit()

# Create video
automation = AutomationEngine(config)
result = automation.create_and_upload_video()

# Save to database
c.execute(
    'INSERT INTO videos (title, video_url, created_at, status) VALUES (?, ?, ?, ?)',
    (result.get('title'), result.get('video_url'), 
     datetime.now().isoformat(), result.get('status'))
)
conn.commit()
conn.close()
```

---

## Advanced Workflows

### Example 12: A/B Testing Different Topics

```python
from automation_engine import AutomationEngine
import random

topics = ['technology', 'gadgets', 'software', 'hardware']

config = {
    'openai_api_key': 'your_key',
    'amazon_affiliate_tag': 'youraffid-20',
}

# Create 10 videos with random topics
for i in range(10):
    topic = random.choice(topics)
    config['content_topic'] = topic
    
    automation = AutomationEngine(config)
    result = automation.create_and_upload_video()
    
    print(f"Video {i+1}: {topic} - {result['status']}")
```

### Example 13: Trending Topics Integration

```python
import requests
from automation_engine import AutomationEngine

def get_trending_topic():
    # Example: Get trending tech topics from an API
    # Replace with your actual trending topics source
    return "AI and Machine Learning"

config = {
    'openai_api_key': 'your_key',
    'amazon_affiliate_tag': 'youraffid-20',
}

# Use trending topic
trending = get_trending_topic()
config['content_topic'] = trending

automation = AutomationEngine(config)
result = automation.create_and_upload_video()
```

### Example 14: Quality Check Before Upload

```python
from automation_engine import AutomationEngine
from content_generator import ContentGenerator
from video_creator import VideoCreator

# Step 1: Generate content
gen = ContentGenerator(api_key='your_key')
script = gen.generate_video_script(topic='technology')

# Step 2: Manual review
print("Script:")
print(script)
print("\nApprove this script? (y/n)")
approval = input()

if approval.lower() == 'y':
    # Step 3: Create and upload
    title, desc = gen.generate_title_and_description(script)
    creator = VideoCreator()
    video_file = creator.create_simple_video(script, title)
    
    # Upload to YouTube
    from youtube_uploader import YouTubeUploader
    uploader = YouTubeUploader()
    uploader.authenticate()
    video_id = uploader.upload_video(video_file, title, desc)
    print(f"Uploaded: https://youtube.com/watch?v={video_id}")
else:
    print("Script rejected. Generating new one...")
```

### Example 15: Batch Processing with Error Handling

```python
from automation_engine import AutomationEngine
import time

topics = ['tech', 'fitness', 'cooking', 'travel', 'finance']
results = []

config = {
    'openai_api_key': 'your_key',
    'amazon_affiliate_tag': 'youraffid-20',
}

for topic in topics:
    try:
        print(f"\nProcessing: {topic}")
        config['content_topic'] = topic
        automation = AutomationEngine(config)
        result = automation.create_and_upload_video()
        results.append(result)
        
        # Wait between uploads to avoid rate limits
        time.sleep(60)
        
    except Exception as e:
        print(f"Error with {topic}: {e}")
        results.append({'topic': topic, 'status': 'error', 'error': str(e)})

# Summary
print("\n=== Summary ===")
successful = [r for r in results if r.get('status') == 'success']
print(f"Successful: {len(successful)}/{len(topics)}")
for r in successful:
    print(f"  ✓ {r.get('title')}")
```

### Example 16: API Server Integration

```python
from flask import Flask, request, jsonify
from automation_engine import AutomationEngine
import threading

app = Flask(__name__)

@app.route('/create', methods=['POST'])
def create_video_endpoint():
    data = request.json
    topic = data.get('topic', 'technology')
    
    # Run in background thread
    def background_task():
        config = {
            'openai_api_key': 'your_key',
            'amazon_affiliate_tag': 'youraffid-20',
            'content_topic': topic,
        }
        automation = AutomationEngine(config)
        result = automation.create_and_upload_video()
        # Here you could send a callback or save to database
    
    thread = threading.Thread(target=background_task)
    thread.start()
    
    return jsonify({'status': 'processing', 'topic': topic})

if __name__ == '__main__':
    app.run(port=8000)
```

**Usage:**
```bash
curl -X POST http://localhost:8000/create \
  -H "Content-Type: application/json" \
  -d '{"topic": "fitness"}'
```

---

## Performance Tips

### Example 17: Optimized Batch Processing

```python
from multiprocessing import Pool
from automation_engine import AutomationEngine

def create_video(topic):
    config = {
        'openai_api_key': 'your_key',
        'amazon_affiliate_tag': 'youraffid-20',
        'content_topic': topic,
    }
    automation = AutomationEngine(config)
    return automation.create_and_upload_video()

topics = ['tech', 'fitness', 'cooking', 'travel']

# Process in parallel (be careful with API rate limits!)
with Pool(processes=2) as pool:
    results = pool.map(create_video, topics)

for result in results:
    print(f"{result.get('title')}: {result.get('status')}")
```

---

For more information, see:
- [README.md](README.md) - Main documentation
- [API.md](API.md) - API reference
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
