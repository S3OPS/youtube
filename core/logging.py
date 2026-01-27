"""
Logging Framework
Centralized logging configuration for the YouTube automation system
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


class LoggerFactory:
    """Factory for creating standardized loggers"""
    
    _loggers = {}
    _configured = False
    
    @classmethod
    def configure(cls, log_level=logging.INFO, log_file=None, log_dir='logs'):
        """Configure global logging settings
        
        Args:
            log_level: Logging level (default: INFO)
            log_file: Optional log file name
            log_dir: Directory for log files (default: 'logs')
        """
        if cls._configured:
            return
        
        # Create log directory
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True, mode=0o755)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_path / log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        cls._configured = True
    
    @classmethod
    def get_logger(cls, name):
        """Get or create a logger with the given name
        
        Args:
            name: Logger name (typically __name__)
            
        Returns:
            Configured logger instance
        """
        if name not in cls._loggers:
            if not cls._configured:
                cls.configure()
            cls._loggers[name] = logging.getLogger(name)
        return cls._loggers[name]


def get_logger(name):
    """Convenience function to get a logger
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    return LoggerFactory.get_logger(name)
