# Number Range API - Quick Reference

## 📋 Five Ways to Specify Number Ranges

### 1️⃣ Default Range (1-59)
```json
POST /frequency
{
  "draws": 100
}
```
**Result:** Analyzes [1, 2, 3, ..., 59]

---

### 2️⃣ Two-Element Range (NEW)
```json
POST /frequency
{
  "number_range": [21, 25],
  "draws": 100
}
```
**Result:** Analyzes [21, 22, 23, 24, 25]

---

### 3️⃣ Single Number with Range End (NEW)
```json
POST /frequency
{
  "number_range": [21],
  "number_range_end": 25,
  "draws": 100
}
```
**Result:** Analyzes [21, 22, 23, 24, 25]

---

### 4️⃣ Verbose List (Original, Still Works)
```json
POST /frequency
{
  "number_range": [21, 22, 23, 24, 25],
  "draws": 100
}
```
**Result:** Analyzes [21, 22, 23, 24, 25]

---

### 5️⃣ Single Number Only
```json
POST /frequency
{
  "number_range": [42],
  "draws": 100
}
```
**Result:** Analyzes [42]

---

## ✅ Valid Requests
| Request | Result |
|---------|--------|
| `"number_range": [21, 25]` | [21, 22, 23, 24, 25] |
| `"number_range": [1, 59]` | [1, 2, ..., 59] |
| `"number_range": [21], "number_range_end": 25` | [21, 22, 23, 24, 25] |
| `"number_range": [5, 10, 15]` | [5, 10, 15] |
| (omitted or null) | [1, 2, ..., 59] (default) |

---

## ❌ Invalid Requests
| Request | Error |
|---------|-------|
| `"number_range": []` | Empty list not allowed |
| `"number_range": [25, 21]` | Reversed range (start > end) |
| `"number_range_end": 25` (no number_range) | End needs range start |
| `"number_range": [1, 2, 3], "number_range_end": 25` | End only with 1-2 element lists |
| `"number_range": [21], "number_range_end": 15` | Start > end |

---

## 🔄 Normalization Examples

| Input | Normalized |
|-------|----------|
| `[21, 25]` | `[21, 22, 23, 24, 25]` |
| `[1], end=20` | `[1, 2, 3, ..., 20]` |
| `[42]` | `[42]` |
| `[5, 10, 15, 20]` | `[5, 10, 15, 20]` |
| `None` | `None` (uses default) |

---

## 📝 All Parameters

```python
class AnalysisRequest:
    draws: Optional[int] = 100           # Number of draws to analyze
    offset: Optional[int] = 0            # Skip first N draws
    number_range: Optional[List[int]]    # Numbers to analyze
    number_range_end: Optional[int]      # Upper limit when number_range is single
```

---

## 🧪 Test Cases

```python
# Test with range [21, 25]
r1 = AnalysisRequest(number_range=[21, 25])
assert r1.number_range == [21, 22, 23, 24, 25]

# Test with single + end
r2 = AnalysisRequest(number_range=[21], number_range_end=25)
assert r2.number_range == [21, 22, 23, 24, 25]

# Test verbose list (unchanged)
r3 = AnalysisRequest(number_range=[21, 22, 23, 24, 25])
assert r3.number_range == [21, 22, 23, 24, 25]

# Test defaults
r4 = AnalysisRequest()
assert r4.draws == 100
assert r4.offset == 0
assert r4.number_range is None
```

---

## 🎯 Use Cases

### Analyze a Small Range
```bash
# Query numbers 1-10
curl -X POST http://localhost:8000/frequency \
  -H "Content-Type: application/json" \
  -d '{"number_range": [1, 10]}'
```

### Analyze Specific Numbers
```bash
# Query specific numbers: 5, 10, 15, 20, 25
curl -X POST http://localhost:8000/frequency \
  -H "Content-Type: application/json" \
  -d '{"number_range": [5, 10, 15, 20, 25]}'
```

### Analyze High Numbers
```bash
# Query numbers 30-59
curl -X POST http://localhost:8000/frequency \
  -H "Content-Type: application/json" \
  -d '{"number_range": [30, 59]}'
```

### Analyze Last 20 Draws
```bash
# Analyze last 20 draws with default range
curl -X POST http://localhost:8000/frequency \
  -H "Content-Type: application/json" \
  -d '{"draws": 20}'
```

---

## 📚 Documentation

- **Full Documentation:** See `NUMBER_RANGE_ENHANCEMENT.md`
- **Implementation Details:** See `ENHANCEMENT_SUMMARY.md`
- **Tests:** See `tests/test_api/test_analysis_controller.py`

