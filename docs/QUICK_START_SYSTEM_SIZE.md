# Quick Reference: Using mainSystemSize Parameter

## What It Does

The `mainSystemSize` parameter now properly works to **randomly select N combinations from all available combinations**.

## Before vs After

### Before
- Parameter: `mainSystemSize` 
- Behavior: Ignored, all combinations returned
- Example: With 6 numbers, 5 per combo → returns all 6 combinations

### After  
- Parameter: `mainSystemSize`
- Behavior: Randomly selects N combinations from all available
- Example: With 6 numbers, 5 per combo, mainSystemSize=3 → randomly returns 3 of the 6

## Quick Example

### Input
```json
{
  "mainNumbersCombination": [1, 2, 3, 4, 5, 6],
  "mainGamePool": 59,
  "mainGameSize": 5,
  "mainSystemSize": 3
}
```

### What Happens
1. **Calculates**: How many 5-number combinations from [1-6]? → **C(6,5) = 6**
2. **Generates**: All 6 possible combinations
3. **Selects**: Randomly picks 3 of them
4. **Returns**: Those 3 selected + statistics

### Output Example
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

## Key Points

- ✓ **Random**: Different each time (not first N, not last N)
- ✓ **From Full Pool**: All combinations generated first
- ✓ **Transparent**: Response shows available vs selected
- ✓ **Flexible**: Works with any mainSystemSize up to maximum

## Mathematical Details

The algorithm:
1. Generates C(n, r) combinations where:
   - n = number of selected lottery numbers
   - r = mainGameSize (numbers per combination)
2. Randomly selects mainSystemSize combinations
3. Returns statistics on coverage

### Example Scenarios

| Numbers | Size | System | Available | Selected | Result |
|---------|------|--------|-----------|----------|--------|
| 6 | 5 | 3 | C(6,5)=6 | 3 | 50% random |
| 7 | 4 | 5 | C(7,4)=35 | 5 | Random 5 of 35 |
| 10 | 6 | 20 | C(10,6)=210 | 20 | Random 20 of 210 |

## Testing

See the actual randomness in action:

```bash
# Run demo showing different selections each time
python demo_random_selection.py

# Run unit tests
python test_wheeling_system.py
```

## Migration Guide (If You Had Old Code)

If you were using the old version and expecting specific deterministic behavior:

**Old (didn't use mainSystemSize):**
```python
# All combinations returned
result = builder.build_wheeling_system({
    "mainNumbersCombination": [1, 2, 3, 4, 5, 6],
    "mainGamePool": 59,
    "mainGameSize": 5,
    "mainSystemSize": 3  # This was ignored
})
# Got all 6 combinations
```

**New (actually uses mainSystemSize):**
```python
# Only 3 randomly selected
result = builder.build_wheeling_system({
    "mainNumbersCombination": [1, 2, 3, 4, 5, 6],
    "mainGamePool": 59,
    "mainGameSize": 5,
    "mainSystemSize": 3  # Now properly selects 3 random combinations
})
# Got 3 randomly selected combinations
```

## With Bonus Numbers

The same logic applies to bonus combinations:

```json
{
  "mainNumbersCombination": [1, 2, 3, 4, 5, 6],
  "mainGameSize": 5,
  "mainSystemSize": 3,
  "bonusNumbers": [1, 2],
  "bonusGameSize": 2,
  "bonusSystemSize": 1
}
```

This will:
- Randomly select 3 main combinations (5-number, from 6)
- Randomly select 1 bonus combination (2-number, from 2)

---

**For detailed documentation, see:**
- `IMPROVEMENT_SUMMARY.md` - Complete overview
- `WHEELING_IMPROVEMENTS.md` - Technical details
- `test_wheeling_system.py` - Unit tests
- `demo_random_selection.py` - Live demonstrations

