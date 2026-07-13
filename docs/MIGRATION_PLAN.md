# Java to Python Migration Plan - High-Level Overview

## Migration Summary
Convert the EUWin lottery wheeling system from Java (Spring Boot 3.4.1) to Python, maintaining all functionality across REST APIs, batch processing, database persistence, and analysis modules.

---

## 1. **Define Python Tech Stack**
- **Web Framework**: FastAPI or Flask (REST APIs & HTTP routing)
- **Batch Processing**: Celery + Redis/RabbitMQ OR APScheduler (for scheduled tasks)
- **Data Persistence**: 
  - SQLAlchemy (replaces Spring Data JPA for MariaDB)
  - MongoEngine or PyMongo (for MongoDB)
- **Testing**: pytest (replaces JUnit 5)
- **Configuration**: Python config files, `.env` for environment variables
- **Async Support**: Native async/await (FastAPI recommendation)

---

## 2. **Map Java Packages to Python Modules**
```
Python Project Structure:
├── app/
│   ├── api/               # REST endpoints (controllers)
│   ├── process/           # Business logic (wheeling, combinations)
│   ├── analysis/          # Analysis modules (frequency, patterns)
│   ├── validate/          # Validation logic
│   ├── models/            # Data models (CQRS domain objects)
│   ├── utils/             # Utility functions
│   ├── exceptions.py      # Custom exceptions
│   └── config.py          # Configuration
├── tests/                 # Test suite
├── requirements.txt       # Dependencies
├── docker-compose.yml     # Services (MongoDB, MariaDB)
└── main.py               # Application entry point
```

---

## 3. **Convert Data Models & Persistence Layer**
- **Models**: Java Records/Classes → Python dataclasses or Pydantic models
  - `Draw`, `DrawEntry`, `Combination` classes
  - Validation decorators in Pydantic
- **Repositories**: Spring Data JPA → SQLAlchemy ORM
  - `DrawRepository` → SQLAlchemy query builder
  - Custom repository methods with proper SQL/document queries
- **MongoDB**: Configure MongoEngine connection strings and schemas

---

## 4. **Implement REST API Endpoints**
Recreate all controllers as route handlers:
- `SystemController` → `/system` routes
- `DataController` → `/data` routes  
- `RandomNumbersController` → `/random` routes
- `AnalysisController` → `/analysis` routes

Features:
- Request/response validation with Pydantic
- Dependency injection patterns (FastAPI services)
- Error handling and proper HTTP status codes
- Optional: Pagination support (as noted in TODO)

---

## 5. **Port Core Business Logic**
- **Process modules**: `WheelingSystemBuilder`, `CombinationBuilder`, `RandomNumbersGenerator`
- **Validation modules**: `CombinationValidation`, `SchemaValidation`
- **Analysis modules**: `SingleNumberFrequency`, `DrawnTogether`, `AnalysePastDraws*`
- **File I/O**: Replace Java file reading with pandas/csv libraries

---

## 6. **Configure Async/Batch Processing**
- Set up Celery task queue OR APScheduler for:
  - Periodic draw analysis
  - CSV data imports
  - Combination generation
- Maintain feature parity with Spring Batch capabilities

---

## 7. **Adapt Configuration & Environment**
- Replace `application.yml` / `application.properties` with Python config
- Use `.env` file for secrets (database URLs, API keys)
- Configure Python logging (replaces Logback)
- Docker Compose for database services

---

## 8. **Convert Test Suite**
- JUnit 5 → pytest framework
- TestContainers → testcontainers-python or Docker fixtures
- `@Mock` annotations → `unittest.mock` or `pytest-mock`
- Preserve test data (CSV files in `resources/`)

---

## 9. **Build & Deployment**
- **Dependency management**: `requirements.txt` or `pyproject.toml` (Poetry)
- **Docker**: Create Dockerfile for Python app
- **Server**: Gunicorn/Uvicorn for WSGI/ASGI
- **Docker Compose**: Update to include Python app + databases

---

## Key Decisions to Make

1. **Framework Choice**: FastAPI (recommended for async) vs Flask (lighter-weight)
2. **Database**: Continue with both MongoDB + MariaDB, or consolidate?
3. **Batch Orchestration**: Celery (distributed) vs APScheduler (simpler)?
4. **Frontend**: Keep Thymeleaf templates, migrate to Jinja2, or decouple as separate frontend?
5. **UI Migration**: HTML templates → Python Jinja2, or REST-only API?

---

## Migration Path (Suggested)
1. Set up Python project structure & dependencies
2. Create data models & database configuration
3. Implement core business logic modules
4. Build REST API endpoints
5. Configure batch processing
6. Migrate and adapt test suite
7. Docker & deployment setup
8. Testing & refinement


