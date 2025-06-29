from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import io
import base64
import json
import plotly.io as pio
from typing import Dict, List, Any
import tempfile
import os

def create_pdf_report(analysis: Dict[str, Any], charts: List[Dict[str, Any]], llm_analysis: str) -> bytes:
    """Create a comprehensive PDF report with charts and analysis"""
    
    # Create buffer for PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    # Build PDF content
    story = []
    
    # Title
    story.append(Paragraph("AutoDashboard Report", title_style))
    story.append(Spacer(1, 20))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph(llm_analysis, normal_style))
    story.append(Spacer(1, 20))
    
    # Dataset Overview
    story.append(Paragraph("Dataset Overview", heading_style))
    
    dataset_info = analysis.get('dataset_info', {})
    overview_data = [
        ['Metric', 'Value'],
        ['Number of Rows', str(dataset_info.get('rows', 'N/A'))],
        ['Number of Columns', str(dataset_info.get('columns', 'N/A'))],
        ['Memory Usage (MB)', f"{dataset_info.get('memory_usage', 0):.2f}"],
    ]
    
    overview_table = Table(overview_data, colWidths=[2*inch, 3*inch])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(overview_table)
    story.append(Spacer(1, 20))
    
    # Data Types and Missing Values
    story.append(Paragraph("Data Quality Assessment", heading_style))
    
    # Data types table
    data_types = analysis.get('data_types', {})
    if data_types:
        dtype_data = [['Column', 'Data Type']]
        for col, dtype in list(data_types.items())[:10]:  # Limit to first 10
            dtype_data.append([col, str(dtype)])
        
        dtype_table = Table(dtype_data, colWidths=[2.5*inch, 2.5*inch])
        dtype_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(Paragraph("Data Types:", normal_style))
        story.append(dtype_table)
        story.append(Spacer(1, 15))
    
    # Missing values table
    missing_values = analysis.get('missing_values', {})
    if missing_values:
        missing_data = [['Column', 'Missing Values']]
        for col, count in list(missing_values.items())[:10]:  # Limit to first 10
            if count > 0:
                missing_data.append([col, str(count)])
        
        if len(missing_data) > 1:
            missing_table = Table(missing_data, colWidths=[2.5*inch, 2.5*inch])
            missing_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightcoral),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(Paragraph("Missing Values:", normal_style))
            story.append(missing_table)
            story.append(Spacer(1, 20))
    
    # Charts and Visualizations
    story.append(Paragraph("Data Visualizations", heading_style))
    
    for i, chart in enumerate(charts[:6]):  # Limit to first 6 charts
        try:
            # Chart title
            story.append(Paragraph(f"Chart {i+1}: {chart.get('title', 'Untitled')}", heading_style))
            
            # Convert plotly chart to image
            chart_json = chart.get('plot', '{}')
            if chart_json:
                fig = pio.from_json(chart_json)
                
                # Save chart as temporary image
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                    fig.write_image(tmp_file.name, width=600, height=400)
                    
                    # Add image to PDF
                    img = Image(tmp_file.name, width=5*inch, height=3.5*inch)
                    story.append(img)
                    
                    # Clean up temporary file
                    os.unlink(tmp_file.name)
            
            story.append(Spacer(1, 15))
            
        except Exception as e:
            story.append(Paragraph(f"Error displaying chart: {str(e)}", normal_style))
            story.append(Spacer(1, 15))
    
    # Statistical Summary
    story.append(Paragraph("Statistical Summary", heading_style))
    
    numeric_summary = analysis.get('numeric_summary', {})
    if numeric_summary:
        for col, stats in list(numeric_summary.items())[:5]:  # Limit to first 5 columns
            story.append(Paragraph(f"Column: {col}", normal_style))
            
            stats_data = [['Statistic', 'Value']]
            for stat, value in stats.items():
                if isinstance(value, (int, float)):
                    stats_data.append([stat, f"{value:.2f}"])
                else:
                    stats_data.append([stat, str(value)])
            
            stats_table = Table(stats_data, colWidths=[2*inch, 3*inch])
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(stats_table)
            story.append(Spacer(1, 15))
    
    # Categorical Analysis
    categorical_summary = analysis.get('categorical_summary', {})
    if categorical_summary:
        story.append(Paragraph("Categorical Analysis", heading_style))
        
        for col, summary in list(categorical_summary.items())[:3]:  # Limit to first 3 columns
            story.append(Paragraph(f"Column: {col}", normal_style))
            
            cat_data = [['Metric', 'Value']]
            cat_data.append(['Unique Values', str(summary.get('unique_values', 'N/A'))])
            cat_data.append(['Most Common', str(summary.get('most_common', 'N/A'))])
            
            cat_table = Table(cat_data, colWidths=[2*inch, 3*inch])
            cat_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightyellow),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(cat_table)
            story.append(Spacer(1, 15))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer.getvalue()

def create_simple_pdf_report(analysis: str, charts: list, llm_analysis: str) -> bytes:
    """Create a simple PDF report (fallback)"""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "AutoDashboard Report")
    
    # Analysis
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Data Analysis:")
    
    # Split analysis into lines
    lines = analysis.split('\n')
    y_position = 700
    for line in lines[:20]:  # Limit lines
        if y_position > 100:
            c.drawString(120, y_position, line[:80])  # Limit line length
            y_position -= 15
    
    # LLM Analysis
    y_position -= 20
    c.drawString(100, y_position, "LLM Insights:")
    y_position -= 15
    
    llm_lines = llm_analysis.split('\n')
    for line in llm_lines[:15]:  # Limit lines
        if y_position > 100:
            c.drawString(120, y_position, line[:80])  # Limit line length
            y_position -= 15
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue() 