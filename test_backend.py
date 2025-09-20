#!/usr/bin/env python3
"""
Simple test script to verify the backend API is working correctly.
Run this after starting the Flask server.
"""

import requests
import json

API_BASE = "http://127.0.0.1:5000"

def test_api():
    print("Testing Task Manager Backend API...")
    
    # Test 1: Create a user
    print("\n1. Testing user creation...")
    user_data = {"name": "TestUser"}
    response = requests.post(f"{API_BASE}/user", json=user_data)
    if response.status_code == 200:
        user_result = response.json()
        print(f"✓ User created/found: {user_result}")
        user_id = user_result['user_id']
    else:
        print(f"✗ User creation failed: {response.status_code}")
        return
    
    # Test 2: Add a task
    print("\n2. Testing task creation...")
    task_data = {
        "user_id": user_id,
        "description": "Test task from API",
        "due_date": "2024-01-15"
    }
    response = requests.post(f"{API_BASE}/task", json=task_data)
    if response.status_code == 200:
        print(f"✓ Task created: {response.json()}")
    else:
        print(f"✗ Task creation failed: {response.status_code}")
        return
    
    # Test 3: Get user tasks
    print("\n3. Testing task retrieval...")
    response = requests.get(f"{API_BASE}/tasks/TestUser")
    if response.status_code == 200:
        tasks_result = response.json()
        print(f"✓ Tasks retrieved: {tasks_result}")
        if tasks_result['tasks']:
            task_id = tasks_result['tasks'][0]['id']
            print(f"  Task ID: {task_id}")
        else:
            print("  No tasks found")
    else:
        print(f"✗ Task retrieval failed: {response.status_code}")
        return
    
    # Test 4: Delete a task (if we have one)
    if 'task_id' in locals():
        print("\n4. Testing task deletion...")
        response = requests.delete(f"{API_BASE}/task/{task_id}")
        if response.status_code == 200:
            print(f"✓ Task deleted: {response.json()}")
        else:
            print(f"✗ Task deletion failed: {response.status_code}")
    
    # Test 5: Get summary
    print("\n5. Testing summary...")
    response = requests.get(f"{API_BASE}/summary")
    if response.status_code == 200:
        summary_result = response.json()
        print(f"✓ Summary retrieved: {summary_result}")
    else:
        print(f"✗ Summary retrieval failed: {response.status_code}")
    
    print("\n✓ All tests completed!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to backend. Make sure Flask server is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"✗ Error during testing: {e}")
