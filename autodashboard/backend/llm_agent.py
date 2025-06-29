# Placeholder for LLM agent logic using LangChain, LangGraph, and Gemini

import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langgraph.graph import StateGraph, END
from typing import Dict, Any, List
import json

# Load environment variables from .env file (with error handling)
try:
    load_dotenv()
except Exception as e:
    print(f"⚠️  Warning: Could not load .env file: {e}")
    print("💡 You can set GOOGLE_API_KEY as an environment variable instead")

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your-api-key-here":
    print("⚠️  Warning: GOOGLE_API_KEY not set. LLM features will be disabled.")
    print("💡 Set it as environment variable: set GOOGLE_API_KEY=your-key")

def setup_gemini():
    """Setup Google Gemini API"""
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your-api-key-here":
        print("❌ Google Gemini API key not configured. Please set GOOGLE_API_KEY in .env file")
        return None
    
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        return model
    except Exception as e:
        print(f"❌ Error setting up Gemini: {e}")
        return None

def setup_langchain_gemini():
    """Setup LangChain with Google Gemini"""
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your-api-key-here":
        print("❌ Google Gemini API key not configured. Please set GOOGLE_API_KEY in .env file")
        return None
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.3,
            max_tokens=2048
        )
        return llm
    except Exception as e:
        print(f"❌ Error setting up LangChain Gemini: {e}")
        return None

def create_analysis_prompt():
    """Create prompt template for data analysis"""
    template = """
    You are a professional data analyst. Analyze the following dataset information and provide comprehensive insights.
    
    Dataset Information:
    {dataset_info}
    
    Analysis Summary:
    {analysis_summary}
    
    Please provide:
    1. Key insights about the data
    2. Patterns and trends identified
    3. Potential business implications
    4. Recommendations for further analysis
    5. Data quality assessment
    
    Format your response in a clear, structured manner with bullet points and sections.
    """
    
    return PromptTemplate(
        input_variables=["dataset_info", "analysis_summary"],
        template=template
    )

def create_chart_analysis_prompt():
    """Create prompt template for chart analysis"""
    template = """
    You are a data visualization expert. Analyze the following chart and provide insights.
    
    Chart Information:
    - Type: {chart_type}
    - Title: {chart_title}
    - Data Summary: {data_summary}
    
    Please provide:
    1. What this chart shows
    2. Key patterns or trends visible
    3. Notable outliers or anomalies
    4. Business implications
    5. Suggestions for additional analysis
    
    Keep your analysis concise but insightful.
    """
    
    return PromptTemplate(
        input_variables=["chart_type", "chart_title", "data_summary"],
        template=template
    )

def analyze_with_llm(analysis_data: Dict[str, Any]) -> str:
    """Analyze data using LLM and return insights"""
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your-api-key-here":
        return """🤖 LLM Analysis (API Key Required)

To enable AI-powered analysis, please:
1. Get a Google Gemini API key from: https://makersuite.google.com/app/apikey
2. Add it to your .env file: GOOGLE_API_KEY=your-actual-api-key
3. Restart the application

For now, here's a basic analysis of your data:
- Dataset has {rows} rows and {columns} columns
- Numeric columns: {numeric_cols}
- Categorical columns: {categorical_cols}
- Missing values detected in: {missing_cols}

Consider exploring the visualizations tab for detailed insights.""".format(
            rows=analysis_data.get('dataset_info', {}).get('rows', 'N/A'),
            columns=analysis_data.get('dataset_info', {}).get('columns', 'N/A'),
            numeric_cols=len(analysis_data.get('numeric_summary', {})),
            categorical_cols=len(analysis_data.get('categorical_summary', {})),
            missing_cols=[col for col, count in analysis_data.get('missing_values', {}).items() if count > 0]
        )
    
    try:
        llm = setup_langchain_gemini()
        if not llm:
            return "LLM analysis not available. Please check API configuration."
        
        # Create analysis prompt
        prompt = create_analysis_prompt()
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Prepare data for analysis
        dataset_info = f"""
        - Rows: {analysis_data.get('dataset_info', {}).get('rows', 'N/A')}
        - Columns: {analysis_data.get('dataset_info', {}).get('columns', 'N/A')}
        - Memory Usage: {analysis_data.get('dataset_info', {}).get('memory_usage', 'N/A'):.2f} MB
        """
        
        analysis_summary = f"""
        - Numeric Columns: {list(analysis_data.get('numeric_summary', {}).keys())}
        - Categorical Columns: {list(analysis_data.get('categorical_summary', {}).keys())}
        - Missing Values: {analysis_data.get('missing_values', {})}
        """
        
        # Generate analysis
        result = chain.run({
            "dataset_info": dataset_info,
            "analysis_summary": analysis_summary
        })
        
        return result
        
    except Exception as e:
        return f"Error in LLM analysis: {str(e)}"

