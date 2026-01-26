# API Documentation

## Web API Endpoints

The Flask application provides a RESTful API for programmatic control of the automation system.

Base URL: `http://localhost:5000`

---

## Endpoints

### GET /

**Description:** Render the web dashboard UI

**Response:** HTML page

**Example:**
```bash
curl http://localhost:5000/
```

---

### GET /api/status

**Description:** Get current system status and statistics

**Response:**
```json
{
  "total_videos": 5,
  "successful": 4,
  "failed": 1,
  "last_run": {
    "timestamp": "2024-01-26T10:30:00",
    "status": "success",
    "title": "Amazing Tech Gadgets",
    "video_id": "dQw4w9WgXcQ"
  },
  "config": {
    "topic": "technology",
    "frequency": "daily"
  }
}
```

**Example:**
```bash
curl http://localhost:5000/api/status
```

**Python Example:**
```python
import requests

response = requests.get('http://localhost:5000/api/status')
data = response.json()
print(f"Total videos: {data['total_videos']}")
```

---

### GET /api/history

**Description:** Get complete automation history

**Response:**
```json
{
  "history": [
    {
      "timestamp": "2024-01-26T10:30:00",
      "status": "success",
      "title": "Amazing Tech Gadgets",
      "video_id": "dQw4w9WgXcQ",
      "video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
      "keywords": ["tech gadgets", "electronics"],
      "script_file": "generated_scripts/script_20240126.txt",
      "video_file": "generated_videos/video_20240126.mp4"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:5000/api/history
```

**Python Example:**
```python
import requests

response = requests.get('http://localhost:5000/api/history')
history = response.json()['history']

for entry in history:
    print(f"{entry['title']} - {entry['status']}")
```

---

### POST /api/create

**Description:** Trigger immediate video creation and upload

**Request Body:** None required

**Response (Success):**
```json
{
  "timestamp": "2024-01-26T10:30:00",
  "status": "success",
  "title": "Amazing Tech Gadgets",
  "video_id": "dQw4w9WgXcQ",
  "video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
  "keywords": ["tech gadgets", "electronics"],
  "description": "Full video description with affiliate links...",
  "script_file": "generated_scripts/script_20240126.txt",
  "video_file": "generated_videos/video_20240126.mp4"
}
```

**Response (Failure):**
```json
{
  "timestamp": "2024-01-26T10:30:00",
  "status": "failed",
  "error": "Failed to generate script"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/create
```

**Python Example:**
```python
import requests
import time

# Trigger video creation
response = requests.post('http://localhost:5000/api/create')
result = response.json()

if result['status'] == 'success':
    print(f"✓ Video created: {result['video_url']}")
else:
    print(f"✗ Failed: {result.get('error')}")
```

**Note:** This endpoint may take several minutes to complete as it performs the entire video creation and upload workflow.

---

### GET /api/config

**Description:** Get current configuration

**Response:**
```json
{
  "openai_api_key": "sk-...",
  "amazon_affiliate_tag": "youraffid-20",
  "content_topic": "technology",
  "content_frequency": "daily",
  "video_output_dir": "generated_videos",
  "youtube_client_secrets": "client_secrets.json",
  "video_privacy": "public"
}
```

**Example:**
```bash
curl http://localhost:5000/api/config
```

**Note:** API key is partially redacted in response.

---

### POST /api/config

**Description:** Update configuration settings

**Request Body:**
```json
{
  "content_topic": "fitness",
  "content_frequency": "weekly"
}
```

**Response:**
```json
{
  "status": "success",
  "config": {
    "content_topic": "fitness",
    "content_frequency": "weekly",
    ...
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/config \
  -H "Content-Type: application/json" \
  -d '{"content_topic": "fitness"}'
```

**Python Example:**
```python
import requests

new_config = {
    "content_topic": "fitness",
    "content_frequency": "weekly"
}

response = requests.post(
    'http://localhost:5000/api/config',
    json=new_config
)

print(response.json())
```

---

## Python SDK

For advanced programmatic control, you can import the modules directly:

### Example: Direct Automation Control

