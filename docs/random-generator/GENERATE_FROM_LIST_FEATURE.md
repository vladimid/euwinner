# Random Numbers from List - Feature Documentation

## Overview

The Random Numbers Controller now supports generating random numbers from a provided list in addition to the existing min/max range functionality. This enables more flexible number selection scenarios.

---

## New Endpoints

### 1. POST `/api/random/generate-from-list`

Generate random numbers by selecting from a provided list.

#### Request
```json
{
  "count": 6,
  "number_pool": [1, 5, 10, 15, 20, 25, 30, 35, 40, 45],
  "include_bonus": false,
  "bonus_range": null
}
```

#### Parameters
- **`count`** (int, required): Number of random numbers to generate (1-100)
- **`number_pool`** (List[int], required): List of numbers to choose from (must be non-empty, no duplicates)
- **`include_bonus`** (bool, optional): Whether to generate a bonus number (default: false)
- **`bonus_range`** (int, optional): Range for bonus number (if include_bonus=true)

#### Response
```json
{
  "numbers": [5, 15, 30, 35, 40, 45],
  "bonus": null,
  "count": 6,
  "seed": null
}
```

#### Response Fields
- **`numbers`**: List of generated random numbers (sorted)
- **`count`**: Count of generated numbers
- **`bonus`**: Generated bonus number (if requested)
- **`seed`**: Random seed used (null unless using seed-based generation)

#### Error Cases
- Status 400 if count exceeds pool size
- Status 400 if pool contains duplicate numbers
- Status 422 if pool is empty

---

### 2. POST `/api/random/generate-from-list-bulk`

Generate multiple sets of random numbers from a list in bulk.

#### Request
```json
{
  "generations": 5,
  "count": 6,
  "number_pool": [1, 5, 10, 15, 20, 25, 30, 35, 40, 45],
  "include_bonus": true,
  "bonus_range": 10
}
```

#### Parameters
- **`generations`** (int, required): Number of generation requests (1-1000)
- **`count`** (int, required): Numbers per generation (1-100)
- **`number_pool`** (List[int], required): List of numbers to choose from
- **`include_bonus`** (bool, optional): Generate bonus for each set (default: false)
- **`bonus_range`** (int, optional): Range for bonus number

#### Response
```json
{
  "results": [
    {
      "numbers": [5, 15, 20, 30, 40, 45],
      "bonus": 7,
      "count": 6
    },
    {
      "numbers": [1, 10, 15, 25, 35, 40],
      "bonus": 3,
      "count": 6
    },
    ...
  ],
  "total_sets": 5
}
```

---

## Use Cases

### 1. Generate from Specific Numbers
```json
{
  "count": 6,
  "number_pool": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
}
```
Generates 6 random numbers from the provided list.

---

### 2. Generate from Lottery Hot Numbers
```json
{
  "count": 6,
  "number_pool": [7, 14, 21, 28, 35, 42, 49]
}
```
Generate combinations from frequently drawn numbers.

---

### 3. Generate from Lottery Cold Numbers
```json
{
  "count": 6,
  "number_pool": [2, 11, 18, 27, 33, 41, 48]
}
```
Generate combinations from rarely drawn numbers.

---

### 4. Generate from Custom Pool with Bonus
```json
{
  "count": 6,
  "number_pool": [5, 10, 15, 20, 25, 30, 35, 40],
  "include_bonus": true,
  "bonus_range": 10
}
```
Generate numbers from a custom pool with an additional bonus number.

---

### 5. Bulk Generate from List
```json
{
  "generations": 100,
  "count": 6,
  "number_pool": [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
}
```
Generate 100 different combinations from the same pool.

---

## Comparison with Existing Generate Endpoint

### Existing `/api/random/generate` (Min/Max Range)
```json
{
  "count": 6,
  "min_number": 1,
  "max_number": 49
}
```
- Generates from contiguous range
- Must specify min and max
- Automatically includes all numbers in range

### New `/api/random/generate-from-list` (Number Pool)
```json
{
  "count": 6,
  "number_pool": [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 49]
}
```
- Generates from specific list of numbers
- Can be non-contiguous
- Can exclude specific numbers
- More flexible for targeted selections

---

## Examples

