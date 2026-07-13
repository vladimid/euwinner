# EUWINNER Documentation Index

## 📚 Where to Start

### For Quick Setup (5 minutes)
👉 **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**
- 3-step startup
- Common commands
- API curl examples

### For Complete Implementation Guide (30 minutes)
👉 **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)**
- Full getting started guide
- All API endpoints
- Example API calls
- Next integration steps
- Troubleshooting

### For API Reference (detailed)
👉 **[RANDOM_NUMBERS_CONTROLLER_GUIDE.md](RANDOM_NUMBERS_CONTROLLER_GUIDE.md)**
- Complete API documentation
- All endpoint parameters
- Request/response examples
- Error handling details

---

## 📖 Documentation by Topic

### Getting Started
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick start card (5 min)
- [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) - Full setup guide (30 min)

### API Documentation
- [RANDOM_NUMBERS_CONTROLLER_GUIDE.md](RANDOM_NUMBERS_CONTROLLER_GUIDE.md) - API reference
- [ADD_WEB_FRAMEWORK.md](ADD_WEB_FRAMEWORK.md) - Framework setup patterns

### Migration & Planning
- [MIGRATION_PLAN.md](MIGRATION_PLAN.md) - Java to Python strategy
- [PLAN.md](PLAN.md) - Original migration plan
- [INNITIAL_PLAN.md](INNITIAL_PLAN.md) - Initial planning

### Implementation Details
- [CONTROLLER_GENERATION_SUMMARY.md](CONTROLLER_GENERATION_SUMMARY.md) - Implementation summary
- [GENERATION_CHECKLIST.md](GENERATION_CHECKLIST.md) - Verification checklist

---

## 🚀 Quick Commands

```bash
# Setup
cd /Users/vlada/sandbox/python/euwinner
source venv/bin/activate
pip install -r requirements.txt

# Run
uvicorn euwin.api.main:app --reload

# Test
pytest tests/ -v

# Access API
# http://localhost:8000/docs
```

---

## 📁 Key Files

### Controllers (API Endpoints)
- `euwin/api/routes/random_numbers_controller.py` - Random number endpoints
- `euwin/api/routes/system_controller.py` - System info endpoints
- `euwin/api/routes/data_controller.py` - Data management (template)
- `euwin/api/routes/analysis_controller.py` - Analysis (template)

### Core Application
- `euwin/api/main.py` - FastAPI app configuration
- `euwin/exception/__init__.py` - Custom exceptions
- `euwin/cqrs/__init__.py` - Domain models

### Testing
- `tests/conftest.py` - Pytest configuration & fixtures
- `tests/test_api/test_random_numbers_controller.py` - API tests (30+ tests)

### Configuration
- `pyproject.toml` - Project metadata & build config
- `requirements.txt` - Python dependencies

---

## 🎯 API Endpoints

### Random Numbers (`/api/random`)
- `POST /generate` - Generate single set
- `POST /generate-bulk` - Bulk generation
- `POST /validate` - Validate numbers
- `GET /sequential` - Sequential numbers
- `GET /range-info` - Range statistics
- `POST /seed-generate` - Reproducible generation

### System (`/api/system`)
- `GET /health` - Health check
- `GET /status` - System status
- `GET /info` - App info
- `GET /config` - Configuration
- `GET /version` - Version

### Root Endpoints
- `GET /` - Welcome message
- `GET /health` - Health status

---

## 🧪 Testing

```bash
# All tests
pytest tests/ -v

# With coverage
pytest --cov=euwin

# Specific test
pytest tests/test_api/test_random_numbers_controller.py -v

# Specific test class
pytest tests/test_api/test_random_numbers_controller.py::TestGenerateRandomNumbers -v
```

---

## 📊 Project Structure

```
euwinner/
├── euwin/                          # Main package
│   ├── api/
│   │   ├── main.py                # FastAPI app
│   │   └── routes/
│   │       ├── random_numbers_controller.py  (354 lines, 6 endpoints)
│   │       ├── system_controller.py         (160 lines, 5 endpoints)
│   │       ├── data_controller.py
│   │       └── analysis_controller.py
│   ├── analysis/                  # Analysis algorithms
│   ├── process/                   # Business logic
│   ├── validate/                  # Validation
│   ├── exception/                 # Custom exceptions
│   ├── cqrs/                      # Domain models
│   └── utils/                     # Utilities
├── tests/                         # Test suite
│   ├── conftest.py                # Pytest config
│   └── test_api/
│       └── test_random_numbers_controller.py  (30+ tests)
├── pyproject.toml                 # Build config
├── requirements.txt               # Dependencies
└── README.md
```

