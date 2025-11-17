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
    # Allow platform (Render, Docker, etc.) to control host and port via environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', os.environ.get('UVICORN_PORT', 8000)))
    print(f"Starting on http://{host}:{port}")
    print(f"API Docs: http://{host}:{port}/docs")
    print("=" * 50)
    print()
    
    # Ensure uploads directory exists to avoid static mount warnings
    try:
        os.makedirs(os.path.join(os.getcwd(), 'uploads'), exist_ok=True)
    except Exception:
        pass

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