### Example 1: Select from High Numbers
**Request:**
```bash
curl -X POST http://localhost:8000/api/random/generate-from-list \
  -H "Content-Type: application/json" \
  -d '{
    "count": 6,
    "number_pool": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
  }'
```

**Response:**
```json
{
  "numbers": [33, 35, 37, 42, 45, 48],
  "bonus": null,
  "count": 6,
  "seed": null
}
```

---

### Example 2: Select from Specific Numbers with Bonus
**Request:**
```bash
curl -X POST http://localhost:8000/api/random/generate-from-list \
  -H "Content-Type: application/json" \
  -d '{
    "count": 5,
    "number_pool": [7, 14, 21, 28, 35, 42, 49],
    "include_bonus": true,
    "bonus_range": 10
  }'
```

**Response:**
```json
{
  "numbers": [7, 14, 28, 35, 49],
  "bonus": 6,
  "count": 5,
  "seed": null
}
```

---

### Example 3: Bulk Generation from Pool
**Request:**
```bash
curl -X POST http://localhost:8000/api/random/generate-from-list-bulk \
  -H "Content-Type: application/json" \
  -d '{
    "generations": 3,
    "count": 3,
    "number_pool": [1, 5, 10, 15, 20]
  }'
```

**Response:**
```json
{
  "results": [
    {
      "numbers": [1, 10, 20],
      "bonus": null,
      "count": 3
    },
    {
      "numbers": [5, 15, 20],
      "bonus": null,
      "count": 3
    },
    {
      "numbers": [1, 5, 15],
      "bonus": null,
      "count": 3
    }
  ],
  "total_sets": 3
}
```

---

## Validation Rules

### Valid Requests ✅
- Non-empty number_pool with unique numbers
- count ≤ pool size
- count between 1-100
- generations between 1-1000 (for bulk)

### Invalid Requests ❌
- Empty number_pool
- number_pool with duplicate numbers
- count > pool size
- count < 1 or count > 100
- generations < 1 or generations > 1000
- bonus_range < 1 (if include_bonus=true)

---

## Error Responses

### Error: Count Exceeds Pool Size
```json
{
  "detail": "Cannot generate 10 unique numbers from pool of 5 numbers"
}
```
Status: 400

### Error: Duplicate Numbers in Pool
```json
{
  "detail": "number_pool contains duplicate numbers"
}
```
Status: 400

### Error: Empty Pool
```json
{
  "detail": "ensure this value has at least 1 items"
}
```
Status: 422

---

## Backward Compatibility

✅ **All existing endpoints continue to work:**
- `/api/random/generate` - Min/max range generation
- `/api/random/generate-bulk` - Bulk min/max generation
- `/api/random/validate` - Number validation
- `/api/random/sequential` - Sequential numbers
- `/api/random/range-info` - Range information
- `/api/random/seed-generate` - Seeded generation

---

## Performance Considerations

- Generation from list uses Python's `random.sample()` - efficient for large pools
- Bulk generation iterates for each set - scales well up to 1000 generations
- No database queries - purely in-memory operations

---

## Advantages of Generate-from-List

1. **Flexibility** - Choose any numbers, not just ranges
2. **Targeted Selection** - Select from specific subsets (e.g., only odd numbers)
3. **Historical Analysis** - Use previously drawn numbers
4. **Custom Pools** - Create domain-specific pools for testing
5. **More Control** - Exclude specific numbers if desired

---

## Integration Examples

### Python Example
```python
import requests

# Generate 6 numbers from a specific pool
response = requests.post(
    'http://localhost:8000/api/random/generate-from-list',
    json={
        'count': 6,
        'number_pool': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    }
)

numbers = response.json()['numbers']
print(f"Generated numbers: {numbers}")
```

### JavaScript Example
```javascript
// Generate 6 numbers from a specific pool
const response = await fetch('http://localhost:8000/api/random/generate-from-list', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        count: 6,
        number_pool: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    })
});

const data = await response.json();
console.log('Generated numbers:', data.numbers);
```

---

## Testing

Run the comprehensive test suite:
```bash
pytest tests/test_api/test_random_from_list.py -v
```

Tests cover:
- Basic generation from list
- Generation with bonus
- Single number selection
- Entire pool selection
- Error cases (exceeds pool, duplicates, empty pool)
- Unique and sorted output
- Bulk generation
- Backward compatibility with existing endpoints

