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

For step-by-step setup, see [QUICKSTART.md](QUICKSTART.md). In short:

1. Install dependencies and ffmpeg.
2. Configure `.env` (run `python setup.py` or copy `.env.example` and fill in required keys).
3. Add `client_secrets.json` for YouTube API access.
4. Run `python app.py` or `python create_video.py`.

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

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common setup issues and fixes.

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
