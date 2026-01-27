"""
Caching Module
Provides caching functionality for API responses and expensive operations
"""

import json
import hashlib
import os
from datetime import datetime, timedelta
from functools import wraps
import threading


class SimpleCache:
    """Simple file-based cache for API responses with thread-safe operations"""
    
    def __init__(self, cache_dir='.cache', ttl_seconds=3600, max_size_mb=100):
        """Initialize cache
        
        Args:
            cache_dir: Directory to store cache files
            ttl_seconds: Time to live for cache entries (default: 1 hour)
            max_size_mb: Maximum cache size in MB (default: 100MB)
        """
        self.cache_dir = cache_dir
        self.ttl_seconds = ttl_seconds
        self.max_size_mb = max_size_mb
        self._lock = threading.RLock()
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
    
    def get(self, key, ttl_override=None):
        """Get value from cache with optional TTL override
        
        Args:
            key: Cache key
            ttl_override: Optional TTL in seconds to override default
            
        Returns:
            Cached value or None if not found or expired
        """
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with self._lock:
                with open(cache_path, 'r') as f:
                    data = json.load(f)
                
                # Check if expired
                cached_time = datetime.fromisoformat(data['timestamp'])
                ttl = ttl_override if ttl_override is not None else data.get('ttl', self.ttl_seconds)
                if datetime.now() - cached_time > timedelta(seconds=ttl):
                    # Expired, remove file
                    os.remove(cache_path)
                    return None
                
                return data['value']
        except Exception as e:
            print(f"Error reading cache: {e}")
            return None
    
    def set(self, key, value, ttl_override=None):
        """Set value in cache with optional TTL override
        
        Args:
            key: Cache key
            value: Value to cache
            ttl_override: Optional TTL in seconds to override default
        """
        cache_path = self._get_cache_path(key)
        
        try:
            with self._lock:
                # Check cache size and evict if needed
                self._evict_if_needed()
                
                data = {
                    'timestamp': datetime.now().isoformat(),
                    'value': value,
                    'ttl': ttl_override if ttl_override is not None else self.ttl_seconds
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
            with self._lock:
                for filename in os.listdir(self.cache_dir):
                    file_path = os.path.join(self.cache_dir, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
            return True
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return False
    
    def invalidate(self, key):
        """Invalidate a specific cache entry
        
        Args:
            key: Cache key to invalidate
            
        Returns:
            True if invalidated, False otherwise
        """
        cache_path = self._get_cache_path(key)
        try:
            with self._lock:
                if os.path.exists(cache_path):
                    os.remove(cache_path)
                    return True
            return False
        except Exception as e:
            print(f"Error invalidating cache: {e}")
            return False
    
    def get_size(self):
        """Get total cache size in MB
        
        Returns:
            Cache size in megabytes
        """
        total_size = 0
        try:
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)
        except Exception as e:
            print(f"Error calculating cache size: {e}")
        return total_size / (1024 * 1024)
    
    def _evict_if_needed(self):
        """Evict old entries if cache exceeds max size"""
        if self.get_size() > self.max_size_mb:
            self._evict_oldest()
    
    def _evict_oldest(self):
        """Evict oldest cache entries to free up space"""
        try:
            files = []
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if os.path.isfile(file_path):
                    mtime = os.path.getmtime(file_path)
                    files.append((mtime, file_path))
            
            # Sort by modification time and remove oldest 25%
            files.sort()
            to_remove = files[:len(files) // 4] if files else []
            
            for _, file_path in to_remove:
                os.remove(file_path)
                
        except Exception as e:
            print(f"Error evicting cache: {e}")
    
    def cleanup_expired(self):
        """Remove all expired cache entries
        
        Returns:
            Number of entries removed
        """
        removed = 0
        try:
            with self._lock:
                for filename in os.listdir(self.cache_dir):
                    file_path = os.path.join(self.cache_dir, filename)
                    if os.path.isfile(file_path):
                        try:
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                            cached_time = datetime.fromisoformat(data['timestamp'])
                            ttl = data.get('ttl', self.ttl_seconds)
                            if datetime.now() - cached_time > timedelta(seconds=ttl):
                                os.remove(file_path)
                                removed += 1
                        except Exception:
                            pass
        except Exception as e:
            print(f"Error cleaning up expired cache: {e}")
        return removed


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
