# Quick Reference: Performance Optimizations

## Usage Examples

### 1. Enhanced Caching
```python
from cache import SimpleCache

# Initialize with custom settings
cache = SimpleCache(
    cache_dir='.cache',
    ttl_seconds=3600,      # Default TTL: 1 hour
    max_size_mb=100,       # Max size: 100MB
    eviction_percentage=25 # Evict 25% when full
)

# Cache with custom TTL
cache.set('key', 'value', ttl_override=7200)  # 2 hours

# Retrieve with TTL override
value = cache.get('key', ttl_override=1800)   # 30 minutes

# Invalidate specific entry
cache.invalidate('key')

# Monitor cache size
size_mb = cache.get_size()

# Cleanup expired entries
removed = cache.cleanup_expired()
```

### 2. Connection Pooling (Automatic)
```python
from content_generator import ContentGenerator

# Connection pooling is automatic - just use as normal
gen = ContentGenerator(api_key='your-key')

# All instances share the same connection pool
# No code changes needed!
```

### 3. Batch Video Processing
```python
from video_creator import VideoCreator

# Initialize with worker pool
creator = VideoCreator(max_workers=2)

# Process multiple videos in parallel
video_specs = [
    {
        'script': 'First video script...',
        'title': 'Video 1',
        'use_simple_bg': True
    },
    {
        'script': 'Second video script...',
        'title': 'Video 2',
        'use_simple_bg': True,
        'output_file': 'custom_path.mp4'
    }
]

results = creator.create_videos_batch(video_specs)

for spec, output_file in results:
    if output_file:
        print(f"Created: {output_file}")
    else:
        print(f"Failed: {spec['title']}")
```

### 4. Async Task Queue
```bash
# Create video (non-blocking)
curl -X POST http://localhost:5000/api/create

# Response:
{
  "status": "queued",
  "task_id": "abc-123-def-456",
  "message": "Video creation task queued..."
}

# Check task status
curl http://localhost:5000/api/task/abc-123-def-456

# Response:
{
  "status": "processing",
  "started_at": "2024-01-27T10:00:00"
}

# List all tasks
curl http://localhost:5000/api/tasks

# Response:
{
  "active_tasks": {...},
  "queue_size": 2
}
```

## Performance Tips

1. **Use batch processing** for multiple videos (2x faster)
2. **Set longer TTL** for stable content (reduce API calls)
3. **Monitor task queue** to avoid overload
4. **Run cleanup_expired()** periodically to free space

## Migration (None Required)

All changes are backward compatible. No migration needed!

## Testing

```bash
# Run all tests
python3 test_performance.py
python3 test_backward_compat.py
python3 test_integration.py

# Run examples
python3 examples_performance.py
```

## Troubleshooting

**Q: Cache growing too large?**
A: Reduce `max_size_mb` or increase `eviction_percentage`

**Q: Too many concurrent videos?**
A: Reduce `max_workers` in VideoCreator

**Q: Task queue backing up?**
A: Limit concurrent POST requests to /api/create

## More Info

See `PERFORMANCE_OPTIMIZATION.md` for complete documentation.
