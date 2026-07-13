# RandomNumbersController - FastAPI Implementation

## Overview

The `random_numbers_controller.py` module has been successfully generated for your EUWINNER lottery wheeling system. It provides a comprehensive set of REST API endpoints for random number generation, validation, and utility operations.

## File Structure

```
euwin/api/routes/
├── __init__.py                           # Package initialization
├── random_numbers_controller.py          # Random number generation endpoints (NEW)
├── data_controller.py                    # Data management endpoints
├── analysis_controller.py                # Analysis endpoints
└── system_controller.py                  # System health & info endpoints (NEW)
```

## API Endpoints

All endpoints are prefixed with `/api/random` as defined in `euwin/api/main.py`.

### 1. Generate Random Numbers
**Endpoint:** `POST /api/random/generate`

Generate a single set of random numbers within a specified range.

**Request:**
```json
{
  "count": 6,
  "min_number": 1,
  "max_number": 49,
  "include_bonus": true,
  "bonus_range": 10
}
```

**Response:**
```json
{
  "numbers": [3, 15, 27, 35, 41, 48],
  "bonus": 7,
  "count": 6,
  "seed": null
}
```

**Validation Rules:**
- `count`: 1-100 numbers (required)
- `min_number`: Minimum value in range (required, >= 1)
- `max_number`: Must be > min_number (required)
- `include_bonus`: Enable bonus number (default: false)
- `bonus_range`: Range for bonus if enabled (optional)

---

### 2. Generate Random Numbers in Bulk
**Endpoint:** `POST /api/random/generate-bulk`

Generate multiple sets of random numbers efficiently.

**Request:**
```json
{
  "generations": 10,
  "count": 6,
  "min_number": 1,
  "max_number": 49,
  "include_bonus": true,
  "bonus_range": 10
}
```

**Response:**
```json
{
  "results": [
    {
      "numbers": [3, 15, 27, 35, 41, 48],
      "bonus": 7,
      "count": 6,
      "seed": null
    },
    {
      "numbers": [5, 12, 19, 32, 43, 47],
      "bonus": 3,
      "count": 6,
      "seed": null
    }
  ],
  "total_sets": 10
}
```

**Use Case:** Generate multiple lottery draws at once.

---

### 3. Validate Random Numbers
**Endpoint:** `POST /api/random/validate`

Validate a set of numbers against specified criteria.

**Request:**
```json
{
  "numbers": [3, 15, 27, 35, 41, 48],
  "min_allowed": 1,
  "max_allowed": 49,
  "allow_duplicates": false
}
```

**Response:**
```json
{
  "is_valid": true,
  "errors": [],
  "total_numbers": 6
}
```

**Validation Checks:**
- Numbers within min/max range
- Duplicate detection (if not allowed)
- Empty list detection

---

### 4. Generate Sequential Numbers
**Endpoint:** `GET /api/random/sequential?count=10&start=1`

Generate sequential numbers starting from a given number.

**Query Parameters:**
- `count`: How many sequential numbers (1-100)
- `start`: Starting number

**Response:**
```json
{
  "numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  "count": 10
}
```

**Use Case:** Create number pools or ranges for lottery analysis.

---

### 5. Get Range Information
**Endpoint:** `GET /api/random/range-info?min_number=1&max_number=49`

Get statistical information about a number range.

**Query Parameters:**
- `min_number`: Minimum value in range
- `max_number`: Maximum value in range

**Response:**
```json
{
  "min": 1,
  "max": 49,
  "available_numbers": 49,
  "middle": 25.0,
  "sum": 1225
}
```

**Use Case:** Understand what random selections are possible from a range.

---

### 6. Generate with Seed (Reproducible)
**Endpoint:** `POST /api/random/seed-generate?seed=12345`

Generate random numbers using a specific seed for reproducibility.

**Request:**
```json
{
  "count": 6,
  "min_number": 1,
  "max_number": 49,
  "include_bonus": true,
  "bonus_range": 10
}
```

**Query Parameter:**
- `seed`: Random seed value (required, any integer)

**Response:**
```json
{
  "numbers": [3, 15, 27, 35, 41, 48],
  "bonus": 7,
  "count": 6,
  "seed": 12345
}
```

**Use Case:** Testing or creating reproducible lottery drawings.

---

## Data Models

### RandomNumbersRequest
```python
class RandomNumbersRequest(BaseModel):
    count: int                              # 1-100
    min_number: int                         # >= 1
    max_number: int                         # > min_number
    include_bonus: bool = False
    bonus_range: Optional[int] = None
```

