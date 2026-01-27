#!/usr/bin/env python3
"""
Integration test for async task queue
Tests the complete flow of task creation, tracking, and retrieval
"""

import os
import sys
import json

# Setup environment
os.environ['OPENAI_API_KEY'] = 'sk-test-' + 'x' * 48

def test_task_queue_integration():
    """Test the task queue integration"""
    print("\n=== Task Queue Integration Test ===")
    
    # Import Flask app
    from app import app, task_queue, active_tasks, task_results, task_lock
    
    # Create test client
    with app.test_client() as client:
        print("\n1. Testing task creation endpoint...")
        response = client.post('/api/create')
        data = json.loads(response.data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert 'task_id' in data, "task_id missing from response"
        assert data['status'] == 'queued', f"Expected status 'queued', got {data['status']}"
        
        task_id = data['task_id']
        print(f"✓ Task created: {task_id}")
        
        print("\n2. Testing task status endpoint...")
        response = client.get(f'/api/task/{task_id}')
        data = json.loads(response.data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert 'status' in data, "status missing from response"
        assert data['status'] in ['queued', 'processing'], f"Unexpected status: {data['status']}"
        print(f"✓ Task status retrieved: {data['status']}")
        
        print("\n3. Testing task list endpoint...")
        response = client.get('/api/tasks')
        data = json.loads(response.data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert 'active_tasks' in data, "active_tasks missing"
        assert 'queue_size' in data, "queue_size missing"
        print(f"✓ Task list retrieved: {len(data['active_tasks'])} active tasks")
        
        print("\n4. Testing invalid task ID...")
        response = client.get('/api/task/invalid-id-123')
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        print("✓ Invalid task ID returns 404")
        
        print("\n5. Testing existing endpoints still work...")
        response = client.get('/api/status')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("✓ /api/status works")
        
        response = client.get('/api/history')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("✓ /api/history works")
        
        response = client.get('/api/config')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("✓ /api/config works")
    
    print("\n✓ All integration tests passed\n")


if __name__ == '__main__':
    print("="*60)
    print("Task Queue Integration Test")
    print("="*60)
    
    try:
        test_task_queue_integration()
        
        print("="*60)
        print("✓ INTEGRATION TEST PASSED")
        print("="*60 + "\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
