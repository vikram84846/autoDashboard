#!/usr/bin/env python3
"""
Script to run the AutoDashboard FastAPI backend server
"""

import uvicorn
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting AutoDashboard Backend Server...")
    print("📊 API will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    
    uvicorn.run(
        "autodashboard.backend.main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info"
    ) 