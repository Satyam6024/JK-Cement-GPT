# AI RAG Agent for Multi-Format Data Analysis

Enterprise-grade RAG agent for comprehensive data analysis, visualization, and business intelligence.

## Features
- Multi-format data ingestion (CSV, XLSX, JSON, PDF, SQLite, Access DB, XML)
- Vector-based semantic search and retrieval
- AI-powered data analysis and business insights
- Automated visualization generation
- RESTful API with real-time processing
- Docker deployment ready

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your OpenAI API key

# Create directories
mkdir -p uploads outputs vector_db

# Run the application
python src/app.py
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## API Usage

### Upload File
```bash
curl -X POST -F "file=@data.csv" http://localhost:5000/api/upload
```

### Query Data
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"query": "What are the sales trends?", "analysis_type": "trend"}' \
  http://localhost:5000/api/query
```

### Get Insights
```bash
curl http://localhost:5000/api/insights/file-id-here
```

## Supported File Formats
- **Spreadsheets**: CSV, XLSX, XLS
- **Documents**: PDF, DOCX
- **Data**: JSON, XML
- **Databases**: SQLite, Access (ACCDB, MDB)
- **Others**: DAT, FDB

## Analysis Types
- **general**: General analysis and insights
- **statistical**: Statistical analysis with metrics
- **trend**: Trend analysis and predictions
- **comparative**: Comparative analysis between datasets

## Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │ -> │ Ingestion Layer │ -> │  Vector Store   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                ↓
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   REST API      │ <- │ Analysis Engine │ <- │   LLM Client    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Environment Variables
```
OPENAI_API_KEY=your_openai_api_key
FLASK_ENV=development
UPLOAD_FOLDER=./uploads
OUTPUT_FOLDER=./outputs
VECTOR_DB_PATH=./vector_db
MAX_FILE_SIZE=104857600
```

## Business Intelligence Features
- **Automated Data Profiling**: Quality assessment and validation
- **Trend Detection**: Identifies patterns and anomalies
- **Business Recommendations**: AI-generated strategic insights
- **Interactive Visualizations**: Charts and graphs for data exploration
- **Multi-source Analysis**: Combines insights across different data sources

## Production Considerations
- Use environment-specific configuration
- Implement proper logging and monitoring
- Set up proper database backups
- Configure SSL/TLS for HTTPS
- Implement rate limiting and authentication
- Use production WSGI server (Gunicorn)

## Testing
```bash
# Run unit tests
python -m pytest tests/

# Test individual components
python -m pytest tests/test_loaders.py
python -m pytest tests/test_api.py
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## License
MIT License - see LICENSE file for details

# ===== USAGE EXAMPLES =====

# Example 1: Upload and Analyze Sales Data
"""
1. Upload CSV file:
POST /api/upload
Content-Type: multipart/form-data
file: sales_data.csv

2. Query sales trends:
POST /api/query
{
  "query": "What are the monthly sales trends?",
  "analysis_type": "trend"
}

3. Get comprehensive insights:
GET /api/insights/file-id-from-upload
"""

# Example 2: Database Analysis
"""
1. Upload SQLite database:
POST /api/upload
Content-Type: multipart/form-data
file: company_db.sqlite

2. Query customer data:
POST /api/query
{
  "query": "Analyze customer demographics and purchasing behavior",
  "analysis_type": "statistical"
}
"""

# Example 3: Document Analysis
"""
1. Upload PDF report:
POST /api/upload
Content-Type: multipart/form-data
file: quarterly_report.pdf

2. Extract key insights:
POST /api/query
{
  "query": "Summarize key financial metrics and risks mentioned",
  "analysis_type": "general"
}
"""

# ===== DEPLOYMENT CHECKLIST =====
"""
Pre-deployment:
□ Set production environment variables
□ Configure OpenAI API key
□ Set up persistent storage volumes
□ Configure SSL certificates
□ Set up monitoring and logging
□ Test all API endpoints
□ Verify file upload limits
□ Test with sample data files

Production:
□ Use production WSGI server
□ Configure reverse proxy (nginx)
□ Set up database backups
□ Implement health checks
□ Configure auto-scaling
□ Set up error tracking
□ Monitor resource usage
□ Regular security updates
"""

# ===== PERFORMANCE OPTIMIZATION =====
"""
For large datasets:
1. Implement chunked processing
2. Use async processing for file uploads
3. Add caching layer (Redis)
4. Optimize vector database queries
5. Implement pagination for results
6. Use connection pooling for databases
7. Add background job processing (Celery)
8. Optimize memory usage for large files
"""