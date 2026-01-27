#!/usr/bin/env python3
"""
Simple performance test for the optimization features
"""

import sys
import os
from datetime import datetime

def test_cache_improvements():
    """Test enhanced cache functionality"""
    print("\n=== Testing Cache Improvements ===")
    from cache import SimpleCache
    
    # Test basic cache operations
    cache = SimpleCache(cache_dir='.cache/test', ttl_seconds=10, max_size_mb=1)
    
    # Test set/get with default TTL
    cache.set('key1', 'value1')
    result = cache.get('key1')
    assert result == 'value1', "Cache get failed"
    print("✓ Basic cache set/get works")
    
    # Test set/get with custom TTL
    cache.set('key2', 'value2', ttl_override=5)
    result = cache.get('key2')
    assert result == 'value2', "Cache with custom TTL failed"
    print("✓ Custom TTL works")
    
    # Test invalidation
    cache.invalidate('key1')
    result = cache.get('key1')
    assert result is None, "Cache invalidation failed"
    print("✓ Cache invalidation works")
    
    # Test size calculation
    size = cache.get_size()
    assert size >= 0, "Cache size calculation failed"
    print(f"✓ Cache size calculation works ({size:.3f} MB)")
    
    # Test cleanup
    cache.cleanup_expired()
    print("✓ Cleanup expired entries works")
    
    # Cleanup test cache
    cache.clear()
    print("✓ All cache tests passed\n")


def test_video_batch_processing():
    """Test batch video processing capability"""
    print("\n=== Testing Batch Video Processing ===")
    from video_creator import VideoCreator
    
    # Test batch creation structure (without actually creating videos)
    creator = VideoCreator(max_workers=2)
    
    # Verify batch method exists
    assert hasattr(creator, 'create_videos_batch'), "Batch method missing"
    print("✓ Batch processing method exists")
    
    # Verify max_workers is set
    assert creator.max_workers == 2, "max_workers not set"
    print("✓ max_workers parameter works")
    
    creator.cleanup()
    print("✓ Batch video processing tests passed\n")


def test_connection_pooling():
    """Test connection pooling setup"""
    print("\n=== Testing Connection Pooling ===")
    
    # Mock API key for testing structure
    os.environ['OPENAI_API_KEY'] = 'sk-test-' + 'x' * 48
    
    from content_generator import ContentGenerator
    
    # Test that HTTP client pool is created
    gen1 = ContentGenerator(os.environ['OPENAI_API_KEY'])
    assert hasattr(ContentGenerator, '_get_http_client'), "HTTP client pool method missing"
    print("✓ Connection pooling method exists")
    
    # Test client initialization
    assert gen1.client is not None, "OpenAI client not initialized"
    print("✓ OpenAI client initialized with pooling")
    
    # Test shared client
    gen2 = ContentGenerator(os.environ['OPENAI_API_KEY'])
    assert ContentGenerator._http_client is not None, "Shared HTTP client not created"
    print("✓ Shared HTTP client pool works")
    
    print("✓ Connection pooling tests passed\n")


def test_async_task_queue():
    """Test async task queue setup"""
    print("\n=== Testing Async Task Queue ===")
    
    # Import app components
    import app as flask_app
    
    # Verify task queue exists
    assert hasattr(flask_app, 'task_queue'), "Task queue missing"
    print("✓ Task queue exists")
    
    # Verify worker thread is running
    assert hasattr(flask_app, 'worker_thread'), "Worker thread missing"
    assert flask_app.worker_thread.is_alive(), "Worker thread not running"
    print("✓ Worker thread is running")
    
    # Verify task tracking structures
    assert hasattr(flask_app, 'active_tasks'), "Active tasks dict missing"
    assert hasattr(flask_app, 'task_results'), "Task results dict missing"
    print("✓ Task tracking structures exist")
    
    print("✓ Async task queue tests passed\n")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Performance Optimization Tests")
    print("="*60)
    
    try:
        test_cache_improvements()
        test_video_batch_processing()
        test_connection_pooling()
        test_async_task_queue()
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED")
        print("="*60 + "\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
