"""
Flask Web Application
Provides a single-page dashboard for the automated content system
"""

from flask import Flask, render_template, jsonify, request
import os
from config import Config
from automation_engine import AutomationEngine
import threading
from queue import Queue
from datetime import datetime
import uuid

# Import new services if available
try:
    from core.logging import get_logger, LoggerFactory
    from services.task_service import TaskService
    _HAS_SERVICES = True
except ImportError:
    _HAS_SERVICES = False

app = Flask(__name__)

# Initialize configuration
config_manager = Config()

# Initialize automation engine
automation = AutomationEngine(config_manager.config)

# Initialize task service or fallback to legacy implementation
if _HAS_SERVICES:
    LoggerFactory.configure(log_file='app.log')
    logger = get_logger(__name__)
    
    task_service = TaskService(config_manager.config)
    
    def task_executor(task_type, **kwargs):
        """Execute tasks for the task service"""
        if task_type == 'create_video':
            return automation.create_and_upload_video()
        return {'status': 'error', 'error': f'Unknown task type: {task_type}'}
    
    task_service.set_executor(task_executor)
    task_service.start()
    
    # Compatibility: expose task_service methods with old names
    task_queue = None
    active_tasks = task_service.active_tasks
    task_results = task_service.task_results
    task_lock = task_service.task_lock
    shutdown_flag = task_service.shutdown_flag
else:
    # Legacy implementation
    task_queue = Queue()
    active_tasks = {}
    task_results = {}
    task_lock = threading.Lock()
    shutdown_flag = threading.Event()
    
    def task_worker():
        """Background worker to process video creation tasks"""
        from queue import Empty
        
        while not shutdown_flag.is_set():
            try:
                # Use timeout to allow checking shutdown flag
                try:
                    task_id, task_type = task_queue.get(timeout=1)
                except Empty:
                    continue
                
                if task_type == 'create_video':
                    with task_lock:
                        active_tasks[task_id] = {
                            'status': 'processing',
                            'started_at': datetime.now().isoformat()
                        }
                    
                    try:
                        # Execute the video creation
                        result = automation.create_and_upload_video()
                        
                        with task_lock:
                            active_tasks[task_id]['status'] = 'completed'
                            active_tasks[task_id]['completed_at'] = datetime.now().isoformat()
                            task_results[task_id] = result
                    except Exception as e:
                        with task_lock:
                            active_tasks[task_id]['status'] = 'failed'
                            active_tasks[task_id]['error'] = str(e)
                            active_tasks[task_id]['completed_at'] = datetime.now().isoformat()
                            task_results[task_id] = {
                                'status': 'failed',
                                'error': str(e)
                            }
                
                task_queue.task_done()
            except Exception as e:
                print(f"Task worker error: {e}")
    
    # Start background worker thread
    worker_thread = threading.Thread(target=task_worker, daemon=True)
    worker_thread.start()


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
    Trigger video creation asynchronously
    
    Returns task_id for tracking progress via /api/task/<task_id>
    """
    try:
        if _HAS_SERVICES:
            task_id = task_service.create_task('create_video')
            logger.info(f"Video creation task queued: {task_id}")
        else:
            # Legacy implementation
            task_id = str(uuid.uuid4())
            
            with task_lock:
                active_tasks[task_id] = {
                    'status': 'queued',
                    'created_at': datetime.now().isoformat()
                }
            
            task_queue.put((task_id, 'create_video'))
        
        return jsonify({
            'status': 'queued',
            'task_id': task_id,
            'message': 'Video creation task queued. Use /api/task/<task_id> to check progress.'
        })
    except Exception as e:
        if _HAS_SERVICES:
            logger.error(f"Failed to create task: {e}")
        return jsonify({
            'status': 'failed',
            'error': str(e)
        }), 500


@app.route('/api/task/<task_id>')
def get_task_status(task_id):
    """Get status of a background task"""
    if _HAS_SERVICES:
        task_info = task_service.get_task_status(task_id)
        if task_info is None:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify(task_info)
    else:
        # Legacy implementation
        with task_lock:
            if task_id not in active_tasks:
                return jsonify({'error': 'Task not found'}), 404
            
            task_info = active_tasks[task_id].copy()
            
            # Include result if completed
            if task_id in task_results:
                task_info['result'] = task_results[task_id]
            
            return jsonify(task_info)


@app.route('/api/tasks')
def list_tasks():
    """List all tasks"""
    if _HAS_SERVICES:
        return jsonify(task_service.list_tasks())
    else:
        # Legacy implementation
        with task_lock:
            return jsonify({
                'active_tasks': active_tasks,
                'queue_size': task_queue.qsize()
            })


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
