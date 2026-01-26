# 🎬 Automated YouTube Content Creation System

A **100% fully automated** content creation system that generates videos with AI, automatically adds Amazon affiliate links, and uploads to YouTube - all from a single-page web interface.

## ✨ Features

- 🤖 **AI-Powered Content Generation** - Uses OpenAI GPT to create engaging video scripts
- 🎥 **Automatic Video Creation** - Generates videos with text-to-speech narration
- 💰 **Amazon Affiliate Integration** - Automatically adds relevant affiliate links to descriptions
- 📤 **YouTube Upload** - Automatically uploads videos to your YouTube channel
- 🖥️ **Single-Page Dashboard** - Beautiful web interface to monitor and control everything
- ⏰ **Scheduled Automation** - Set it and forget it with automated scheduling
- 📊 **Real-time Monitoring** - Track all video creation and upload activity

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Amazon Affiliate account
- YouTube account with API access
- ffmpeg installed (for video creation)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/S3OPS/youtube.git
   cd youtube
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ffmpeg** (required for video creation)
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install ffmpeg
   ```
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **Windows:**
   Download from https://ffmpeg.org/download.html

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

5. **Set up YouTube API credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable YouTube Data API v3
   - Create OAuth 2.0 credentials
   - Download the credentials as `client_secrets.json`
   - Place in the project root directory

### Configuration

Edit `.env` file with your credentials:

```env
# OpenAI API Key (required)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Amazon Affiliate Tag (required)
AMAZON_AFFILIATE_TAG=youraffid-20

# Content Settings
CONTENT_TOPIC=technology
CONTENT_FREQUENCY=daily
VIDEO_DURATION=60

# Server Settings
FLASK_PORT=5000
FLASK_HOST=0.0.0.0
```

## 📖 Usage

### Method 1: Web Dashboard (Recommended)

1. **Start the web server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   ```
   http://localhost:5000
   ```

3. **Use the dashboard to:**
   - Create videos on-demand with one click
   - Monitor video creation status
   - View recent uploads
   - Track success/failure rates

### Method 2: Command Line

Create a single video immediately:

```bash
python create_video.py
```

#### QA Automation Logic (Full-Auto CLI)

The CLI follows a deterministic, fully automated sequence with preflight validation:

1. **Preflight checks**: Verify Python version, ffmpeg availability, required `.env` variables, and `client_secrets.json`.
2. **Generate script**: Use OpenAI to create the narration.
3. **Generate metadata**: Produce title + description, extract affiliate keywords.
4. **Affiliate links**: Append Amazon links + disclosure to the description.
5. **Render video**: Text-to-speech → MP4 generation.
6. **Upload**: Push to YouTube with metadata + privacy settings.
7. **Persist history**: Record results in `automation_history.json`.

#### Potential Failure Points

- **Preflight**: missing `ffmpeg`, `client_secrets.json`, or required `.env` keys.
- **OpenAI**: quota errors or invalid API key.
- **Video render**: MoviePy/ffmpeg issues on PATH or temp file permissions.
- **Upload**: OAuth consent errors or quota limits.

### Method 3: Automated Scheduling

Run the automation on a schedule:

```python
from automation_engine import AutomationEngine
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    'openai_api_key': os.getenv('OPENAI_API_KEY'),
    'amazon_affiliate_tag': os.getenv('AMAZON_AFFILIATE_TAG'),
    'content_topic': 'technology',
    'content_frequency': 'daily',
}

automation = AutomationEngine(config)
automation.schedule_automation(frequency='daily')
```

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Web Dashboard (Flask)                  │
│              Single-page monitoring interface             │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Automation Engine                           │
│         Orchestrates the entire workflow                 │
└──────┬───────┬────────┬──────────────┬──────────────────┘
       │       │        │              │
   ┌───▼──┐ ┌──▼───┐ ┌─▼────┐   ┌─────▼──────┐
   │Content│ │Video │ │Amazon│   │  YouTube   │
   │  Gen  │ │Creator│ │Affiliate│  │  Uploader  │
   └───────┘ └──────┘ └──────┘   └────────────┘
```

## 📁 Project Structure

```
youtube/
├── app.py                    # Flask web application
├── automation_engine.py      # Main automation orchestrator
├── content_generator.py      # AI content generation
├── amazon_affiliate.py       # Affiliate link generator
├── video_creator.py          # Video creation with TTS
├── youtube_uploader.py       # YouTube API integration
├── create_video.py           # Standalone CLI script
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
├── templates/
│   └── index.html           # Web dashboard UI
├── generated_videos/        # Output videos (created automatically)
└── generated_scripts/       # Generated scripts (created automatically)
```

## 🔧 How It Works

1. **Content Generation**
   - AI generates an engaging video script based on your topic
   - Creates SEO-optimized title and description
   - Identifies relevant products for affiliate links

2. **Amazon Affiliate Links**
   - Automatically generates product search links
   - Adds affiliate tag to all links
   - Formats links in video description
   - Includes disclosure statement

3. **Video Creation**
   - Converts script to speech using text-to-speech
   - Creates video with background and title
   - Renders final MP4 video file

4. **YouTube Upload**
   - Authenticates with YouTube API
   - Uploads video with metadata
   - Sets privacy settings
   - Returns video URL

## 🎯 Example Output

**Generated Title:**
```
"Amazing Tech Gadgets You Need in 2024"
```

**Generated Description with Affiliate Links:**
```
Discover the most innovative tech gadgets that will transform your daily life...

🛒 RECOMMENDED PRODUCTS:
1. Smart Home Devices: https://www.amazon.com/s?k=smart+home+devices&tag=youraffid-20
2. Wireless Earbuds: https://www.amazon.com/s?k=wireless+earbuds&tag=youraffid-20
3. Portable Chargers: https://www.amazon.com/s?k=portable+chargers&tag=youraffid-20

💡 As an Amazon Associate, I earn from qualifying purchases.
```

## 🔐 Security & Privacy

- Never commit your `.env` file or API credentials
- `client_secrets.json` is git-ignored for security
- OAuth tokens are stored locally and not shared
- All API calls use secure HTTPS connections

## 🐛 Troubleshooting

**Video creation fails:**
- Ensure ffmpeg is installed: `ffmpeg -version`
- Check that all dependencies are installed

**YouTube upload fails:**
- Verify `client_secrets.json` is in the root directory
- Check that YouTube Data API v3 is enabled
- Ensure you've completed OAuth authentication

**No content generated:**
- Verify your OpenAI API key is valid
- Check your OpenAI API usage/credits
- Review the activity log in the dashboard

## 📝 Customization

### Change Content Topic
Edit `.env`:
```env
CONTENT_TOPIC=fitness
```

### Modify Video Style
Edit `video_creator.py` to customize:
- Background colors
- Text styling
- Video resolution
- Audio settings

### Add More Affiliate Links
Edit `amazon_affiliate.py` to customize:
- Link format
- Number of products
- Product categories

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

- This tool is for educational purposes
- Follow YouTube's Terms of Service
- Follow Amazon Associates Program Operating Agreement
- Ensure you have rights to all content you create
- Always disclose affiliate relationships

## 🎓 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation

---

**Made with ❤️ for automated content creators**
