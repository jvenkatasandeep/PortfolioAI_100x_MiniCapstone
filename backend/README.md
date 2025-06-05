# PortfolioAI Backend

Backend service for the PortfolioAI application, built with FastAPI.

## Project Structure

```
backend/
├── app/                    # Application package
│   ├── api/                # API routes
│   ├── core/               # Core functionality
│   ├── database/           # Database models and operations
│   ├── models/             # Pydantic models
│   ├── services/           # Business logic
│   └── utils/              # Utility functions
├── tests/                  # Test files
├── instance/               # Instance-specific files (e.g., local database)
├── migrations/             # Database migrations
├── .env                    # Environment variables
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Project dependencies
└── run.py                 # Application entry point
```

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd portfolioai/backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .  # For development
   # or
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the backend directory with the required variables:
   ```
   DATABASE_URL=sqlite:///./portfolioai.db
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

## Running the Application

```bash
# Run the development server
python run.py

# Or using uvicorn directly
uvicorn app.main:app --reload --reload-dir=app
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests

```bash
pytest tests/
```

## Deployment

For production deployment, consider using:
- Gunicorn with Uvicorn workers
- Docker containers
- Cloud platforms like AWS, GCP, or Azure
