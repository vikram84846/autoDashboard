# AutoDashboard 📊

**Interactive Data Visualization & Analysis Platform**

## 🚀 Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **LLM & Agents**: LangChain, LangGraph, Google Gemini 2.0 Flash
- **Visualization**: Plotly, Seaborn, Matplotlib
- **Data Processing**: Pandas, NumPy
- **Report Generation**: ReportLab (PDF)
- **Package Management**: UV

## 📋 Features

- 📁 **File Upload**: Support for CSV and Excel files
- 🧹 **Data Cleaning**: Automatic handling of missing values, duplicates, and data types
- 📊 **Interactive Visualizations**: Multiple chart types with responsive grid layout
- 🧠 **AI-Powered Analysis**: Insights from Google Gemini using LangChain and LangGraph
- 📈 **Statistical Analysis**: Comprehensive data analysis and summaries
- 📄 **PDF Reports**: Downloadable professional reports with charts and analysis
- 🎨 **Beautiful UI**: Clean, modern interface with proper spacing and colors

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.11+
- UV package manager
- Google Gemini API key

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd AutoDashboard

# Create virtual environment and install dependencies
uv venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Unix/Mac

# Install dependencies
uv pip install -r pyproject.toml
```

### 2. Configure Google Gemini API

Set your Google Gemini API key as an environment variable:

```bash
# Windows
set GOOGLE_API_KEY=your-api-key-here

# Unix/Mac
export GOOGLE_API_KEY=your-api-key-here
```

**Get your API key from**: [Google AI Studio](https://makersuite.google.com/app/apikey)

### 3. Start the Application

#### Option A: Using the provided scripts

```bash
# Terminal 1: Start Backend
python run_backend.py

# Terminal 2: Start Frontend
python run_frontend.py
```

#### Option B: Manual startup

```bash
# Terminal 1: Start Backend
uvicorn autodashboard.backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Frontend
streamlit run autodashboard/frontend/app.py --server.port 8501
```

## 🌐 Access Points

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 Usage

### 1. Upload Your Data

- Navigate to http://localhost:8501
- Click "Browse files" in the sidebar
- Select your CSV or Excel file

### 2. Explore the Dashboard

- **Overview Tab**: See dataset summary and data quality metrics
- **Dashboard Tab**: View interactive visualizations and AI analysis
- **Report Tab**: Generate and download comprehensive PDF reports

### 3. Generated Visualizations

The system automatically creates:

- Distribution histograms for numeric columns
- Correlation heatmaps
- Box plots for outlier detection
- Bar charts for categorical data
- Scatter plot matrices
- Time series plots (if datetime columns exist)

### 4. AI Analysis

- Dataset insights and patterns
- Business implications
- Recommendations for further analysis
- Data quality assessment

## 🏗️ Project Structure

```
AutoDashboard/
├── autodashboard/
│   ├── backend/
│   │   ├── main.py          # FastAPI app with endpoints
│   │   ├── analysis.py      # Data cleaning and visualization
│   │   ├── llm_agent.py     # LangChain/LangGraph integration
│   │   └── pdf_report.py    # PDF generation
│   ├── frontend/
│   │   └── app.py           # Streamlit dashboard
│   └── shared/
│       └── utils.py         # Shared utilities
├── run_backend.py           # Backend startup script
├── run_frontend.py          # Frontend startup script
├── pyproject.toml           # Dependencies and project config
└── README.md               # This file
```

## 🔧 API Endpoints

- `GET /health` - Health check
- `POST /upload` - Upload and analyze file
- `POST /analyze` - Generate visualizations and analysis
- `POST /generate-pdf` - Create downloadable PDF report

## 🎨 Design Features

- **Responsive Grid Layout**: Charts are displayed in a clean grid format
- **Proper Spacing**: No overlapping content, well-organized sections
- **Color Scheme**: Professional blue theme with appropriate contrast
- **Interactive Elements**: Hover effects, expandable sections, tabs
- **Clean Typography**: Clear hierarchy and readable fonts

## 🧪 Testing

To test the application, you can use sample datasets:

1. **Sales Data**: Revenue, product performance, customer data
2. **Financial Data**: Stock prices, market trends, risk metrics
3. **Survey Data**: Customer satisfaction, demographics, responses

## 🔍 Troubleshooting

### Backend Issues

- Ensure all dependencies are installed: `uv pip install -r pyproject.toml`
- Check if port 8000 is available
- Verify Google API key is set correctly

### Frontend Issues

- Ensure backend is running before starting frontend
- Check if port 8501 is available
- Clear browser cache if UI doesn't load properly

### LLM Issues

- Verify Google Gemini API key is valid
- Check API quota and limits
- Ensure internet connection for API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- Streamlit for the beautiful frontend framework
- FastAPI for the robust backend
- Plotly for interactive visualizations
- LangChain for LLM orchestration
