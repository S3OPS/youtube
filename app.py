"""
Flask Web Application
Provides a single-page dashboard for the automated content system
"""

from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv
from automation_engine import AutomationEngine
import threading

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize automation engine
config = {
    'openai_api_key': os.getenv('OPENAI_API_KEY'),
    'amazon_affiliate_tag': os.getenv('AMAZON_AFFILIATE_TAG', 'youraffid-20'),
    'content_topic': os.getenv('CONTENT_TOPIC', 'technology'),
    'content_frequency': os.getenv('CONTENT_FREQUENCY', 'daily'),
    'video_output_dir': 'generated_videos',
    'youtube_client_secrets': 'client_secrets.json',
    'video_privacy': os.getenv('VIDEO_PRIVACY', 'public')
}

automation = AutomationEngine(config)


@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('index.html')


@app.route('/api/status')
def get_status():
    """Get current automation status"""
    try:
        status = automation.get_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history')
def get_history():
    """Get automation history"""
    try:
        return jsonify({'history': automation.history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/create', methods=['POST'])
def create_video():
    """Trigger video creation"""
    try:
        # Run in a separate thread to avoid blocking
        def run_creation():
            return automation.create_and_upload_video()
        
        result = run_creation()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'status': 'failed',
            'error': str(e)
        }), 500


@app.route('/api/config', methods=['GET', 'POST'])
def manage_config():
    """Get or update configuration"""
    if request.method == 'GET':
        return jsonify(config)
    else:
        try:
            data = request.json
            # Update config
            for key in ['content_topic', 'content_frequency']:
                if key in data:
                    config[key] = data[key]
            return jsonify({'status': 'success', 'config': config})
        except Exception as e:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    
    print(f"""
{'='*60}
🎬 Automated YouTube Content System
{'='*60}

Dashboard URL: http://{host}:{port}

Features:
✓ AI-powered content generation
✓ Automatic video creation
✓ Amazon affiliate link integration
✓ YouTube upload automation
✓ Real-time monitoring dashboard

{'='*60}
    """)
    
    app.run(host=host, port=port, debug=True)
