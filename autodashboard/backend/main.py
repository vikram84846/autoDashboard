from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import io
import tempfile
import os
from typing import Dict, Any
import json

from .analysis import clean_data, generate_visualizations, analyze_data
from .llm_agent import analyze_with_llm
from .pdf_report import create_pdf_report

app = FastAPI(title="AutoDashboard API", version="1.0.0")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "AutoDashboard API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload CSV or Excel file and return initial data summary"""
    try:
        # Read file content
        content = await file.read()
        
        # Parse based on file type
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Clean data
        df_cleaned = clean_data(df)
        
        # Generate basic summary
        summary = {
            "filename": file.filename,
            "rows": len(df_cleaned),
            "columns": len(df_cleaned.columns),
            "column_names": df_cleaned.columns.tolist(),
            "data_types": df_cleaned.dtypes.astype(str).to_dict(),
            "missing_values": df_cleaned.isnull().sum().to_dict(),
            "numeric_columns": df_cleaned.select_dtypes(include=['number']).columns.tolist(),
            "categorical_columns": df_cleaned.select_dtypes(include=['object']).columns.tolist()
        }
        
        return {"success": True, "summary": summary}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    """Analyze uploaded file and generate visualizations"""
    try:
        # Read and clean data
        content = await file.read()
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        df_cleaned = clean_data(df)
        
        # Generate visualizations
        charts = generate_visualizations(df_cleaned)
        
        # Generate data analysis
        analysis = analyze_data(df_cleaned)
        
        # Get LLM insights
        llm_analysis = analyze_with_llm(analysis)
        
        return {
            "success": True,
            "charts": charts,
            "analysis": analysis,
            "llm_insights": llm_analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing file: {str(e)}")

@app.post("/generate-pdf")
async def generate_pdf_report(file: UploadFile = File(...)):
    """Generate and return PDF report"""
    try:
        # Read and analyze data
        content = await file.read()
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        df_cleaned = clean_data(df)
        charts = generate_visualizations(df_cleaned)
        analysis = analyze_data(df_cleaned)
        llm_analysis = analyze_with_llm(analysis)
        
        # Generate PDF
        pdf_content = create_pdf_report(analysis, charts, llm_analysis)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_content)
            tmp_file_path = tmp_file.name
        
        return FileResponse(
            tmp_file_path,
            media_type='application/pdf',
            filename=f"autodashboard_report_{file.filename.split('.')[0]}.pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000) 