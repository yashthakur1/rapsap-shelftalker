#!/usr/bin/env python
"""
Quick start script for AOPS Backend
Runs the FastAPI server with proper configuration
"""

import os
import sys
import asyncio

# Change to backend directory
os.chdir(os.path.join(os.path.dirname(__file__), 'aops', 'backend'))
sys.path.insert(0, os.getcwd())

# Now run uvicorn
import uvicorn

if __name__ == "__main__":
    print("=" * 50)
    print("AOPS Backend Server")
    print("=" * 50)
    print(f"Working directory: {os.getcwd()}")
    print(f"Starting on http://127.0.0.1:8001")
    print(f"API Docs: http://127.0.0.1:8001/docs")
    print("=" * 50)
    print()
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )
