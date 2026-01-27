"""
Utility Functions
Common utilities for the YouTube automation system

Note: This module maintains backward compatibility while delegating to core utilities.
"""

import os
import json
from datetime import datetime
from functools import lru_cache

# Import from core for new functionality
try:
    from core.file_utils import FileManager
    from core.exceptions import ConfigurationError
    _HAS_CORE = True
except ImportError:
    _HAS_CORE = False


def get_timestamp_string():
    """Generate a timestamp string in consistent format"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def get_secure_directory(dir_name):
    """Get a secure directory path in user's home directory"""
    if _HAS_CORE:
        return str(FileManager.get_secure_user_directory(dir_name))
    # Fallback implementation
    secure_dir = os.path.expanduser(f"~/.youtube_automation/{dir_name}")
    os.makedirs(secure_dir, exist_ok=True, mode=0o700)
    return secure_dir


def load_json_file(filepath, default=None):
    """Safely load a JSON file with error handling"""
    if default is None:
        default = []
    
    if _HAS_CORE:
        return FileManager.read_json(filepath, default=default)
    
    # Fallback implementation
    if not os.path.exists(filepath):
        return default
    
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return default


def save_json_file(filepath, data):
    """Safely save data to a JSON file"""
    if _HAS_CORE:
        return FileManager.write_json(filepath, data)
    
    # Fallback implementation
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False


def validate_api_key(api_key, key_name="API key"):
    """Validate that an API key is provided and non-empty"""
    if not api_key or not isinstance(api_key, str) or not api_key.strip():
        error_msg = f"{key_name} is required and cannot be empty"
        if _HAS_CORE:
            raise ConfigurationError(error_msg)
        raise ValueError(error_msg)
    return api_key.strip()


@lru_cache(maxsize=128)
def cache_key(*args, **kwargs):
    """Generate a cache key from arguments"""
    key_parts = list(args)
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    return "|".join(str(part) for part in key_parts)
