# Wheeling System Builder Improvements

## Overview

The wheeling system builder has been enhanced to properly utilize the `mainSystemSize` parameter from JSON input. Previously, the parameter was being passed but not actually used to limit the number of combinations returned. Now the system correctly implements random selection of combinations from the full pool.

## What Changed

### 1. **Proper Interpretation of Parameters**

The parameters now mean:
- **`mainNumbersCombination`**: List of selected lottery numbers to draw combinations from
- **`mainGameSize`**: Size of each individual combination (e.g., 5 numbers per line)
- **`mainSystemSize`**: Number of combinations to randomly select (the wheeling system size)

### 2. **Algorithm Behavior**

**Before:**
- Generated all combinations of size `mainGameSize` from `mainNumbersCombination`
- Returned ALL combinations (e.g., all 6 combinations when requesting 5-from-6)
- `mainSystemSize` parameter was ignored

**After:**
- Generates all combinations of size `mainGameSize` from `mainNumbersCombination`
- Randomly selects `mainSystemSize` combinations from the full pool
- Returns only the selected combinations
- Reports both available and selected counts in response

### 3. **Random Selection Mechanism**

The `_select_random_combinations()` method:
```python
@staticmethod
def _select_random_combinations(
    all_combinations: List[List[int]],
    count: int
) -> List[List[int]]:
    """
    Randomly select a subset of combinations from the full set.
    Uses random.sample() for unbiased selection without replacement.
    """
    if count >= len(all_combinations):
        return all_combinations  # Return all if requesting more than available
    
    selected = random.sample(all_combinations, count)
    return sorted([sorted(combo) for combo in selected])
```

## Example Usage

### Request
```json
{
  "mainNumbersCombination": [1, 2, 3, 4, 5, 6],
  "mainGamePool": 59,
  "mainGameSize": 5,
  "mainSystemSize": 3
}
```

### Processing
1. Available combinations: C(6,5) = 6 total combinations possible
2. Selected combinations: Randomly pick 3 from these 6
3. All possible 5-from-6 combos:
   - [1, 2, 3, 4, 5]
   - [1, 2, 3, 4, 6]
   - [1, 2, 3, 5, 6]
   - [1, 2, 4, 5, 6]
   - [1, 3, 4, 5, 6]
   - [2, 3, 4, 5, 6]

4. Example output (random selection):
   - [1, 2, 3, 4, 6]
   - [1, 2, 4, 5, 6]
   - [1, 3, 4, 5, 6]

### Response
```json
{
  "main_combinations": [
    [1, 2, 3, 4, 6],
    [1, 2, 4, 5, 6],
    [1, 3, 4, 5, 6]
  ],
  "total_main_combinations": 3,
  "available_main_combinations": 6,
  "coverage": {
    "total_possible_combinations": 6,
    "covered_combinations": 1,
    "coverage_percentage": 16.67
  }
}
```

## Files Modified

### `euwin/process/combination_builder.py`
- Added `import random` for random selection
- Updated `create_wheeling_combinations()` to:
  - Generate all combinations
  - Randomly select N combinations using the new method
  - Track both available and selected counts
- Added `_select_random_combinations()` method

### `euwin/process/wheeling_system_builder.py`
- Added `BONUS_GAME_SIZE` field constant
- Updated `build_wheeling_system()` to use `bonusGameSize` parameter

### `euwin/api/routes/system_controller.py`
- Added `bonusGameSize` optional parameter to `WheelingSystemRequest`
- Updated documentation and examples

### `euwin/validate/schema_validation.py`
- Added `bonusGameSize` to `OPTIONAL_FIELDS`

## Bonus System Support

The same improvements apply to bonus number combinations:
- **`bonusNumbers`**: Bonus numbers to select from
- **`bonusGameSize`**: Size of each bonus combination (optional, defaults to len(bonusNumbers))
- **`bonusSystemSize`**: Number of bonus combinations to randomly select

## Benefits

1. **True Lottery Wheeling**: Now properly implements wheeling system by randomly selecting combinations
2. **Flexible System Sizes**: Can request any number of combinations (up to the theoretical maximum)
3. **Randomization**: Different runs produce different results, avoiding patterns
4. **Transparency**: Response includes both available and selected counts for clarity
5. **Consistent Output**: Selected combinations are sorted for reproducibility per run

## Testing

Run the included test scripts to verify:

```bash
# Basic functionality tests
python test_wheeling_system.py

# Demonstration of random selection
python demo_random_selection.py
```

## API Endpoint Examples

### Basic Wheeling System
```bash
curl -X POST http://localhost:8000/system \
  -H "Content-Type: application/json" \
  -d '{
    "mainNumbersCombination": [1, 2, 3, 4, 5, 6],
    "mainGamePool": 59,
    "mainGameSize": 5,
    "mainSystemSize": 3
  }'
```

### With Bonus Numbers
```bash
curl -X POST http://localhost:8000/system \
  -H "Content-Type: application/json" \
  -d '{
    "mainNumbersCombination": [1, 2, 3, 4, 5, 6],
    "mainGamePool": 59,
    "mainGameSize": 5,
    "mainSystemSize": 3,
    "bonusNumbers": [1, 2],
    "bonusPool": 11,
    "bonusGameSize": 2,
    "bonusSystemSize": 1
  }'
```

### Random Wheeling System
```bash
curl -X POST http://localhost:8000/system/wheeling/random \
  -H "Content-Type: application/json" \
  -d '{
    "mainGamePoolSize": 59,
    "fullSystemSize": 6,
    "bonusGamePoolSize": 11,
    "bonusSize": 2,
    "mainGameSize": 5,
    "mainSystemSize": 3,
    "bonusSystemSize": 1
  }'
```

