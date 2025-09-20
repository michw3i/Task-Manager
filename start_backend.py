#!/usr/bin/env python3
"""
Startup script for the Task Manager backend.
This will initialize the database and start the Flask server.
"""

import subprocess
import sys
import os
import time

def main():
    print("Starting Task Manager Backend...")
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    # Initialize database
    print("1. Initializing database...")
    try:
        subprocess.run([sys.executable, 'init_db.py'], check=True)
        print("✓ Database initialized successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Database initialization failed: {e}")
        return
    
    # Start Flask server
    print("2. Starting Flask server...")
    print("   Server will be available at: http://127.0.0.1:5000")
    print("   Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, 'todo.py'], check=True)
    except KeyboardInterrupt:
        print("\n✓ Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"✗ Server failed to start: {e}")

if __name__ == "__main__":
    main()
