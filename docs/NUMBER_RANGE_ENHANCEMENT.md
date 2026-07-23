# Analysis Controller - Number Range Enhancement

## Overview
The Analysis Controller now supports multiple ways to specify the `number_range` parameter, providing more flexibility for API consumers.

## Number Range Specification Methods

### 1. Verbose List (Original Method)
Pass a complete list of numbers to analyze:

**Request:**
```json
{
  "number_range": [21, 22, 23, 24, 25],
  "draws": 100,
  "offset": 0
}
```

**Result:** Analyzes exactly these 5 numbers: 21, 22, 23, 24, 25

---

### 2. Two-Element Range (New Method)
Pass a two-element list `[start, end]` to create a range:

**Request:**
```json
{
  "number_range": [21, 25],
  "draws": 100,
  "offset": 0
}
```

**Result:** Automatically expands to `[21, 22, 23, 24, 25]` (inclusive on both ends)

**Note:** The range is inclusive on both ends. `[21, 25]` produces 5 numbers, not 4.

---

### 3. Single Number with Range End (New Method)
Pass a single-element list with the `number_range_end` field:

**Request:**
```json
{
  "number_range": [21],
  "number_range_end": 25,
  "draws": 100,
  "offset": 0
}
```

**Result:** Equivalent to `[21, 25]`, expands to `[21, 22, 23, 24, 25]`

**Use case:** When you want to pass the range as separate parameters instead of a list.

---

### 4. Single Number Only
Pass a single-element list without `number_range_end`:

**Request:**
```json
{
  "number_range": [42],
  "draws": 100,
  "offset": 0
}
```

**Result:** Analyzes just the single number 42

---

### 5. Default (No Range Specified)
Don't provide `number_range`:

**Request:**
```json
{
  "draws": 100,
  "offset": 0
}
```

**Result:** Uses default range `[1-59]` (for National Lottery)

---

## Validation Rules

### Valid Combinations
- ✅ `"number_range": [21, 22, 23, 24, 25]` - verbose list
- ✅ `"number_range": [21, 25]` - range with start and end
- ✅ `"number_range": [21], "number_range_end": 25` - single with end
- ✅ `"number_range": [42]` - single number only
- ✅ `"number_range": null` or omitted - use defaults

### Invalid Combinations
- ❌ `"number_range": []` - empty list not allowed
- ❌ `"number_range_end": 25` without `number_range` - end requires range start
- ❌ `"number_range": [1, 2, 3], "number_range_end": 25` - end only valid with 1-2 element lists
- ❌ `"number_range": [25, 21]` - reversed range (start > end)
- ❌ `"number_range": [25], "number_range_end": 21` - start > end

---

## Examples

### Example 1: Analyze numbers 21-30
```bash
curl -X POST http://localhost:8000/frequency \
  -H "Content-Type: application/json" \
  -d '{
    "number_range": [21, 30],
    "draws": 100,
    "offset": 0
  }'
```

### Example 2: Analyze numbers 1-59 (default) for last 50 draws
```bash
curl -X POST http://localhost:8000/frequency \
  -H "Content-Type: application/json" \
  -d '{
    "draws": 50,
    "offset": 0
  }'
```

### Example 3: Analyze single number with separate end parameter
```bash
curl -X POST http://localhost:8000/frequency \
  -H "Content-Type: application/json" \
  -d '{
    "number_range": [1],
    "number_range_end": 20,
    "draws": 100
  }'
```

### Example 4: Analyze specific numbers
```bash
curl -X POST http://localhost:8000/frequency \
  -H "Content-Type: application/json" \
  -d '{
    "number_range": [5, 10, 15, 20, 25, 30],
    "draws": 100
  }'
```

---

## Implementation Details

### Normalization Process
When a request is received:

1. **Validation Phase (before):** Check that `number_range_end` is only used appropriately
2. **Normalization Phase (after):** Convert the range format to a verbose list
   - 2-element list → expand to full range `list(range(start, end + 1))`
   - 1-element + end → combine into range
   - Multi-element (>2) → keep as-is (verbose list)
   - None → stays None (use analyzer defaults)
3. **Pass to Analyzer:** The normalized list is passed to the frequency analyzer

### Inclusive Ranges
All ranges are inclusive on both ends:
- `[21, 25]` includes 21 and 25 (5 numbers total)
- `[21], end=25` includes 21 and 25 (5 numbers total)

---

## Backward Compatibility

✅ **Fully backward compatible** with existing code that passes verbose lists:
```json
{
  "number_range": [21, 22, 23, 24, 25]
}
```

The verbose list format continues to work exactly as before.

---

## Error Handling

All validation errors return HTTP 400 with descriptive error messages:

```json
{
  "detail": "number_range start (25) cannot be greater than end (21)"
}
```

---

## Field Descriptions in API

- **`number_range`**: `Optional[List[int]]`
  - Can be a verbose list: `[21, 22, 23, 24, 25]`
  - Can be a range: `[21, 25]`
  - Can be a single number: `[42]`
  - Default: `None` (uses `[1-59]`)

- **`number_range_end`**: `Optional[int]`
  - Used only when `number_range` contains a single number
  - Specifies the upper limit of the range
  - Default: `None`

