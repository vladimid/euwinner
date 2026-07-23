# How to Add a Python Web Framework to Your Project

This guide covers adding Flask or FastAPI to your existing Python project, with a focus on your EUWINNER lottery wheeling system migration.

## Quick Start Comparison

| Aspect | Flask | FastAPI |
|--------|-------|---------|
| **Learning Curve** | Easy | Moderate |
| **Performance** | Moderate | High (async/await) |
| **API Documentation** | Manual (via extensions) | Automatic (Swagger/ReDoc) |
| **Type Hints** | Optional | Required/Built-in |
| **Best For** | Rapid prototyping | Production APIs, modern async |
| **Your Use Case** | ✓ Good | ✓✓ Better (recommended) |

**Recommendation for EUWINNER**: FastAPI (better async support, auto-documentation, type safety)

---

## Step 1: Set Up Your Project Structure

Your final structure should look like:

```
euwinner/
├── requirements.txt           # Python dependencies
├── pyproject.toml            # (Optional) Poetry config
├── setup.py                  # (Optional) Package setup
├── README.md
├── euwin/                    # Your main package
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── data_controller.py
│   │   │   ├── analysis_controller.py
│   │   │   ├── random_numbers_controller.py
│   │   │   └── system_controller.py
│   │   └── main.py           # FastAPI/Flask app initialization
│   ├── analysis/             # Existing/future analysis logic
│   ├── process/              # Existing/future processing logic
│   ├── utils/                # Existing/future utilities
│   ├── validate/             # Existing/future validation
│   ├── exception/            # Existing/future exceptions
│   └── cqrs/                 # Existing/future CQRS models
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Pytest configuration & fixtures
│   ├── test_api/
│   ├── test_analysis/
│   └── fixtures/             # Test data (CSV, JSON files)
└── config/
    └── settings.py           # Configuration management
```

---

## Step 2: Install Dependencies

### Option A: Using pip with requirements.txt

**For FastAPI:**

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install FastAPI and dependencies
pip install fastapi uvicorn[standard] pydantic sqlalchemy pymongo pytest pytest-mock

# Save to requirements.txt
pip freeze > requirements.txt
```

**For Flask:**

```bash
python3 -m venv venv
source venv/bin/activate

pip install flask flask-cors flask-restx sqlalchemy pymongo pytest pytest-mock

pip freeze > requirements.txt
```

### Option B: Using Poetry (Recommended)

```bash
# Initialize Poetry project
poetry init

# Add dependencies
poetry add fastapi uvicorn[standard] pydantic sqlalchemy pymongo
poetry add --group dev pytest pytest-mock pytest-asyncio

