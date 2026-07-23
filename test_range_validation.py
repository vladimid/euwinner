#!/usr/bin/env python
"""Quick test of AnalysisRequest number range normalization"""

from euwin.api.routes.analysis_controller import AnalysisRequest
from pydantic import ValidationError

def test_case(name, should_fail=False):
    def decorator(func):
        try:
            func()
            if should_fail:
                print(f"❌ {name} - FAILED (expected error but passed)")
            else:
                print(f"✓ {name}")
        except ValidationError as e:
            if should_fail:
                print(f"✓ {name} (correctly raised error)")
            else:
                print(f"❌ {name} - FAILED: {e.error_count()} error(s)")
                for err in e.errors():
                    print(f"   - {err}")
        except AssertionError as e:
            print(f"❌ {name} - FAILED: {e}")
        except Exception as e:
            print(f"❌ {name} - FAILED with exception: {e}")
        return func
    return decorator

# Test cases
@test_case("Test 1: Range [21, 25]")
def test_range():
    r = AnalysisRequest(number_range=[21, 25])
    assert r.number_range == [21, 22, 23, 24, 25], f"Got {r.number_range}"

@test_case("Test 2: Single [21] + end=25")
def test_single_with_end():
    r = AnalysisRequest(number_range=[21], number_range_end=25)
    assert r.number_range == [21, 22, 23, 24, 25], f"Got {r.number_range}"

@test_case("Test 3: Verbose list [21,22,23,24,25]")
def test_verbose():
    r = AnalysisRequest(number_range=[21, 22, 23, 24, 25])
    assert r.number_range == [21, 22, 23, 24, 25], f"Got {r.number_range}"

@test_case("Test 4: None range")
def test_none():
    r = AnalysisRequest(number_range=None)
    assert r.number_range is None, f"Got {r.number_range}"

@test_case("Test 5: Single number [42]")
def test_single():
    r = AnalysisRequest(number_range=[42])
    assert r.number_range == [42], f"Got {r.number_range}"

@test_case("Test 6: Large range [1, 59]")
def test_large_range():
    r = AnalysisRequest(number_range=[1, 59])
    assert r.number_range == list(range(1, 60)), f"Got {len(r.number_range)} elements"

@test_case("Test 7: Reversed range [25, 21]", should_fail=True)
def test_reversed_range():
    r = AnalysisRequest(number_range=[25, 21])

@test_case("Test 8: number_range_end without number_range", should_fail=True)
def test_end_without_range():
    r = AnalysisRequest(number_range_end=25)

@test_case("Test 9: number_range_end with long list", should_fail=True)
def test_end_with_long_list():
    r = AnalysisRequest(number_range=[1, 2, 3], number_range_end=25)

@test_case("Test 10: Empty list", should_fail=True)
def test_empty_list():
    r = AnalysisRequest(number_range=[])

@test_case("Test 11: Defaults")
def test_defaults():
    r = AnalysisRequest()
    assert r.draws == 100, f"draws: {r.draws}"
    assert r.offset == 0, f"offset: {r.offset}"
    assert r.number_range is None, f"number_range: {r.number_range}"

@test_case("Test 12: Full request with range")
def test_full_request():
    r = AnalysisRequest(draws=50, offset=10, number_range=[20, 30])
    assert r.draws == 50
    assert r.offset == 10
    assert r.number_range == list(range(20, 31))

print("\n✅ All tests completed!")

