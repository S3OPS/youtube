# 🎬 Automated YouTube Content Creation System

A **100% fully automated** content creation system that generates videos with AI, automatically adds Amazon affiliate links, and uploads to YouTube - all from a single-page web interface.

## ✨ Features

- 🤖 **AI-Powered Content Generation** - Uses OpenAI GPT-3.5-turbo to create engaging video scripts
- 🎥 **Automatic Video Creation** - Generates videos with text-to-speech narration (gTTS + MoviePy)
- 💰 **Amazon Affiliate Integration** - Automatically adds relevant affiliate links to descriptions
- 📤 **YouTube Upload** - Automatically uploads videos to your YouTube channel via OAuth 2.0
- 🖥️ **Single-Page Dashboard** - Beautiful Flask-based web interface with async task queue
- ⏰ **Scheduled Automation** - Set it and forget it with automated scheduling
- 📊 **Real-time Monitoring** - Track all video creation and upload activity with history persistence
- ⚡ **Performance Optimized** - File-based caching, HTTP connection pooling, and LRU eviction
- 🧪 **Testing Infrastructure** - Integration, performance, and backward compatibility tests

## 🚀 Quick Start

For step-by-step setup, see [SETUP_GUIDE.md](SETUP_GUIDE.md). In short:

1. Run the one-command setup script (installs Python 3.12+ and dependencies): `./setup.sh`
2. Configure `.env` via the interactive wizard (`python setup.py`) or copy from `.env.example`
3. Add `client_secrets.json` for YouTube API access
4. Run `python app.py` (web dashboard) or `python create_video.py` (CLI)

**Requirements:** Python 3.12+, ffmpeg

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
│              Web Dashboard (Flask + Task Queue)          │
│         Single-page interface with async processing      │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Automation Engine                           │
│         Orchestrates the entire workflow                 │
│         (with History Service for persistence)           │
└──────┬───────┬────────┬──────────────┬──────────────────┘
       │       │        │              │
   ┌───▼──┐ ┌──▼───┐ ┌─▼────┐   ┌─────▼──────┐
   │Content│ │Video │ │Amazon│   │  YouTube   │
   │  Gen  │ │Creator│ │Affiliate│  │  Uploader  │
   │(Cached)│ │(gTTS)│ │ Links │   │  (OAuth)   │
   └───┬───┘ └──┬───┘ └──────┘   └─────┬──────┘
       │        │                       │
   ┌───▼────────▼───────────────────────▼──────┐
   │      Core Infrastructure Layer            │
   │  • BaseService (service abstraction)      │
   │  • Logging (structured logging)           │
   │  • Error Handling (decorators)            │
   │  • File Utils (I/O operations)            │
   │  • Cache (file-based + LRU eviction)      │
   └───────────────────────────────────────────┘
```

## 📁 Project Structure

```
youtube/
├── Core Application
│   ├── app.py                    # Flask web application with async task queue
│   ├── automation_engine.py      # Main automation orchestrator
│   ├── content_generator.py      # AI content generation with caching
│   ├── amazon_affiliate.py       # Affiliate link generator
│   ├── video_creator.py          # Video creation with TTS (gTTS + MoviePy)
│   ├── youtube_uploader.py       # YouTube API integration (OAuth 2.0)
│   ├── cache.py                  # File-based caching with LRU eviction
│   ├── config.py                 # Configuration management
│   └── utils.py                  # Utility functions
│
├── Core Infrastructure (core/)
│   ├── base.py                   # Abstract base classes (BaseService, BaseAPIClient)
│   ├── logging.py                # Structured logging system
│   ├── error_handler.py          # Error handling decorators
│   ├── exceptions.py             # Custom exception types
│   └── file_utils.py             # File I/O operations
│
├── Services (services/)
│   ├── task_service.py           # Async task queue management
│   └── history_service.py        # Execution history persistence
│
├── CLI Utilities
│   ├── create_video.py           # Standalone video creation script
│   ├── setup.py                  # Interactive setup wizard
│   └── setup.sh                  # One-command automated setup
│
├── Testing
│   ├── test_integration.py       # Task queue API tests
│   ├── test_performance.py       # Cache optimization tests
│   └── test_backward_compat.py   # Legacy compatibility tests
│
├── Configuration
│   ├── requirements.txt          # Python dependencies (Flask 3.0.0, OpenAI 1.6.1)
│   ├── .env.example              # Environment variable template
│   └── .gitignore                # Git ignore rules
│
├── Templates
│   └── templates/
│       └── index.html            # Web dashboard UI
│
└── Documentation
    ├── README.md                 # This file
    ├── SETUP_GUIDE.md            # Setup instructions
    ├── QUICKSTART.md             # 5-minute quick start
    ├── API.md                    # API reference
    ├── ARCHITECTURE.md           # System architecture
    ├── EXAMPLES.md               # Usage examples
    ├── PERFORMANCE_OPTIMIZATION.md  # Performance guide
    ├── SECURITY.md               # Security best practices
    └── TROUBLESHOOTING.md        # Common issues and solutions
