# EUWINNER Quick Reference Card

## 🚀 Start Development (3 steps)

```bash
cd /Users/vlada/sandbox/python/euwinner
source venv/bin/activate
uvicorn euwin.api.main:app --reload
```
## 🚀 Start Development (5 steps, safer)
```bash
cd /Users/vlada/sandbox/python/euwinner
python3 -m venv .venv
source .venv/bin/activate
pip install -r euwin/requirements.txt
python -m uvicorn euwin.api.main:app --reload --host 0.0.0.0 --port 8000
**API Available at:** http://localhost:8000/docs
```
---

## 📝 Common Commands

### Running
```bash
# Start server
uvicorn euwin.api.main:app --reload --port 8000

# Run with different host
uvicorn euwin.api.main:app --host 0.0.0.0 --port 8000
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=euwin --cov-report=html

# Run specific test file
pytest tests/test_api/test_random_numbers_controller.py -v

# Run specific test class
pytest tests/test_api/test_random_numbers_controller.py::TestGenerateRandomNumbers -v
```

### Code Quality
```bash
# Format code
black euwin/ tests/

# Sort imports
isort euwin/ tests/

# Lint
flake8 euwin/ tests/

# Type check
mypy euwin/
```

---

## 🎯 API Endpoints Quick Reference

### Generate Random Numbers
```bash
curl -X POST http://localhost:8000/api/random/generate \
  -H "Content-Type: application/json" \
  -d '{"count": 6, "min_number": 1, "max_number": 49, "include_bonus": true, "bonus_range": 10}'
```

### Validate Numbers
```bash
curl -X POST http://localhost:8000/api/random/validate \
  -H "Content-Type: application/json" \
  -d '{"numbers": [3,15,27,35,41,48], "min_allowed": 1, "max_allowed": 49}'
```

### Get Range Info
```bash
curl http://localhost:8000/api/random/range-info?min_number=1&max_number=49
```

### Health Check
```bash
curl http://localhost:8000/health
```

---

## 📁 Project Structure

```
euwin/
├── api/               # REST endpoints
│   ├── main.py       # FastAPI app
│   └── routes/       # Controllers
├── process/          # Business logic (implement here)
├── analysis/         # Analysis algorithms (implement here)
├── validate/         # Validation (implement here)
├── exception/        # Custom exceptions
├── cqrs/            # Domain models
└── utils/           # Utilities

tests/
├── conftest.py      # Fixtures
└── test_api/        # API tests
```

---

## 🔧 Key Files to Know

| File | Purpose |
|------|---------|
| `euwin/api/main.py` | FastAPI app configuration |
| `euwin/api/routes/random_numbers_controller.py` | Random number endpoints |
| `tests/conftest.py` | Pytest fixtures & config |
| `tests/test_api/test_random_numbers_controller.py` | API tests |
| `pyproject.toml` | Project config |

---

## 📚 Documentation

- **IMPLEMENTATION_GUIDE.md** - Getting started & next steps
- **RANDOM_NUMBERS_CONTROLLER_GUIDE.md** - API reference
- **ADD_WEB_FRAMEWORK.md** - Framework patterns
- **MIGRATION_PLAN.md** - Java→Python migration plan

---

## 💡 Development Checklist

- [ ] Start server: `uvicorn euwin.api.main:app --reload`
- [ ] Run tests: `pytest tests/ -v`
- [ ] View API docs: http://localhost:8000/docs
- [ ] Create business logic in `euwin/process/`
- [ ] Set up database in `euwin/models/`
- [ ] Add repository layer in `euwin/repository/`
- [ ] Update controllers to use repositories
- [ ] Write integration tests
- [ ] Deploy with Docker

---

## 🆘 Quick Troubleshooting

```bash
# Module not found?
pip install -e .

# Port in use?
lsof -i :8000

# Need to reinstall deps?
pip install -r requirements.txt

# Pytest can't find modules?
pytest tests/ (from project root)
```

---

## 📊 Project Statistics

- **API Endpoints:** 11 (6 random numbers + 5 system)
- **Test Cases:** 30+
- **Type Coverage:** 100%
- **Documentation:** 4 guides

---

**Last Updated:** February 17, 2026
**Framework:** FastAPI + Pydantic + pytest
**Status:** ✅ Ready for Development