# Install from lock file
poetry install
```

---

## Step 3: Create Your Web Framework App

### Option 1: FastAPI (Recommended for EUWINNER)

**File: `euwin/api/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app instance
app = FastAPI(
    title="EUWINNER API",
    description="Lottery Wheeling System",
    version="1.0.0"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers from your controllers
from euwin.api.routes import data_controller, analysis_controller, random_numbers_controller, system_controller

app.include_router(data_controller.router, prefix="/data", tags=["Data"])
app.include_router(analysis_controller.router, prefix="/analysis", tags=["Analysis"])
app.include_router(random_numbers_controller.router, prefix="/random", tags=["Random Numbers"])
app.include_router(system_controller.router, prefix="/system", tags=["System"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "EUWINNER Lottery Wheeling API"}

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

**File: `euwin/api/routes/data_controller.py`**

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Define request/response models
class DrawEntryRequest(BaseModel):
    draw_id: int
    numbers: List[int]
    bonus: Optional[int] = None

class DrawEntryResponse(BaseModel):
    draw_id: int
    numbers: List[int]
    bonus: Optional[int]

# Translate your Spring @RestController endpoints
@router.get("/draws/{draw_id}")
async def get_draw(draw_id: int):
    """Get a specific draw by ID"""
    try:
        # Your business logic here
        return DrawEntryResponse(draw_id=draw_id, numbers=[1,2,3], bonus=5)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/draws")
async def create_draw(draw: DrawEntryRequest):
    """Create a new draw entry"""
    # Your business logic here
    return draw
```

**File: `euwin/api/routes/analysis_controller.py`**

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class AnalysisRequest(BaseModel):
    draws: List[List[int]]
    number_range: int

class AnalysisResponse(BaseModel):
    most_frequent: List[int]
    least_frequent: List[int]
    drawn_together: dict

@router.post("/frequency")
async def analyze_frequency(request: AnalysisRequest):
    """Analyze number frequency from past draws"""
    try:
        # Call your analysis.SingleNumberFrequency logic
        return AnalysisResponse(
            most_frequent=[1,2,3],
            least_frequent=[45,46,47],
            drawn_together={}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Option 2: Flask

**File: `euwin/api/main.py`**

```python
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Import blueprints from your controllers
from euwin.api.routes import data_controller, analysis_controller

app.register_blueprint(data_controller.bp)
app.register_blueprint(analysis_controller.bp)

@app.route("/")
def index():
    return jsonify({"message": "EUWINNER Lottery Wheeling API"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
```

**File: `euwin/api/routes/data_controller.py`**

```python
from flask import Blueprint, jsonify, request

bp = Blueprint('data', __name__, url_prefix='/api/data')

@bp.route('/draws/<int:draw_id>', methods=['GET'])
def get_draw(draw_id):
    """Get a specific draw by ID"""
    try:
        return jsonify({"draw_id": draw_id, "numbers": [1,2,3], "bonus": 5})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/draws', methods=['POST'])
def create_draw():
    """Create a new draw entry"""
    data = request.get_json()
    return jsonify(data), 201
```

---

## Step 4: Create Requirements File

**File: `requirements.txt`**

For **FastAPI setup**:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.4.2
sqlalchemy==2.0.23
pymongo==4.6.0
python-multipart==0.0.6
```

For **development & testing**:
```
pytest==7.4.3
pytest-mock==3.12.0
pytest-asyncio==0.21.1
pytest-cov==4.1.0
```

For **Optional utilities**:
```
pandas==2.1.3  # CSV processing
python-dotenv==1.0.0  # Environment variables
```

---

## Step 5: Create Configuration Management

**File: `euwin/config/settings.py`**

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = os.getenv("DEBUG", False)
    TESTING = os.getenv("TESTING", False)
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///euwinner.db")
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    DATABASE_URL = os.getenv("DATABASE_URL")
    MONGODB_URL = os.getenv("MONGODB_URL")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_URL = "sqlite:///test.db"
    MONGODB_URL = "mongodb://localhost:27017/test"

def get_config():
    env = os.getenv("ENVIRONMENT", "development")
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    return config_map.get(env, DevelopmentConfig)
```

**File: `.env` (add to .gitignore)**

```
ENVIRONMENT=development
DEBUG=True
DATABASE_URL=sqlite:///euwinner.db
MONGODB_URL=mongodb://localhost:27017
```

---

## Step 6: Run Your Application

### FastAPI

```bash
# Using uvicorn directly
uvicorn euwin.api.main:app --reload --host 0.0.0.0 --port 8000

# Auto-generated API docs available at:
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

### Flask

```bash
# Using Flask CLI
export FLASK_APP=euwin/api/main.py
export FLASK_ENV=development
flask run --port 8000

# Or directly
python -m flask --app euwin.api.main run
```

---

## Step 7: Set Up Testing

**File: `tests/conftest.py`**

```python
import pytest
from fastapi.testclient import TestClient
from euwin.api.main import app

@pytest.fixture
def client():
    """Test client for FastAPI"""
    return TestClient(app)

@pytest.fixture
def sample_draw_data():
    """Sample test data"""
    return {
        "draw_id": 1,
        "numbers": [1, 2, 3, 4, 5, 6],
        "bonus": 7
    }
```

**File: `tests/test_api/test_data_controller.py`**

```python
def test_get_draw(client):
    response = client.get("/data/draws/1")
    assert response.status_code == 200
    assert response.json()["draw_id"] == 1

def test_create_draw(client, sample_draw_data):
    response = client.post("/data/draws", json=sample_draw_data)
    assert response.status_code in [200, 201]
```

Run tests:
```bash
pytest tests/ -v
pytest tests/ --cov=euwin  # With coverage
```

---

## Step 8: Docker Setup (Optional)

**File: `Dockerfile`**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

CMD ["uvicorn", "euwin.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**File: `docker-compose.yml`**

```yaml
version: '3.9'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      MONGODB_URL: mongodb://mongo:27017
      DATABASE_URL: postgresql://user:password@postgres:5432/euwinner
    depends_on:
      - mongo
      - postgres

  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: euwinner
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
```

---

## Common Patterns for Your Migration

### 1. Translating Spring @RestController to FastAPI

```python
# Spring Java:
# @RestController
# @RequestMapping("/data")
# public class DataController {
#     @PostMapping
#     public ResponseEntity<DrawEntry> createDraw(@RequestBody DrawEntry draw) { ... }
# }

# FastAPI Python:
from fastapi import APIRouter
from pydantic import BaseModel

class DrawEntry(BaseModel):
    draw_id: int
    numbers: list[int]

router = APIRouter(prefix="/data")

@router.post("/")
def create_draw(draw: DrawEntry):
    return draw
```

### 2. Error Handling

```python
# FastAPI
from fastapi import HTTPException
from euwin.exception import InvalidCombinationException

@router.get("/combination/{id}")
async def get_combination(id: int):
    try:
        # Your business logic
        pass
    except InvalidCombinationException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

### 3. Dependency Injection (FastAPI)

```python
from fastapi import Depends

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/draws")
async def list_draws(db: Session = Depends(get_db)):
    return db.query(Draw).all()
```

---

## Checklist for Adding Web Framework

- [ ] Choose web framework (FastAPI recommended)
- [ ] Create virtual environment
- [ ] Install dependencies to `requirements.txt`
- [ ] Create `euwin/api/main.py` with app initialization
- [ ] Create `euwin/api/routes/` subdirectory with controller modules
- [ ] Define Pydantic models (FastAPI) or request/response classes
- [ ] Translate Spring @RestController classes to routes
- [ ] Add CORS middleware if needed
- [ ] Create configuration management (`config/settings.py`)
- [ ] Add environment variables (`.env`)
- [ ] Set up test fixtures and client
- [ ] Create `tests/` directory with test files
- [ ] Test all endpoints with `pytest`
- [ ] (Optional) Create `Dockerfile` and `docker-compose.yml`
- [ ] Update `README.md` with API documentation and setup instructions

---

## Next Steps for Your Project

1. **Translate your existing business logic** from `analysis/`, `process/`, `validate/` packages
2. **Create data access layer** using SQLAlchemy for MariaDB, pymongo for MongoDB
3. **Implement Pydantic models** from your existing CQRS data models
4. **Migrate test files** and data fixtures
5. **Deploy** using Docker or cloud platform

---

## Helpful Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **Flask**: https://flask.palletsprojects.com/
- **Pydantic**: https://docs.pydantic.dev/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pytest**: https://docs.pytest.org/

Good luck with your EUWINNER migration! 🎰