```

## 🔧 How It Works

1. **Content Generation** (with AI & Caching)
   - AI generates an engaging video script based on your topic using GPT-3.5-turbo
   - Creates SEO-optimized title and description
   - Identifies relevant products for affiliate links
   - Results cached to reduce API costs (1-hour TTL, configurable)
   - HTTP connection pooling for improved performance

2. **Amazon Affiliate Links**
   - Automatically generates product search links
   - Adds affiliate tag to all links
   - Formats links in video description
   - Includes FTC compliance disclosure statement

3. **Video Creation** (gTTS + MoviePy)
   - Converts script to speech using Google Text-to-Speech (gTTS)
   - Creates video with background and title using MoviePy
   - Renders final MP4 video file optimized for YouTube

4. **YouTube Upload** (OAuth 2.0)
   - Authenticates with YouTube Data API v3 using OAuth 2.0
   - Uploads video with metadata (title, description, tags)
   - Sets privacy settings (public/unlisted/private)
   - Returns video URL and upload status

5. **Task Queue & Monitoring**
   - Async task queue powered by TaskService
   - Real-time status tracking (queued → processing → completed/failed)
   - History persistence via HistoryService
   - Thread-safe operations with proper locking

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

- Never commit your `.env` file or API credentials to version control
- `client_secrets.json` is automatically git-ignored for security
- OAuth tokens are stored locally and not shared
- All API calls use secure HTTPS connections
- See [SECURITY.md](SECURITY.md) for comprehensive security guidelines and best practices

## 🐛 Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common setup issues and fixes.

**Common Issues:**
- **Python version**: Ensure you have Python 3.12+ installed
- **ffmpeg missing**: Install via `apt-get install ffmpeg` (Linux) or `brew install ffmpeg` (Mac)
- **API key errors**: Check your `.env` file has valid `OPENAI_API_KEY`
- **Cache issues**: Clear cache directory: `rm -rf .cache/`

## 📝 Customization

### Change Content Topic
Edit `.env`:
```env
CONTENT_TOPIC=fitness
```

### Configure AI Model
Edit `.env` to use different OpenAI models:
```env
AI_MODEL=gpt-3.5-turbo  # Default, cost-effective
# AI_MODEL=gpt-4  # Higher quality, higher cost
```

### Adjust Cache Settings
Customize caching behavior in your code:
```python
from cache import SimpleCache

# Custom cache with 2-hour TTL and 200MB limit
cache = SimpleCache(cache_dir='.cache', ttl_seconds=7200, max_size_mb=200)
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

## ⚡ Performance Features

The system includes several performance optimizations:

- **File-based Caching**: Automatic caching of API responses with configurable TTL (default 1 hour)
- **LRU Eviction**: Automatic removal of old cache entries when size limit is reached (default 100MB)
- **HTTP Connection Pooling**: Reused connections to OpenAI API for faster requests
- **Thread-safe Operations**: Proper locking for concurrent web requests
- **Async Task Queue**: Non-blocking video creation via background worker threads

See [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md) for detailed performance tuning guide.

## 🧪 Testing

Run the test suite to verify your setup:

```bash
# Test cache performance optimizations
python test_performance.py

# Test async task queue integration
python test_integration.py

# Test backward compatibility
python test_backward_compat.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

**Development Setup:**
1. Fork the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Make your changes
4. Run tests: `python test_integration.py && python test_performance.py`
5. Submit a pull request

**Code Style:**
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add tests for new features
- Update documentation for user-facing changes

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