### RandomNumbersResponse
```python
class RandomNumbersResponse(BaseModel):
    numbers: List[int]
    bonus: Optional[int]
    count: int
    seed: Optional[int]
```

### BulkRandomGenerationRequest / BulkRandomGenerationResponse
Similar to above but supports multiple generations in a single request.

### RandomNumberValidationRequest / RandomNumberValidationResponse
For validating number sets against criteria.

### SequentialNumbersRequest / SequentialNumbersResponse
For sequential number generation.

---

## Features

✅ **Input Validation** - Comprehensive validation using Pydantic Field constraints
✅ **Error Handling** - Proper HTTP status codes and detailed error messages
✅ **Bonus Number Support** - Optional bonus number generation with separate range
✅ **Bulk Operations** - Generate multiple sets efficiently in one request
✅ **Reproducibility** - Seeded generation for testing
✅ **Range Analysis** - Statistical information about number ranges
✅ **Type Safety** - Full type hints with Pydantic models
✅ **Auto Documentation** - Automatic Swagger/OpenAPI documentation
✅ **Async Support** - All endpoints are async-capable

---

## Integration with FastAPI App

The module is already integrated into your FastAPI application (`euwin/api/main.py`):

```python
from euwin.api.routes import random_numbers_controller

app.include_router(
    random_numbers_controller.router,
    prefix="/api/random",
    tags=["Random Numbers"]
)
```

---

## Error Handling Examples

### Invalid Range
**Request:** `min_number: 49, max_number: 1`
**Response (400):**
```json
{"detail": "min_number must be less than max_number"}
```

### Insufficient Available Numbers
**Request:** `count: 100, min_number: 1, max_number: 49`
**Response (400):**
```json
{"detail": "Cannot generate 100 unique numbers from range [1, 49]"}
```

### Server Error
**Response (500):**
```json
{"detail": "Error generating random numbers: <error message>"}
```

---

## Testing the Endpoints

### Using curl

```bash
# Generate random numbers
curl -X POST http://localhost:8000/api/random/generate \
  -H "Content-Type: application/json" \
  -d '{
    "count": 6,
    "min_number": 1,
    "max_number": 49,
    "include_bonus": true,
    "bonus_range": 10
  }'

# Get range info
curl http://localhost:8000/api/random/range-info?min_number=1&max_number=49

# Validate numbers
curl -X POST http://localhost:8000/api/random/validate \
  -H "Content-Type: application/json" \
  -d '{
    "numbers": [3, 15, 27, 35, 41, 48],
    "min_allowed": 1,
    "max_allowed": 49,
    "allow_duplicates": false
  }'
```

### Using Python requests

```python
import requests

# Generate random numbers
response = requests.post(
    'http://localhost:8000/api/random/generate',
    json={
        'count': 6,
        'min_number': 1,
        'max_number': 49,
        'include_bonus': True,
        'bonus_range': 10
    }
)
print(response.json())
```

---

## Running the API Server

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (if needed)
pip install -r requirements.txt

# Run the server
uvicorn euwin.api.main:app --reload --host 0.0.0.0 --port 8000

# Access API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

---

## Next Steps

1. **Connect to Business Logic** - Integrate with `euwin/process/` and `euwin/analysis/` modules
2. **Database Integration** - Add MongoDB/MariaDB persistence for generated numbers
3. **Performance Testing** - Test bulk generation with large datasets
4. **Add Caching** - Cache frequently requested range statistics
5. **Implement Logging** - Add request/response logging for audit trails
6. **Add Rate Limiting** - Protect bulk generation endpoint from abuse
7. **Unit Tests** - Create pytest tests in `tests/test_api/test_random_numbers_controller.py`

---

## Files Created/Modified

✅ **Created:**
- `/euwin/api/routes/random_numbers_controller.py` - Main module (432 lines)
- `/euwin/api/routes/system_controller.py` - System health endpoints
- `/euwin/api/routes/__init__.py` - Package initialization

✅ **No modifications needed to:**
- `euwin/api/main.py` - Already configured to import this module
- `requirements.txt` - Dependencies already satisfy FastAPI needs

---

## Documentation

For more details on the migration and framework usage, see:
- `ADD_WEB_FRAMEWORK.md` - Web framework setup guide
- `MIGRATION_PLAN.md` - Java to Python migration strategy
- FastAPI Docs: https://fastapi.tiangolo.com/
- Pydantic Docs: https://docs.pydantic.dev/

