"""
File Utilities
Common file operation utilities with error handling
"""

import os
import json
import tempfile
import shutil
from pathlib import Path
from .logging import get_logger
from .error_handler import handle_errors


logger = get_logger(__name__)


class FileManager:
    """Manages file operations with consistent error handling"""
    
    @staticmethod
    @handle_errors(default_return=None, log_error=True)
    def read_file(filepath, encoding='utf-8'):
        """Read file contents
        
        Args:
            filepath: Path to file
            encoding: File encoding (default: utf-8)
            
        Returns:
            File contents or None on error
        """
        with open(filepath, 'r', encoding=encoding) as f:
            return f.read()
    
    @staticmethod
    @handle_errors(default_return=False, log_error=True)
    def write_file(filepath, content, encoding='utf-8'):
        """Write content to file
        
        Args:
            filepath: Path to file
            content: Content to write
            encoding: File encoding (default: utf-8)
            
        Returns:
            True on success, False on error
        """
        dir_path = os.path.dirname(filepath)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    
    @staticmethod
    @handle_errors(default_return=None, log_error=True)
    def read_json(filepath, default=None):
        """Read JSON file
        
        Args:
            filepath: Path to JSON file
            default: Default value if file doesn't exist
            
        Returns:
            Parsed JSON data or default on error
        """
        if not os.path.exists(filepath):
            return default if default is not None else {}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    @handle_errors(default_return=False, log_error=True)
    def write_json(filepath, data, indent=2):
        """Write data to JSON file
        
        Args:
            filepath: Path to JSON file
            data: Data to write
            indent: JSON indentation (default: 2)
            
        Returns:
            True on success, False on error
        """
        dir_path = os.path.dirname(filepath)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
        return True
    
    @staticmethod
    def ensure_directory(directory, mode=0o755):
        """Ensure directory exists
        
        Args:
            directory: Directory path
            mode: Directory permissions (default: 0o755)
            
        Returns:
            Path object for the directory
        """
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True, mode=mode)
        return path
    
    @staticmethod
    def create_temp_directory(prefix='youtube_', suffix='', dir=None):
        """Create a temporary directory
        
        Args:
            prefix: Directory name prefix
            suffix: Directory name suffix
            dir: Parent directory (default: system temp)
            
        Returns:
            Path to temporary directory
        """
        temp_dir = tempfile.mkdtemp(prefix=prefix, suffix=suffix, dir=dir)
        os.chmod(temp_dir, 0o700)
        return temp_dir
    
    @staticmethod
    @handle_errors(default_return=False, log_error=True)
    def remove_directory(directory):
        """Remove directory and all contents
        
        Args:
            directory: Directory path to remove
            
        Returns:
            True on success, False on error
        """
        if os.path.exists(directory):
            shutil.rmtree(directory)
        return True
    
    @staticmethod
    @handle_errors(default_return=False, log_error=True)
    def remove_file(filepath):
        """Remove a file
        
        Args:
            filepath: Path to file
            
        Returns:
            True on success, False on error
        """
        if os.path.exists(filepath):
            os.remove(filepath)
        return True
    
    @staticmethod
    def get_secure_user_directory(dir_name):
        """Get a secure directory in user's home
        
        Args:
            dir_name: Subdirectory name
            
        Returns:
            String path to secure directory
        """
        secure_dir = os.path.expanduser(f"~/.youtube_automation/{dir_name}")
        return str(FileManager.ensure_directory(secure_dir, mode=0o700))


class TempFileContext:
    """Context manager for temporary files with automatic cleanup"""
    
    def __init__(self, prefix='youtube_', suffix='', dir=None):
        """Initialize temp file context
        
        Args:
            prefix: File name prefix
            suffix: File name suffix
            dir: Parent directory
        """
        self.prefix = prefix
        self.suffix = suffix
        self.dir = dir
        self.temp_file = None
        self.temp_path = None
    
    def __enter__(self):
        """Create temporary file"""
        self.temp_file = tempfile.NamedTemporaryFile(
            prefix=self.prefix,
            suffix=self.suffix,
            dir=self.dir,
            delete=False,
            mode='w'
        )
        self.temp_path = self.temp_file.name
        return self.temp_file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up temporary file"""
        if self.temp_file:
            self.temp_file.close()
        if self.temp_path and os.path.exists(self.temp_path):
            FileManager.remove_file(self.temp_path)
        return False
