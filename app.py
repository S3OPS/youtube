"""
Flask Web Application
Provides a single-page dashboard for the automated content system
"""

from flask import Flask, render_template, jsonify, request
import os
from config import Config
from automation_engine import AutomationEngine
import threading

app = Flask(__name__)

# Initialize configuration
config_manager = Config()

# Initialize automation engine
automation = AutomationEngine(config_manager.config)


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
    """
    Trigger video creation
    
    Note: This runs synchronously and may take 2-5 minutes to complete.
    For production use, consider implementing a task queue (e.g., Celery, RQ)
    to handle video creation asynchronously.
    """
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
        return jsonify(config_manager.to_dict())
    else:
        try:
            data = request.json
            # Update config with validation
            success, error = config_manager.update(data)
            if success:
                # Update automation engine config as well
                for key, value in data.items():
                    automation.config[key] = value
                return jsonify({'status': 'success', 'config': config_manager.to_dict()})
            else:
                return jsonify({'status': 'error', 'error': error}), 400
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
