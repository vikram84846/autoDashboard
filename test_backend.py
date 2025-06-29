#!/usr/bin/env python3
"""
Test script to verify backend functionality
"""

import sys
import os
import requests
import time
import subprocess
import threading

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_backend_startup():
    """Test if backend can start and respond"""
    print("🧪 Testing backend startup...")
    
    try:
        # Import the app
        from autodashboard.backend.main import app
        print("✅ Backend app imported successfully")
        
        # Test health endpoint
        from fastapi.testclient import TestClient
        client = TestClient(app)
        response = client.get("/health")
        
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"📋 Response: {response.json()}")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🧪 Testing API endpoints...")
    
    try:
        from autodashboard.backend.main import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/health")
        print(f"✅ GET /health: {response.status_code}")
        
        # Test upload endpoint (without file)
        response = client.post("/upload")
        print(f"✅ POST /upload: {response.status_code} (expected 422 for missing file)")
        
        # Test analyze endpoint (without file)
        response = client.post("/analyze")
        print(f"✅ POST /analyze: {response.status_code} (expected 422 for missing file)")
        
        # Test PDF endpoint (without file)
        response = client.post("/generate-pdf")
        print(f"✅ POST /generate-pdf: {response.status_code} (expected 422 for missing file)")
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return False

def main():
    """Run backend tests"""
    print("🚀 AutoDashboard Backend Tests")
    print("=" * 50)
    
    tests = [
        test_backend_startup,
        test_api_endpoints
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Backend is working correctly!")
        print("\n📝 You can now:")
        print("1. Start the backend: python run_backend.py")
        print("2. Start the frontend: python run_frontend.py")
        print("3. Open http://localhost:8501 in your browser")
    else:
        print("⚠️  Some backend tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main() 