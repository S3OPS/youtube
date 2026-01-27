"""
History Service
Manages automation execution history
"""

from datetime import datetime
from core.logging import get_logger
from core.base import BaseService
from core.file_utils import FileManager


logger = get_logger(__name__)


class HistoryService(BaseService):
    """Service for managing automation history"""
    
    def __init__(self, history_file='automation_history.json', config=None):
        """Initialize history service
        
        Args:
            history_file: Path to history file
            config: Configuration dictionary
        """
        super().__init__(config)
        self.history_file = history_file
        self.history = []
        self._load_history()
    
    def validate_config(self):
        """Validate configuration"""
        return True, None
    
    def _load_history(self):
        """Load history from file"""
        self.history = FileManager.read_json(self.history_file, default=[])
        if self.history:
            logger.info(f"Loaded {len(self.history)} history entries")
        else:
            logger.info("No existing history found")
    
    def _save_history(self):
        """Save history to file"""
        if FileManager.write_json(self.history_file, self.history):
            logger.debug("History saved successfully")
        else:
            logger.error("Failed to save history")
    
    def add_entry(self, entry):
        """Add an entry to history
        
        Args:
            entry: History entry dictionary
        """
        if 'timestamp' not in entry:
            entry['timestamp'] = datetime.now().isoformat()
        
        self.history.append(entry)
        self._save_history()
        logger.info(f"History entry added: {entry.get('status', 'unknown')}")
    
    def get_all(self):
        """Get all history entries
        
        Returns:
            List of history entries
        """
        return self.history
    
    def get_recent(self, limit=10):
        """Get recent history entries
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of recent history entries
        """
        return self.history[-limit:] if self.history else []
    
    def get_last(self):
        """Get last history entry
        
        Returns:
            Last history entry or None
        """
        return self.history[-1] if self.history else None
    
    def get_stats(self):
        """Get history statistics
        
        Returns:
            Dictionary with statistics
        """
        total = len(self.history)
        successful = len([h for h in self.history if h.get('status') == 'success'])
        failed = len([h for h in self.history if h.get('status') == 'failed'])
        
        return {
            'total_videos': total,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'last_run': self.get_last()
        }
    
    def clear(self):
        """Clear all history"""
        self.history = []
        self._save_history()
        logger.info("History cleared")
