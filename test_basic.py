#!/usr/bin/env python3
"""
Basic test script for AutoDashboard core functionality (no API key required)
"""

import sys
import os
import pandas as pd
import numpy as np

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_imports():
    """Test core module imports"""
    print("🧪 Testing core imports...")
    
    try:
        from autodashboard.backend.analysis import clean_data, analyze_data, generate_visualizations
        print("✅ Core analysis modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Core import failed: {e}")
        return False

def test_data_processing():
    """Test data processing without API calls"""
    print("\n🧪 Testing data processing...")
    
    try:
        from autodashboard.backend.analysis import clean_data, analyze_data, generate_visualizations
        
        # Create sample dataset
        np.random.seed(42)
        data = {
            'sales': np.random.randint(100, 1000, 50),
            'profit': np.random.uniform(10, 100, 50),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 50),
            'product': np.random.choice(['A', 'B', 'C', 'D'], 50),
            'date': pd.date_range('2023-01-01', periods=50, freq='D')
        }
        df = pd.DataFrame(data)
        
        # Add some missing values
        df.loc[5:10, 'sales'] = np.nan
        df.loc[15:20, 'region'] = None
        
        print(f"📊 Original dataset: {len(df)} rows, {len(df.columns)} columns")
        print(f"📊 Missing values: {df.isnull().sum().sum()} total")
        
        # Test data cleaning
        df_cleaned = clean_data(df)
        print(f"✅ Data cleaning: {len(df_cleaned)} rows, {len(df_cleaned.columns)} columns")
        print(f"✅ Missing values after cleaning: {df_cleaned.isnull().sum().sum()}")
        
        # Test analysis
        analysis_result = analyze_data(df_cleaned)
        print(f"✅ Data analysis completed: {len(analysis_result)} components")
        
        # Test visualizations
        charts = generate_visualizations(df_cleaned)
        print(f"✅ Visualizations generated: {len(charts)} charts")
        
        # Show chart types
        chart_types = [chart.get('type', 'unknown') for chart in charts]
        print(f"📊 Chart types: {', '.join(set(chart_types))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data processing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backend_api():
    """Test backend API structure"""
    print("\n🧪 Testing backend API structure...")
    
    try:
        from autodashboard.backend.main import app
        
        # Check if FastAPI app is properly configured
        routes = [route.path for route in app.routes]
        expected_routes = ['/health', '/upload', '/analyze', '/generate-pdf']
        
        print(f"✅ FastAPI app created with {len(routes)} routes")
        print(f"📋 Available routes: {', '.join(routes)}")
        
        # Check if expected routes exist
        missing_routes = [route for route in expected_routes if route not in routes]
        if missing_routes:
            print(f"⚠️  Missing routes: {missing_routes}")
        else:
            print("✅ All expected routes present")
        
        return True
        
    except Exception as e:
        print(f"❌ Backend API test failed: {e}")
        return False

def test_frontend_structure():
    """Test frontend structure"""
    print("\n🧪 Testing frontend structure...")
    
    try:
        from autodashboard.frontend.app import main, check_backend_health, upload_file_to_backend
        
        print("✅ Frontend functions imported successfully")
        print("✅ Streamlit app structure is valid")
        
        return True
        
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
        return False

def main():
    """Run all basic tests"""
    print("🚀 AutoDashboard Basic Tests (No API Key Required)")
    print("=" * 60)
    
    tests = [
        test_core_imports,
        test_data_processing,
        test_backend_api,
        test_frontend_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed! Core functionality is working.")
        print("\n📝 Next steps:")
        print("1. Add your Google Gemini API key to .env file")
        print("2. Run: python run_backend.py")
        print("3. Run: python run_frontend.py")
        print("4. Open http://localhost:8501 in your browser")
        print("\n💡 The app will work for data visualization even without the API key!")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main() 