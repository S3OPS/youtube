#!/usr/bin/env python3
"""
Performance Optimization Examples
Demonstrates how to use the new performance features
"""

import os
from content_generator import ContentGenerator
from video_creator import VideoCreator
from cache import SimpleCache


def example_cache_with_custom_ttl():
    """Example: Using cache with custom TTL"""
    print("\n=== Example: Cache with Custom TTL ===")
    
    cache = SimpleCache(cache_dir='.cache/examples', ttl_seconds=3600)
    
    # Cache script with 2-hour TTL (longer for stable content)
    cache.set('script_v1', 'This is my video script...', ttl_override=7200)
    
    # Cache API response with 30-minute TTL (shorter for dynamic content)
    cache.set('api_response', {'data': 'response'}, ttl_override=1800)
    
    # Retrieve with TTL override
    script = cache.get('script_v1', ttl_override=3600)
    
    print("✓ Custom TTL example completed")


def example_batch_video_creation():
    """Example: Batch process multiple videos"""
    print("\n=== Example: Batch Video Creation ===")
    
    creator = VideoCreator(max_workers=2)
    
    # Define multiple videos to create
    video_specs = [
        {
            'script': 'First video script here...',
            'title': 'Video 1',
            'use_simple_bg': True
        },
        {
            'script': 'Second video script here...',
            'title': 'Video 2',
            'use_simple_bg': True
        }
    ]
    
    # Process all videos in parallel
    # results = creator.create_videos_batch(video_specs)
    
    # Check results
    # for spec, output_file in results:
    #     if output_file:
    #         print(f"✓ Created: {output_file}")
    #     else:
    #         print(f"✗ Failed: {spec['title']}")
    
    print("✓ Batch processing example shown (commented out to avoid actual video creation)")
    creator.cleanup()


def example_connection_pooling():
    """Example: Content generator with connection pooling"""
    print("\n=== Example: Connection Pooling ===")
    
    # Set mock API key for example
    os.environ['OPENAI_API_KEY'] = 'sk-test-' + 'x' * 48
    
    # Create multiple generators - they share the same HTTP client pool
    gen1 = ContentGenerator(os.environ['OPENAI_API_KEY'], enable_cache=True)
    gen2 = ContentGenerator(os.environ['OPENAI_API_KEY'], enable_cache=True)
    
    # Both use the same connection pool automatically
    # API calls will reuse connections, reducing latency
    
    print("✓ Connection pooling is automatic and shared across instances")


def example_async_task_api():
    """Example: Using async task API"""
    print("\n=== Example: Async Task API Usage ===")
    
    print("""
    # Create video asynchronously
    curl -X POST http://localhost:5000/api/create
    
    Response:
    {
        "status": "queued",
        "task_id": "abc-123-def-456",
        "message": "Video creation task queued..."
    }
    
    # Check task status
    curl http://localhost:5000/api/task/abc-123-def-456
    
    Response:
    {
        "status": "processing",
        "started_at": "2024-01-01T12:00:00",
        ...
    }
    
    # List all tasks
    curl http://localhost:5000/api/tasks
    
    Response:
    {
        "active_tasks": {...},
        "queue_size": 2
    }
    """)
    
    print("✓ Async API usage examples shown")


def example_cache_management():
    """Example: Cache management operations"""
    print("\n=== Example: Cache Management ===")
    
    cache = SimpleCache(cache_dir='.cache/managed', max_size_mb=50)
    
    # Store some data
    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    
    # Check cache size
    size = cache.get_size()
    print(f"Cache size: {size:.3f} MB")
    
    # Invalidate specific entry
    cache.invalidate('key1')
    print("Invalidated key1")
    
    # Cleanup expired entries
    removed = cache.cleanup_expired()
    print(f"Removed {removed} expired entries")
    
    # Clear all
    cache.clear()
    print("Cleared all cache")
    
    print("✓ Cache management example completed")


if __name__ == '__main__':
    print("="*60)
    print("Performance Optimization Examples")
    print("="*60)
    
    example_cache_with_custom_ttl()
    example_batch_video_creation()
    example_connection_pooling()
    example_async_task_api()
    example_cache_management()
    
    print("\n" + "="*60)
    print("All examples completed")
    print("="*60 + "\n")
