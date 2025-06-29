#!/usr/bin/env python3
"""
Script to run the AutoDashboard Streamlit frontend
"""

import subprocess
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting AutoDashboard Frontend...")
    print("📊 Frontend will be available at: http://localhost:8501")
    print("⚠️  Make sure the backend server is running first!")
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "autodashboard/frontend/app.py",
        "--server.port", "8501",
        "--server.address", "localhost"
    ]) 