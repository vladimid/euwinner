# Analysis Controller Usage Examples

## API Endpoint: POST /analysis/frequency

The Analysis Controller accepts JSON requests with 0-3 optional fields:
- **draws**: Number of draws to analyze (default: 100)
- **offset**: Number of draws to skip from the beginning (default: 0)  
- **number_range**: List of numbers to analyze (default: [1-59])

### Example 1: Default Parameters (Analyze most recent 100 draws, all numbers)
```json
POST /analysis/frequency
Content-Type: application/json

{}
```

Response:
```json
{
  "draws_analyzed": 100,
  "offset": 0,
  "number_range": [1, 2, 3, ..., 59],
  "most_frequent": [40, 14, 56, 10, 12, ...],
  "least_frequent": [8, 21, 26, ...],
  "never_drawn": [8, 21, 26, 48, 55],
  "frequency": {"1": 2, "2": 1, "3": 4, ...},
  "total_balls_drawn": 600
}
```

### Example 2: Analyze 50 draws starting from offset 10
```json
POST /analysis/frequency
Content-Type: application/json

{
  "draws": 50,
  "offset": 10
}
```

### Example 3: Analyze specific numbers only
```json
POST /analysis/frequency
Content-Type: application/json

{
  "draws": 100,
  "offset": 0,
  "number_range": [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
}
```

### Example 4: Quick snapshot of most recent 20 draws
```json
POST /analysis/frequency
Content-Type: application/json

{
  "draws": 20
}
```

## CLI Usage (number_frequency.py)

The command-line script still works as before:

```bash
# Analyze most recent 26 draws
python euwin/analysis/number_frequency.py

# Analyze most recent 50 draws
python euwin/analysis/number_frequency.py 50

# Analyze 30 draws before draw 3160
python euwin/analysis/number_frequency.py 3160 30
```

## How to Test with cURL

```bash
# Default parameters
curl -X POST http://localhost:8000/analysis/frequency \
  -H "Content-Type: application/json" \
  -d '{}'

# Custom parameters
curl -X POST http://localhost:8000/analysis/frequency \
  -H "Content-Type: application/json" \
  -d '{"draws": 50, "offset": 10}'

# Specific numbers
curl -X POST http://localhost:8000/analysis/frequency \
  -H "Content-Type: application/json" \
  -d '{"draws": 100, "number_range": [1, 2, 3, 4, 5, 6]}'
```

## Implementation Details

- The API uses the `euwin.analysis.frequency_analyzer` module
- The analyzer reads from `tests/data/lotto-draw-history.csv`
- Data is automatically validated and error messages are returned for invalid parameters
- Both CLI and API share the same underlying analysis logic