---

## 🎯 Development Workflow

1. **Setup** (see QUICK_REFERENCE.md)
2. **Explore API** - Visit http://localhost:8000/docs
3. **Run Tests** - `pytest tests/ -v`
4. **Implement Logic** - Add to `euwin/process/` and `euwin/analysis/`
5. **Test Changes** - Write tests in `tests/test_api/`
6. **Deploy** - Use Docker (see ADD_WEB_FRAMEWORK.md)

---

## 💡 Key Concepts

### Pydantic Models
Used for request/response validation. Examples:
- `RandomNumbersRequest`
- `RandomNumbersResponse`
- `BulkRandomGenerationRequest`
- `RandomNumberValidationRequest`

### Exception Hierarchy
Custom exceptions in `euwin/exception/`:
- `EUWinnerException` - Base exception
- `InvalidCombinationException`
- `InvalidDrawException`
- `InvalidNumbersException`
- `DataAccessException`

### Domain Models
CQRS models in `euwin/cqrs/`:
- `Draw` - Draw information
- `DrawEntry` - Individual draw entry
- `Combination` - Lottery combination

---

## 🔍 Finding Information

### "How do I..."

**Start the server?**
→ QUICK_REFERENCE.md, line "## 🚀 Start Development"

**Test the API?**
→ IMPLEMENTATION_GUIDE.md, line "## 🧪 Example API Calls"

**Understand all endpoints?**
→ RANDOM_NUMBERS_CONTROLLER_GUIDE.md, line "## API Endpoints"

**Set up the database?**
→ IMPLEMENTATION_GUIDE.md, line "## 📝 Next Integration Steps"

**Add more endpoints?**
→ IMPLEMENTATION_GUIDE.md, line "## 🔧 Development Workflow"

**Deploy to production?**
→ ADD_WEB_FRAMEWORK.md, line "## Step 8: Docker Setup"

**Fix a problem?**
→ IMPLEMENTATION_GUIDE.md, line "## 🆘 Troubleshooting"

---

## 📞 Support Resources

### Frameworks
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Pydantic Docs:** https://docs.pydantic.dev/
- **pytest Docs:** https://docs.pytest.org/

### Python Guides
- **Type Hints:** https://docs.python.org/3/library/typing.html
- **Async/Await:** https://docs.python.org/3/library/asyncio.html
- **SQLAlchemy:** https://docs.sqlalchemy.org/

### In This Project
- Check `euwin/api/routes/random_numbers_controller.py` for endpoint examples
- Check `tests/conftest.py` for test fixture examples
- Check `euwin/exception/__init__.py` for exception patterns

---

## ✅ Documentation Status

| Document | Status | Purpose |
|----------|--------|---------|
| QUICK_REFERENCE.md | ✅ Complete | Quick start (5 min) |
| IMPLEMENTATION_GUIDE.md | ✅ Complete | Full setup guide |
| RANDOM_NUMBERS_CONTROLLER_GUIDE.md | ✅ Complete | API reference |
| ADD_WEB_FRAMEWORK.md | ✅ Complete | Framework patterns |
| MIGRATION_PLAN.md | ✅ Complete | Migration strategy |
| README.md | ⏳ Needs update | Project overview |

---

## 🎓 Learning Path

### Day 1: Setup & Exploration
1. Read QUICK_REFERENCE.md (5 min)
2. Start server (5 min)
3. Explore API at http://localhost:8000/docs (10 min)
4. Run tests: `pytest tests/ -v` (5 min)

### Day 2: Understanding the Code
1. Read IMPLEMENTATION_GUIDE.md (30 min)
2. Read RANDOM_NUMBERS_CONTROLLER_GUIDE.md (20 min)
3. Test API endpoints with curl or Swagger (20 min)

### Day 3: Development
1. Review `euwin/api/routes/random_numbers_controller.py` (15 min)
2. Review `tests/test_api/test_random_numbers_controller.py` (15 min)
3. Start implementing business logic (2+ hours)

### Ongoing: Reference
- Use QUICK_REFERENCE.md for command reminders
- Use RANDOM_NUMBERS_CONTROLLER_GUIDE.md for API details
- Use IMPLEMENTATION_GUIDE.md for next steps

---

**Last Updated:** February 17, 2026
**Status:** ✅ Complete
**Framework:** FastAPI + Pydantic + pytest