```python
from automation_engine import AutomationEngine
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize
config = {
    'openai_api_key': os.getenv('OPENAI_API_KEY'),
    'amazon_affiliate_tag': os.getenv('AMAZON_AFFILIATE_TAG'),
    'content_topic': 'technology',
}

automation = AutomationEngine(config)

# Create a video
result = automation.create_and_upload_video()
print(result)

# Get status
status = automation.get_status()
print(f"Total videos: {status['total_videos']}")
```

### Example: Custom Content Generation

```python
from content_generator import ContentGenerator

# Initialize
gen = ContentGenerator(
    api_key="your_openai_key",
    topic="fitness"
)

# Generate script
script = gen.generate_video_script()
print(script)

# Generate metadata
title, description = gen.generate_title_and_description(script)
print(f"Title: {title}")

# Generate keywords
keywords = gen.generate_product_keywords(script)
print(f"Keywords: {keywords}")
```

### Example: Amazon Affiliate Links

```python
from amazon_affiliate import AmazonAffiliate

# Initialize
affiliate = AmazonAffiliate(affiliate_tag="youraffid-20")

# Generate search link
link = affiliate.generate_search_link("wireless earbuds")
print(link)
# Output: https://www.amazon.com/s?k=wireless+earbuds&tag=youraffid-20

# Generate product link
product_link = affiliate.generate_product_link("B08X1234ABC")
print(product_link)
# Output: https://www.amazon.com/dp/B08X1234ABC?tag=youraffid-20

# Format description
keywords = ["wireless earbuds", "phone case", "charger"]
description = "Great video about tech..."
full_description = affiliate.format_description_with_links(
    description, 
    keywords
)
print(full_description)
```

### Example: Video Creation

```python
from video_creator import VideoCreator

# Initialize
creator = VideoCreator(output_dir="my_videos")

# Create video from script
script = "Your video script here..."
title = "My Amazing Video"

video_file = creator.create_simple_video(script, title)
print(f"Video created: {video_file}")
```

### Example: YouTube Upload

```python
from youtube_uploader import YouTubeUploader

# Initialize
uploader = YouTubeUploader(
    client_secrets_file='client_secrets.json'
)

# Authenticate
uploader.authenticate()

# Upload video
video_id = uploader.upload_video(
    video_file="path/to/video.mp4",
    title="My Video Title",
    description="Video description with links...",
    tags=["tech", "gadgets"],
    privacy_status="public"
)

print(f"Uploaded! Video ID: {video_id}")
print(f"URL: https://youtube.com/watch?v={video_id}")
```

---

## Error Responses

All endpoints may return error responses:

**Format:**
```json
{
  "error": "Error message describing what went wrong"
}
```

**HTTP Status Codes:**
- `200` - Success
- `500` - Internal server error

---

## Rate Limiting

Currently, there is no rate limiting on the API. However, external APIs have their own limits:

- **OpenAI API:** Based on your plan
- **YouTube API:** 10,000 quota units per day (upload = 1,600 units)
- **gTTS:** No official limit, but use responsibly

---

## Webhooks (Future Feature)

Future versions may support webhooks to notify external systems when videos are created:

```json
{
  "event": "video_created",
  "data": {
    "video_id": "dQw4w9WgXcQ",
    "title": "Amazing Tech Gadgets",
    "url": "https://youtube.com/watch?v=dQw4w9WgXcQ"
  }
}
```

---

## Testing the API

### Using cURL

```bash
# Get status
curl http://localhost:5000/api/status

# Create video
curl -X POST http://localhost:5000/api/create

# Update config
curl -X POST http://localhost:5000/api/config \
  -H "Content-Type: application/json" \
  -d '{"content_topic": "fitness"}'
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:5000"

# Get status
response = requests.get(f"{BASE_URL}/api/status")
print(response.json())

# Create video
response = requests.post(f"{BASE_URL}/api/create")
print(response.json())

# Update config
response = requests.post(
    f"{BASE_URL}/api/config",
    json={"content_topic": "fitness"}
)
print(response.json())
```

### Using JavaScript/Fetch

```javascript
// Get status
fetch('http://localhost:5000/api/status')
  .then(response => response.json())
  .then(data => console.log(data));

// Create video
fetch('http://localhost:5000/api/create', {
  method: 'POST'
})
  .then(response => response.json())
  .then(data => console.log(data));

// Update config
fetch('http://localhost:5000/api/config', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    content_topic: 'fitness'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

---

For more examples, see the [README.md](README.md) or check the source code.
