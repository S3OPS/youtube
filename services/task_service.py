"""
Task Service
Manages asynchronous task execution for video creation
"""

import uuid
import threading
from queue import Queue, Empty
from datetime import datetime
from core.logging import get_logger
from core.base import BaseService


logger = get_logger(__name__)


class TaskService(BaseService):
    """Service for managing asynchronous tasks"""
    
    def __init__(self, config=None):
        """Initialize task service
        
        Args:
            config: Configuration dictionary
        """
        super().__init__(config)
        self.task_queue = Queue()
        self.active_tasks = {}
        self.task_results = {}
        self.task_lock = threading.Lock()
        self.shutdown_flag = threading.Event()
        self.worker_thread = None
        self.task_executor = None
    
    def validate_config(self):
        """Validate configuration"""
        return True, None
    
    def set_executor(self, executor_func):
        """Set the task executor function
        
        Args:
            executor_func: Function to execute tasks (receives task_type)
        """
        self.task_executor = executor_func
    
    def start(self):
        """Start the task worker thread"""
        if self.worker_thread and self.worker_thread.is_alive():
            logger.warning("Task worker already running")
            return
        
        self.shutdown_flag.clear()
        self.worker_thread = threading.Thread(target=self._task_worker, daemon=True)
        self.worker_thread.start()
        logger.info("Task worker started")
    
    def stop(self):
        """Stop the task worker thread"""
        logger.info("Stopping task worker...")
        self.shutdown_flag.set()
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        logger.info("Task worker stopped")
    
    def _task_worker(self):
        """Background worker to process tasks"""
        while not self.shutdown_flag.is_set():
            try:
                try:
                    task_id, task_type, task_args = self.task_queue.get(timeout=1)
                except Empty:
                    continue
                
                self._update_task_status(task_id, 'processing', started_at=datetime.now().isoformat())
                
                try:
                    # Execute the task
                    if self.task_executor:
                        result = self.task_executor(task_type, **task_args)
                    else:
                        result = {'status': 'error', 'error': 'No task executor set'}
                    
                    self._complete_task(task_id, result)
                except Exception as e:
                    logger.error(f"Task {task_id} failed: {e}", exc_info=True)
                    self._fail_task(task_id, str(e))
                
                self.task_queue.task_done()
            except Exception as e:
                logger.error(f"Task worker error: {e}", exc_info=True)
    
    def create_task(self, task_type, **task_args):
        """Create a new task
        
        Args:
            task_type: Type of task to execute
            **task_args: Additional arguments for the task
            
        Returns:
            Task ID
        """
        task_id = str(uuid.uuid4())
        
        with self.task_lock:
            self.active_tasks[task_id] = {
                'status': 'queued',
                'task_type': task_type,
                'created_at': datetime.now().isoformat()
            }
        
        self.task_queue.put((task_id, task_type, task_args))
        logger.info(f"Task {task_id} created: {task_type}")
        
        return task_id
    
    def get_task_status(self, task_id):
        """Get task status
        
        Args:
            task_id: Task ID
            
        Returns:
            Task information dictionary or None if not found
        """
        with self.task_lock:
            if task_id not in self.active_tasks:
                return None
            
            task_info = self.active_tasks[task_id].copy()
            
            if task_id in self.task_results:
                task_info['result'] = self.task_results[task_id]
            
            return task_info
    
    def list_tasks(self):
        """List all tasks
        
        Returns:
            Dictionary with active tasks and queue size
        """
        with self.task_lock:
            return {
                'active_tasks': self.active_tasks.copy(),
                'queue_size': self.task_queue.qsize()
            }
    
    def _update_task_status(self, task_id, status, **extra_fields):
        """Update task status
        
        Args:
            task_id: Task ID
            status: New status
            **extra_fields: Additional fields to update
        """
        with self.task_lock:
            if task_id in self.active_tasks:
                self.active_tasks[task_id]['status'] = status
                self.active_tasks[task_id].update(extra_fields)
    
    def _complete_task(self, task_id, result):
        """Mark task as completed
        
        Args:
            task_id: Task ID
            result: Task result
        """
        with self.task_lock:
            self.active_tasks[task_id]['status'] = 'completed'
            self.active_tasks[task_id]['completed_at'] = datetime.now().isoformat()
            self.task_results[task_id] = result
        logger.info(f"Task {task_id} completed successfully")
    
    def _fail_task(self, task_id, error):
        """Mark task as failed
        
        Args:
            task_id: Task ID
            error: Error message
        """
        with self.task_lock:
            self.active_tasks[task_id]['status'] = 'failed'
            self.active_tasks[task_id]['error'] = error
            self.active_tasks[task_id]['completed_at'] = datetime.now().isoformat()
            self.task_results[task_id] = {
                'status': 'failed',
                'error': error
            }
        logger.error(f"Task {task_id} failed: {error}")
