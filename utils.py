"""
Utility Functions
Common utilities for the YouTube automation system
"""

import os
import json
from datetime import datetime
from functools import lru_cache


def get_timestamp_string():
    """Generate a timestamp string in consistent format"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def get_secure_directory(dir_name):
    """Get a secure directory path in user's home directory"""
    secure_dir = os.path.expanduser(f"~/.youtube_automation/{dir_name}")
    os.makedirs(secure_dir, exist_ok=True, mode=0o700)
    return secure_dir


def load_json_file(filepath, default=None):
    """Safely load a JSON file with error handling"""
    if default is None:
        default = []
    
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
        raise ValueError(f"{key_name} is required and cannot be empty")
    return api_key.strip()


@lru_cache(maxsize=128)
def cache_key(*args, **kwargs):
    """Generate a cache key from arguments"""
    key_parts = list(args)
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    return "|".join(str(part) for part in key_parts)
