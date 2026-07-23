# Quick Reference: Analysis Controller

## TL;DR - How to Use

### API POST Request Examples

**Default (100 draws, all numbers 1-59):**
```bash
curl -X POST http://localhost:8000/analysis/frequency \
  -H "Content-Type: application/json" -d '{}'
```

**Last 20 draws:**
```bash
curl -X POST http://localhost:8000/analysis/frequency \
  -H "Content-Type: application/json" -d '{"draws": 20}'
```

**Skip 10, analyze next 50:**
```bash
curl -X POST http://localhost:8000/analysis/frequency \
  -H "Content-Type: application/json" -d '{"draws": 50, "offset": 10}'
```

**Only numbers [1,10,20,30,40,50,59]:**
```bash
curl -X POST http://localhost:8000/analysis/frequency \
  -H "Content-Type: application/json" \
  -d '{"number_range": [1,10,20,30,40,50,59]}'
```

## Request Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `draws` | integer | 100 | How many draws to analyze |
| `offset` | integer | 0 | How many draws to skip from start |
| `number_range` | array | [1-59] | Which numbers to include in analysis |

All parameters are optional - omit any to use defaults.

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `draws_analyzed` | int | Number of draws actually analyzed |
| `offset` | int | Offset used |
| `number_range` | array | Numbers that were analyzed |
| `frequency` | object | {number: count} for each number |
| `most_frequent` | array | Numbers drawn most often |
| `least_frequent` | array | Numbers drawn least often (or never) |
| `never_drawn` | array | Numbers with count = 0 |
| `total_balls_drawn` | int | Total balls drawn in period |

## CLI Commands

```bash
# Default (most recent 26 draws)
python euwin/analysis/number_frequency.py

# Last N draws
python euwin/analysis/number_frequency.py 50

# N draws before draw M
python euwin/analysis/number_frequency.py 3160 30
```

## Python Code Example

```python
from euwin.analysis.frequency_analyzer import analyze_frequency

# Analyze 50 draws starting from draw 10
result = analyze_frequency(draws=50, offset=10)

# Get top 5 most frequent numbers
top_5 = result['most_frequent'][:5]
print(f"Top 5 numbers: {top_5}")

# Get numbers never drawn
never_drawn = result['never_drawn']
print(f"Never drawn: {never_drawn}")

# Get full frequency map
frequency = result['frequency']
print(f"Number 1 drawn {frequency[1]} times")
```

## Error Handling

All parameters are validated. Common errors:
- `offset >= total_draws` → Error
- `draws <= 0` → Error
- `offset < 0` → Error
- Invalid CSV → Error with details

All errors return HTTP 400 with descriptive message.

## Data Source

CSV file: `/Users/vlada/sandbox/python/euwinner/tests/data/lotto-draw-history.csv`
- One draw per row
- Columns: DrawDate, Ball 1-6, Bonus Ball, Ball Set, Machine, DrawNumber

## Integration

Both API and CLI use the same `frequency_analyzer` module for consistent results.

Module path: `euwin.analysis.frequency_analyzer`
- `analyze_frequency()` - Main analysis function
- `load_csv_data()` - Load CSV file
- `get_csv_file_path()` - Get CSV path

