# Backend - Conversational AI Service

This is the backend service for the Think41 conversational AI platform.

## Quick Start

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**
   ```bash
   export DATABASE_URL="your_postgresql_connection_string"
   export XAI_API_KEY="your_xai_api_key"
   ```

3. **Load sample data**
   ```bash
   python -m backend.load_data
   ```

4. **Start the server**
   ```bash
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 5000 --reload
   ```

## API Documentation

Once running, visit:
- `http://localhost:5000/` - Service status
- `http://localhost:5000/docs` - Interactive API docs

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `XAI_API_KEY` - xAI API key from console.x.ai
- `GROQ_MODEL` - Model name (default: grok-2-1212)
- `DEBUG` - Development mode (default: False)

## Project Structure

```
backend/
├── __init__.py
├── main.py              # FastAPI application
├── config.py            # Configuration
├── database.py          # Database setup
├── models.py            # Data models
├── schemas.py           # API schemas
├── crud.py              # Database operations
├── chat_service.py      # AI chat logic
├── load_data.py         # Data loading
└── sample_products.csv  # Sample data
```