"""
Caching Module
Provides caching functionality for API responses and expensive operations
"""

import json
import hashlib
import os
from datetime import datetime, timedelta
from functools import wraps


class SimpleCache:
    """Simple file-based cache for API responses"""
    
    def __init__(self, cache_dir='.cache', ttl_seconds=3600):
        """Initialize cache
        
        Args:
            cache_dir: Directory to store cache files
            ttl_seconds: Time to live for cache entries (default: 1 hour)
        """
        self.cache_dir = cache_dir
        self.ttl_seconds = ttl_seconds
        os.makedirs(cache_dir, exist_ok=True, mode=0o700)
    
    def _get_cache_key(self, *args, **kwargs):
        """Generate cache key from arguments (internal implementation)"""
        key_data = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get_cache_key(self, *args, **kwargs):
        """Public method to generate cache key from arguments
        
        Args:
            *args: Positional arguments to include in key
            **kwargs: Keyword arguments to include in key
            
        Returns:
            MD5 hash of the arguments as cache key
        """
        return self._get_cache_key(*args, **kwargs)
    
    def _get_cache_path(self, key):
        """Get file path for cache key"""
        return os.path.join(self.cache_dir, f"{key}.json")
    
    def get(self, key):
        """Get value from cache
        
        Returns:
            Cached value or None if not found or expired
        """
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
            
            # Check if expired
            cached_time = datetime.fromisoformat(data['timestamp'])
            if datetime.now() - cached_time > timedelta(seconds=self.ttl_seconds):
                # Expired, remove file
                os.remove(cache_path)
                return None
            
            return data['value']
        except Exception as e:
            print(f"Error reading cache: {e}")
            return None
    
    def set(self, key, value):
        """Set value in cache"""
        cache_path = self._get_cache_path(key)
        
        try:
            data = {
                'timestamp': datetime.now().isoformat(),
                'value': value
            }
            with open(cache_path, 'w') as f:
                json.dump(data, f)
            return True
        except Exception as e:
            print(f"Error writing cache: {e}")
            return False
    
    def clear(self):
        """Clear all cache entries"""
        try:
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return False


def cached(cache_instance, ttl_seconds=None):
    """Decorator to cache function results
    
    Args:
        cache_instance: SimpleCache instance to use
        ttl_seconds: Optional TTL override for this function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = cache_instance._get_cache_key(func.__name__, *args, **kwargs)
            
            # Try to get from cache
            cached_value = cache_instance.get(cache_key)
            if cached_value is not None:
                print(f"Cache hit for {func.__name__}")
                return cached_value
            
            # Cache miss, call function
            print(f"Cache miss for {func.__name__}")
            result = func(*args, **kwargs)
            
            # Store in cache
            if result is not None:
                cache_instance.set(cache_key, result)
            
            return result
        
        return wrapper
    return decorator
