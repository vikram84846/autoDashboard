import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset by handling missing values, duplicates, and data types"""
    # Make a copy to avoid modifying original
    df_clean = df.copy()
    
    # Remove completely empty rows and columns
    df_clean = df_clean.dropna(how='all')
    df_clean = df_clean.dropna(axis=1, how='all')
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
    # Handle missing values
    for col in df_clean.columns:
        if df_clean[col].dtype in ['object', 'string']:
            # For categorical columns, fill with mode
            mode_val = df_clean[col].mode()
            if len(mode_val) > 0:
                df_clean[col] = df_clean[col].fillna(mode_val[0])
            else:
                df_clean[col] = df_clean[col].fillna('Unknown')
        else:
            # For numeric columns, fill with median
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
    
    # Convert date columns if possible
    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':
            try:
                pd.to_datetime(df_clean[col])
                df_clean[col] = pd.to_datetime(df_clean[col])
            except:
                pass
    
    return df_clean

def analyze_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate comprehensive data analysis"""
    analysis = {
        "dataset_info": {
            "rows": len(df),
            "columns": len(df.columns),
            "memory_usage": df.memory_usage(deep=True).sum() / 1024 / 1024,  # MB
        },
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_summary": {},
        "categorical_summary": {},
        "correlations": {}
    }
    
    # Numeric columns analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        analysis["numeric_summary"] = df[numeric_cols].describe().to_dict()
        
        # Correlation matrix for numeric columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            analysis["correlations"] = corr_matrix.to_dict()
    
    # Categorical columns analysis
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols:
        value_counts = df[col].value_counts()
        analysis["categorical_summary"][col] = {
            "unique_values": len(value_counts),
            "top_values": value_counts.head(5).to_dict(),
            "most_common": value_counts.index[0] if len(value_counts) > 0 else None
        }
    
    return analysis

def generate_visualizations(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Generate comprehensive visualizations for the dataset"""
    charts = []
    
    # Get column types
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # 1. Data Overview Chart
    if len(numeric_cols) > 0:
        # Distribution plots for numeric columns
        for col in numeric_cols[:5]:  # Limit to first 5 numeric columns
            fig = px.histogram(df, x=col, title=f"Distribution of {col}", 
                             nbins=30, color_discrete_sequence=['#1f77b4'])
            fig.update_layout(
                width=400, height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False
            )
            charts.append({
                "type": "distribution",
                "title": f"Distribution of {col}",
                "plot": fig.to_json()
            })
    
    # 2. Correlation Heatmap
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        fig = px.imshow(
            corr_matrix,
            title="Correlation Heatmap",
            color_continuous_scale='RdBu',
            aspect="auto"
        )
        fig.update_layout(
            width=500, height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        charts.append({
            "type": "correlation",
            "title": "Correlation Heatmap",
            "plot": fig.to_json()
        })
    
    # 3. Box plots for numeric columns
    if len(numeric_cols) > 0:
        fig = px.box(df, y=numeric_cols[:5], title="Box Plots - Outlier Detection")
        fig.update_layout(
            width=600, height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        charts.append({
            "type": "boxplot",
            "title": "Box Plots - Outlier Detection",
            "plot": fig.to_json()
        })
    
    # 4. Categorical analysis
    if len(categorical_cols) > 0:
        for col in categorical_cols[:3]:  # Limit to first 3 categorical columns
            value_counts = df[col].value_counts().head(10)
            fig = px.bar(
                x=value_counts.index, 
                y=value_counts.values,
                title=f"Top 10 Values in {col}",
                labels={'x': col, 'y': 'Count'}
            )
            fig.update_layout(
                width=400, height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                showlegend=False
            )
            charts.append({
                "type": "categorical",
                "title": f"Top 10 Values in {col}",
                "plot": fig.to_json()
            })
    
    # 5. Scatter plot matrix for numeric columns
    if len(numeric_cols) >= 2:
        fig = px.scatter_matrix(
            df, 
            dimensions=numeric_cols[:4],  # Limit to first 4 columns
            title="Scatter Plot Matrix"
        )
        fig.update_layout(
            width=800, height=600,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        charts.append({
            "type": "scatter_matrix",
            "title": "Scatter Plot Matrix",
            "plot": fig.to_json()
        })
    
    # 6. Time series analysis (if datetime columns exist)
    if len(datetime_cols) > 0 and len(numeric_cols) > 0:
        time_col = datetime_cols[0]
        numeric_col = numeric_cols[0]
        
        # Sort by time
        df_time = df.sort_values(time_col)
        
        fig = px.line(
            df_time, 
            x=time_col, 
            y=numeric_col,
            title=f"Time Series: {numeric_col} over {time_col}"
        )
        fig.update_layout(
            width=600, height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        charts.append({
            "type": "timeseries",
            "title": f"Time Series: {numeric_col} over {time_col}",
            "plot": fig.to_json()
        })
    
    return charts

def get_chart_image_base64(fig) -> str:
    """Convert plotly figure to base64 image string"""
    img_bytes = fig.to_image(format="png")
    img_base64 = base64.b64encode(img_bytes).decode()
    return img_base64

# Add more analysis functions as needed 