# Generate from List - Quick Start Guide

## What's New?

Two new endpoints added to generate random numbers from a provided list:

1. **POST `/random/generate-from-list`** - Single generation
2. **POST `/random/generate-from-list-bulk`** - Bulk generation

---

## Quick Examples

### Generate 6 numbers from a pool
```bash
curl -X POST http://localhost:8000/random/generate-from-list \
  -H "Content-Type: application/json" \
  -d '{
    "count": 6,
    "number_pool": [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
  }'
```

**Response:**
```json
{
  "numbers": [5, 15, 25, 30, 40, 50],
  "bonus": null,
  "count": 6,
  "seed": null
}
```

---

### With Bonus Number
```bash
curl -X POST http://localhost:8000/random/generate-from-list \
  -H "Content-Type: application/json" \
  -d '{
    "count": 6,
    "number_pool": [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
    "include_bonus": true,
    "bonus_range": 10
  }'
```

**Response:**
```json
{
  "numbers": [1, 10, 20, 30, 40, 45],
  "bonus": 7,
  "count": 6,
  "seed": null
}
```

---

### Bulk Generate 100 Sets
```bash
curl -X POST http://localhost:8000/random/generate-from-list-bulk \
  -H "Content-Type: application/json" \
  -d '{
    "generations": 100,
    "count": 6,
    "number_pool": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  }'
```

**Response:**
```json
{
  "results": [
    {"numbers": [1, 3, 5, 7, 9, 2], "bonus": null, "count": 6},
    {"numbers": [2, 4, 6, 8, 10, 1], "bonus": null, "count": 6},
    ...
  ],
  "total_sets": 100
}
```

---

## Use Cases

### Lottery Hot Numbers
Select from frequently drawn numbers:
```json
{
  "count": 6,
  "number_pool": [7, 14, 21, 28, 35, 42, 49]
}
```

### High Numbers Only
```json
{
  "count": 6,
  "number_pool": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
}
```

### Even Numbers Only
```json
{
  "count": 6,
  "number_pool": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48]
}
```

### Custom Mix
```json
{
  "count": 6,
  "number_pool": [5, 15, 25, 35, 45, 49]
}
```

---

## Request Format

### Single Generation
```json
{
  "count": 6,                              // 1-100: numbers to select
  "number_pool": [1, 2, 3, 4, 5],         // required: list to choose from
  "include_bonus": false,                  // optional: add bonus number
  "bonus_range": null                      // optional: bonus range (1-N)
}
```

### Bulk Generation
```json
{
  "generations": 100,                      // 1-1000: how many sets
  "count": 6,                              // 1-100: numbers per set
  "number_pool": [1, 2, 3, 4, 5],         // required: list to choose from
  "include_bonus": false,                  // optional: add bonus to each
  "bonus_range": null                      // optional: bonus range
}
```

---

## Response Format

### Single Generation Response
```json
{
  "numbers": [1, 2, 3, 4, 5, 6],  // Generated numbers (sorted)
  "bonus": null,                   // Bonus if requested
  "count": 6,                      // Count of numbers
  "seed": null                     // Seed if seeded generation
}
```

### Bulk Generation Response
```json
{
  "results": [                     // Array of responses
    {"numbers": [...], "bonus": null, "count": 6},
    {"numbers": [...], "bonus": null, "count": 6},
    ...
  ],
  "total_sets": 100               // Total generated sets
}
```

---

## Error Cases

| Scenario | Status | Detail |
|----------|--------|--------|
| count > pool size | 400 | "Cannot generate X unique numbers from pool of Y" |
| duplicates in pool | 400 | "number_pool contains duplicate numbers" |
| empty pool | 422 | "ensure this value has at least 1 items" |
| bonus_range < 1 | 400 | "bonus_range must be at least 1" |

---

## Key Features

✅ Select from any list of numbers (non-contiguous ok)
✅ Unique numbers guaranteed (no duplicates in result)
✅ Sorted output
✅ Optional bonus number
✅ Bulk generation support (1-1000 sets)
✅ Duplicate detection in pool
✅ Clear validation errors

---

## Advantages Over Min/Max

| Aspect | Min/Max | From List |
|--------|---------|-----------|
| Range | Must be contiguous | Any numbers |
| Exclude | Can't exclude specific | Can choose subset |
| Flexibility | Fixed | High |
| Use Case | General | Targeted |

---

## Example: Hot Number Lottery Selection

1. **Analyze lottery data** to find hot numbers
2. **Get the list**: [7, 14, 21, 28, 35, 42, 49]
3. **Generate combinations**:
```bash
curl -X POST http://localhost:8000/random/generate-from-list-bulk \
  -H "Content-Type: application/json" \
  -d '{
    "generations": 50,
    "count": 6,
    "number_pool": [7, 14, 21, 28, 35, 42, 49]
  }'
```
4. **Get 50 different combinations** of 6 numbers from the hot numbers list

---

## Python Example

```python
import requests

# Single generation
response = requests.post(
    'http://localhost:8000/random/generate-from-list',
    json={
        'count': 6,
        'number_pool': [1, 5, 10, 15, 20, 25, 30, 35, 40, 45]
    }
)
numbers = response.json()['numbers']
print(f"Generated: {numbers}")

# Bulk generation
response = requests.post(
    'http://localhost:8000/random/generate-from-list-bulk',
    json={
        'generations': 10,
        'count': 6,
        'number_pool': [1, 5, 10, 15, 20, 25, 30, 35, 40, 45]
    }
)
all_sets = response.json()['results']
for i, result in enumerate(all_sets, 1):
    print(f"Set {i}: {result['numbers']}")
```

---

## Backward Compatibility

✅ All existing endpoints still work:
- `/random/generate` (min/max)
- `/random/generate-bulk` (bulk min/max)
- `/random/validate`
- `/random/sequential`
- `/random/range-info`
- `/random/seed-generate`

No breaking changes!

---

## Documentation

For comprehensive documentation, see:
- `docs/GENERATE_FROM_LIST_FEATURE.md` - Full feature guide
- `RANDOM_FROM_LIST_SUMMARY.md` - Implementation details
- `tests/test_api/test_random_from_list.py` - Test examples

---

## Testing

Run the test suite:
```bash
pytest tests/test_api/test_random_from_list.py -v
```

Tests cover:
- Basic generation ✓
- With/without bonus ✓
- Validation errors ✓
- Bulk operations ✓
- Backward compatibility ✓
- 20+ test cases ✓

---

Ready to use! 🚀

