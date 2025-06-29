#!/usr/bin/env python3
"""
Test script for AutoDashboard components
"""

import sys
import os
import pandas as pd
import numpy as np

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from autodashboard.backend import main, analysis, llm_agent, pdf_report
        print("✅ Backend modules imported successfully")
    except Exception as e:
        print(f"❌ Backend import failed: {e}")
        return False
    
    try:
        from autodashboard.frontend import app
        print("✅ Frontend module imported successfully")
    except Exception as e:
        print(f"❌ Frontend import failed: {e}")
        return False
    
    return True

def test_data_analysis():
    """Test data analysis functions"""
    print("\n🧪 Testing data analysis...")
    
    try:
        from autodashboard.backend.analysis import clean_data, analyze_data, generate_visualizations
        
        # Create sample data
        data = {
            'numeric_col': [1, 2, 3, 4, 5, np.nan, 7, 8, 9, 10],
            'categorical_col': ['A', 'B', 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'B'],
            'date_col': pd.date_range('2023-01-01', periods=10, freq='D')
        }
        df = pd.DataFrame(data)
        
        # Test data cleaning
        df_cleaned = clean_data(df)
        print(f"✅ Data cleaning: {len(df_cleaned)} rows, {len(df_cleaned.columns)} columns")
        
        # Test analysis
        analysis_result = analyze_data(df_cleaned)
        print(f"✅ Data analysis: {len(analysis_result)} analysis components")
        
        # Test visualizations
        charts = generate_visualizations(df_cleaned)
        print(f"✅ Visualizations: {len(charts)} charts generated")
        
        return True
        
    except Exception as e:
        print(f"❌ Data analysis test failed: {e}")
        return False

def test_llm_agent():
    """Test LLM agent functions"""
    print("\n🧪 Testing LLM agent...")
    
    try:
        from autodashboard.backend.llm_agent import analyze_with_llm
        
        # Test with sample data
        sample_analysis = {
            'dataset_info': {'rows': 100, 'columns': 5, 'memory_usage': 0.5},
            'numeric_summary': {'col1': {'mean': 50, 'std': 10}},
            'categorical_summary': {'col2': {'unique_values': 3}},
            'missing_values': {'col1': 0, 'col2': 2}
        }
        
        # This will fail without API key, but should not crash
        result = analyze_with_llm(sample_analysis)
        print(f"✅ LLM agent: {result[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM agent test failed: {e}")
        return False

def test_pdf_generation():
    """Test PDF generation"""
    print("\n🧪 Testing PDF generation...")
    
    try:
        from autodashboard.backend.pdf_report import create_pdf_report
        
        # Test with sample data
        sample_analysis = {
            'dataset_info': {'rows': 100, 'columns': 5, 'memory_usage': 0.5},
            'data_types': {'col1': 'int64', 'col2': 'object'},
            'missing_values': {'col1': 0, 'col2': 2},
            'numeric_summary': {'col1': {'mean': 50, 'std': 10}},
            'categorical_summary': {'col2': {'unique_values': 3, 'most_common': 'A'}}
        }
        
        sample_charts = [
            {'type': 'distribution', 'title': 'Test Chart', 'plot': '{}'}
        ]
        
        sample_llm_analysis = "This is a sample LLM analysis for testing purposes."
        
        pdf_content = create_pdf_report(sample_analysis, sample_charts, sample_llm_analysis)
        print(f"✅ PDF generation: {len(pdf_content)} bytes generated")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF generation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AutoDashboard Component Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_data_analysis,
        test_llm_agent,
        test_pdf_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AutoDashboard is ready to use.")
        print("\n📝 Next steps:")
        print("1. Set your GOOGLE_API_KEY environment variable")
        print("2. Run: python run_backend.py")
        print("3. Run: python run_frontend.py")
        print("4. Open http://localhost:8501 in your browser")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main() 