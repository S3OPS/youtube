#!/usr/bin/env python3
"""
Backward compatibility verification
Ensures all existing APIs still work as expected
"""

import os
import sys

# Setup test environment
os.environ['OPENAI_API_KEY'] = 'sk-test-' + 'x' * 48


def test_video_creator_backward_compat():
    """Verify VideoCreator backward compatibility"""
    print("\n=== VideoCreator Backward Compatibility ===")
    from video_creator import VideoCreator
    
    # Old initialization (without max_workers)
    creator = VideoCreator(output_dir="test_videos")
    assert creator.output_dir == "test_videos"
    print("✓ Old constructor signature works")
    
    # Old methods still exist
    assert hasattr(creator, 'create_video_from_script')
    assert hasattr(creator, 'create_simple_video')
    assert hasattr(creator, 'create_video')
    print("✓ All legacy methods exist")
    
    creator.cleanup()
    print("✓ VideoCreator backward compatible\n")


def test_cache_backward_compat():
    """Verify SimpleCache backward compatibility"""
    print("\n=== SimpleCache Backward Compatibility ===")
    from cache import SimpleCache
    
    # Old initialization (without new params)
    cache = SimpleCache(cache_dir='.cache/test_compat', ttl_seconds=3600)
    
    # Old API usage
    cache.set('key', 'value')
    result = cache.get('key')
    assert result == 'value'
    print("✓ Old set/get API works")
    
    cache.clear()
    print("✓ SimpleCache backward compatible\n")


def test_content_generator_backward_compat():
    """Verify ContentGenerator backward compatibility"""
    print("\n=== ContentGenerator Backward Compatibility ===")
    from content_generator import ContentGenerator
    
    # Old initialization
    gen = ContentGenerator(
        api_key=os.environ['OPENAI_API_KEY'],
        topic='technology',
        enable_cache=True
    )
    
    # Old methods still exist
    assert hasattr(gen, 'generate_video_script')
    assert hasattr(gen, 'generate_title_and_description')
    assert hasattr(gen, 'generate_product_keywords')
    print("✓ All legacy methods exist")
    
    print("✓ ContentGenerator backward compatible\n")


def test_app_routes_exist():
    """Verify Flask app routes"""
    print("\n=== Flask App Routes ===")
    import app as flask_app
    
    # Check existing routes still exist
    routes = [rule.rule for rule in flask_app.app.url_map.iter_rules()]
    
    assert '/' in routes
    assert '/api/status' in routes
    assert '/api/history' in routes
    assert '/api/create' in routes
    assert '/api/config' in routes
    print("✓ All existing routes present")
    
    # New routes added
    assert any('/api/task/<task_id>' in route for route in routes)
    assert '/api/tasks' in routes
    print("✓ New task routes added")
    
    print("✓ Flask app backward compatible\n")


if __name__ == '__main__':
    print("="*60)
    print("Backward Compatibility Tests")
    print("="*60)
    
    try:
        test_video_creator_backward_compat()
        test_cache_backward_compat()
        test_content_generator_backward_compat()
        test_app_routes_exist()
        
        print("\n" + "="*60)
        print("✓ ALL BACKWARD COMPATIBILITY TESTS PASSED")
        print("="*60 + "\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