def analyze_chart_with_llm(chart_data: Dict[str, Any], data_summary: str) -> str:
    """Analyze individual chart using LLM"""
    try:
        llm = setup_langchain_gemini()
        if not llm:
            return "LLM analysis not available for this chart."
        
        # Create chart analysis prompt
        prompt = create_chart_analysis_prompt()
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Generate chart analysis
        result = chain.run({
            "chart_type": chart_data.get("type", "Unknown"),
            "chart_title": chart_data.get("title", "Unknown"),
            "data_summary": data_summary
        })
        
        return result
        
    except Exception as e:
        return f"Error in chart analysis: {str(e)}"

def create_analysis_workflow():
    """Create LangGraph workflow for comprehensive analysis"""
    
    def analyze_dataset(state):
        """Analyze the dataset"""
        analysis_data = state.get("analysis_data", {})
        insights = analyze_with_llm(analysis_data)
        state["llm_insights"] = insights
        return state
    
    def analyze_charts(state):
        """Analyze individual charts"""
        charts = state.get("charts", [])
        chart_insights = []
        
        for chart in charts:
            insight = analyze_chart_with_llm(chart, "Chart data analysis")
            chart_insights.append({
                "chart_title": chart.get("title", "Unknown"),
                "insight": insight
            })
        
        state["chart_insights"] = chart_insights
        return state
    
    def generate_summary(state):
        """Generate final summary"""
        llm = setup_langchain_gemini()
        if not llm:
            state["final_summary"] = "Summary generation not available."
            return state
        
        summary_prompt = PromptTemplate(
            input_variables=["insights", "chart_insights"],
            template="""
            Create a comprehensive executive summary based on the following analysis:
            
            Dataset Insights:
            {insights}
            
            Chart Analysis:
            {chart_insights}
            
            Provide a concise executive summary highlighting the most important findings and recommendations.
            """
        )
        
        chain = LLMChain(llm=llm, prompt=summary_prompt)
        
        insights = state.get("llm_insights", "")
        chart_insights = state.get("chart_insights", [])
        
        chart_summary = "\n".join([f"- {ci['chart_title']}: {ci['insight'][:100]}..." for ci in chart_insights])
        
        summary = chain.run({
            "insights": insights,
            "chart_insights": chart_summary
        })
        
        state["final_summary"] = summary
        return state
    
    # Create workflow
    workflow = StateGraph(name="data_analysis_workflow")
    
    # Add nodes
    workflow.add_node("analyze_dataset", analyze_dataset)
    workflow.add_node("analyze_charts", analyze_charts)
    workflow.add_node("generate_summary", generate_summary)
    
    # Add edges
    workflow.add_edge("analyze_dataset", "analyze_charts")
    workflow.add_edge("analyze_charts", "generate_summary")
    workflow.add_edge("generate_summary", END)
    
    return workflow.compile()

def run_comprehensive_analysis(analysis_data: Dict[str, Any], charts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run comprehensive analysis using LangGraph workflow"""
    try:
        workflow = create_analysis_workflow()
        
        # Prepare initial state
        initial_state = {
            "analysis_data": analysis_data,
            "charts": charts
        }
        
        # Run workflow
        result = workflow.invoke(initial_state)
        
        return {
            "dataset_insights": result.get("llm_insights", ""),
            "chart_insights": result.get("chart_insights", []),
            "executive_summary": result.get("final_summary", "")
        }
        
    except Exception as e:
        return {
            "dataset_insights": f"Error in comprehensive analysis: {str(e)}",
            "chart_insights": [],
            "executive_summary": "Analysis failed due to technical issues."
        } 