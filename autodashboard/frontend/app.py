import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import requests
import json
import io
import base64
from typing import Dict, Any, List
import time
from dotenv import load_dotenv
import os

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    print(f"⚠️  Warning: Could not load .env file: {e}")
    print("💡 You can set GOOGLE_API_KEY as an environment variable instead")

# Page configuration
st.set_page_config(
    page_title="AutoDashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
</style>
""", unsafe_allow_html=True)

# Backend API URL - use localhost
BACKEND_URL = "http://localhost:8000"

def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def upload_file_to_backend(file):
    """Upload file to backend and get summary"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{BACKEND_URL}/upload", files=files)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error uploading file: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return None

def analyze_file_with_backend(file):
    """Analyze file with backend and get results"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{BACKEND_URL}/analyze", files=files)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error analyzing file: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return None

def download_pdf_report(file):
    """Download PDF report from backend"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{BACKEND_URL}/generate-pdf", files=files)
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"Error generating PDF: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return None

def display_dataset_summary(summary: Dict[str, Any]):
    """Display dataset summary in a clean format"""
    st.subheader("📋 Dataset Overview")
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Rows", summary.get('rows', 'N/A'))
    
    with col2:
        st.metric("Columns", summary.get('columns', 'N/A'))
    
    with col3:
        st.metric("Numeric Columns", len(summary.get('numeric_columns', [])))
    
    with col4:
        st.metric("Categorical Columns", len(summary.get('categorical_columns', [])))
    
    # Data types and missing values
    st.subheader("🔍 Data Quality")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Data Types:**")
        data_types = summary.get('data_types', {})
        for col, dtype in data_types.items():
            st.write(f"• {col}: {dtype}")
    
    with col2:
        st.write("**Missing Values:**")
        missing_values = summary.get('missing_values', {})
        for col, count in missing_values.items():
            if count > 0:
                st.write(f"• {col}: {count}")

def display_charts(charts: List[Dict[str, Any]]):
    """Display charts in a grid layout"""
    st.subheader("📊 Data Visualizations")
    
    if not charts:
        st.info("No charts generated for this dataset.")
        return
    
    # Group charts by type for better organization
    chart_types = {}
    for chart in charts:
        chart_type = chart.get('type', 'other')
        if chart_type not in chart_types:
            chart_types[chart_type] = []
        chart_types[chart_type].append(chart)
    
    # Display charts in a responsive grid
    for chart_type, type_charts in chart_types.items():
        st.write(f"**{chart_type.title()} Charts:**")
        
        # Calculate grid layout
        num_charts = len(type_charts)
        if num_charts == 1:
            # Single chart - no columns needed
            chart = type_charts[0]
            try:
                # Parse plotly chart
                chart_json = chart.get('plot', '{}')
                if chart_json:
                    fig = pio.from_json(chart_json)
                    
                    # Update layout for better display
                    fig.update_layout(
                        height=400,
                        margin=dict(l=20, r=20, t=40, b=20),
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Chart title
                    st.caption(chart.get('title', 'Untitled'))
            
            except Exception as e:
                st.error(f"Error displaying chart: {str(e)}")
        
        else:
            # Multiple charts - use columns
            if num_charts == 2:
                col1, col2 = st.columns(2)
                cols = [col1, col2]
            elif num_charts == 3:
                col1, col2, col3 = st.columns(3)
                cols = [col1, col2, col3]
            else:
                # For more than 3 charts, use 2 columns
                col1, col2 = st.columns(2)
                cols = [col1, col2]
            
            for i, chart in enumerate(type_charts):
                col_idx = i % len(cols)
                with cols[col_idx]:
                    try:
                        # Parse plotly chart
                        chart_json = chart.get('plot', '{}')
                        if chart_json:
                            fig = pio.from_json(chart_json)
                            
                            # Update layout for better display
                            fig.update_layout(
                                height=400,
                                margin=dict(l=20, r=20, t=40, b=20),
                                showlegend=True
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Chart title
                            st.caption(chart.get('title', 'Untitled'))
                    
                    except Exception as e:
                        st.error(f"Error displaying chart: {str(e)}")

def display_analysis(analysis: Dict[str, Any], llm_insights: str):
    """Display analysis results"""
    st.subheader("🧠 AI-Powered Analysis")
    
    # LLM Insights
    with st.expander("🤖 LLM Insights", expanded=True):
        st.write(llm_insights)
    
    # Statistical Summary
    with st.expander("📈 Statistical Summary"):
        numeric_summary = analysis.get('numeric_summary', {})
        if numeric_summary:
            for col, stats in numeric_summary.items():
                st.write(f"**{col}:**")
                stats_df = pd.DataFrame(list(stats.items()), columns=['Statistic', 'Value'])
                st.dataframe(stats_df, use_container_width=True)
                st.write("---")
    
    # Categorical Summary
    with st.expander("📊 Categorical Analysis"):
        categorical_summary = analysis.get('categorical_summary', {})
        if categorical_summary:
            for col, summary in categorical_summary.items():
                st.write(f"**{col}:**")
                st.write(f"• Unique values: {summary.get('unique_values', 'N/A')}")
                st.write(f"• Most common: {summary.get('most_common', 'N/A')}")
                st.write("---")

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 AutoDashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Interactive Data Visualization & Analysis Platform")
    
    # Check API key status
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your-api-key-here":
        st.warning("⚠️ **Google Gemini API Key Not Configured**")
        st.info("""
        To enable AI-powered analysis:
        1. Get your API key from: https://makersuite.google.com/app/apikey
        2. Add it to your `.env` file: `GOOGLE_API_KEY=your-actual-api-key`
        3. Restart the application
        
        **Note**: The application will still work for data visualization and analysis, but AI insights will be limited.
        """)
    else:
        st.success("✅ Google Gemini API Key Configured - AI Analysis Enabled")
    
    # Check backend health
    if not check_backend_health():
        st.error("⚠️ Backend server is not running. Please start the FastAPI backend first.")
        st.info("To start the backend, run: `python run_backend.py`")
        return
    
    # Sidebar
    st.sidebar.title("⚙️ Settings")
    
    # File upload
    st.sidebar.subheader("📁 Upload Data")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV or Excel file",
        type=['csv', 'xlsx'],
        help="Upload your dataset to get started"
    )
    
    # Main content area
    if uploaded_file is not None:
        # Show file info
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Overview", "📊 Dashboard", "📄 Report"])
        
        with tab1:
            # Get dataset summary
            with st.spinner("Analyzing dataset..."):
                summary_result = upload_file_to_backend(uploaded_file)
            
            if summary_result and summary_result.get('success'):
                summary = summary_result['summary']
                display_dataset_summary(summary)
                
                # Show raw data preview
                st.subheader("👀 Data Preview")
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    st.dataframe(df.head(10), use_container_width=True)
                    st.caption(f"Showing first 10 rows of {len(df)} total rows")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        with tab2:
            # Generate full analysis and charts
            with st.spinner("Generating visualizations and analysis..."):
                analysis_result = analyze_file_with_backend(uploaded_file)
            
            if analysis_result and analysis_result.get('success'):
                charts = analysis_result.get('charts', [])
                analysis = analysis_result.get('analysis', {})
                llm_insights = analysis_result.get('llm_insights', '')
                
                # Display charts
                display_charts(charts)
                
                # Display analysis
                display_analysis(analysis, llm_insights)
            else:
                st.error("Failed to analyze the dataset. Please check your file format.")
        
        with tab3:
            # PDF Report generation
            st.subheader("📄 Generate PDF Report")
            st.write("Generate a comprehensive PDF report with all analysis and visualizations.")
            
            if st.button("🔄 Generate PDF Report", type="primary"):
                with st.spinner("Generating PDF report..."):
                    pdf_content = download_pdf_report(uploaded_file)
                
                if pdf_content:
                    st.success("✅ PDF report generated successfully!")
                    
                    # Create download button
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_content,
                        file_name=f"autodashboard_report_{uploaded_file.name.split('.')[0]}.pdf",
                        mime="application/pdf"
                    )
                    
                    st.info("💡 The PDF report includes:")
                    st.write("• Executive summary with AI insights")
                    st.write("• Dataset overview and data quality assessment")
                    st.write("• All generated visualizations")
                    st.write("• Statistical analysis")
                    st.write("• Categorical analysis")
                else:
                    st.error("Failed to generate PDF report.")
    
    else:
        # Welcome message when no file is uploaded
        st.markdown("""
        ## 🚀 Welcome to AutoDashboard!
        
        **Upload your CSV or Excel file to get started with:**
        
        - 📊 **Interactive Visualizations** - Beautiful charts and graphs
        - 🧠 **AI-Powered Analysis** - Insights from Google Gemini
        - 📋 **Data Quality Assessment** - Missing values, data types, and more
        - 📄 **Comprehensive Reports** - Downloadable PDF with full analysis
        
        ### How it works:
        1. **Upload** your dataset (CSV or Excel)
        2. **Explore** the overview and data quality
        3. **View** interactive visualizations
        4. **Download** a comprehensive PDF report
        
        ### Supported Features:
        - ✅ Data cleaning and preprocessing
        - ✅ Multiple chart types (histograms, correlations, box plots, etc.)
        - ✅ Statistical analysis
        - ✅ AI-powered insights
        - ✅ Professional PDF reports
        """)
        
        # Example datasets
        st.subheader("📁 Example Datasets")
        st.write("Try uploading one of these sample datasets:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Sales Data**")
            st.write("• Revenue trends")
            st.write("• Product performance")
            st.write("• Customer analysis")
        
        with col2:
            st.write("**Financial Data**")
            st.write("• Stock prices")
            st.write("• Market trends")
            st.write("• Risk analysis")
        
        with col3:
            st.write("**Survey Data**")
            st.write("• Customer satisfaction")
            st.write("• Demographics")
            st.write("• Response patterns")

if __name__ == "__main__":
    main() 