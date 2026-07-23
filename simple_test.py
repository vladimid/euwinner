#!/usr/bin/env python
"""Simple validation of AnalysisRequest number range normalization - No pytest required"""

import sys
sys.path.insert(0, '/Users/vlada/sandbox/python/euwinner')

from euwin.api.routes.analysis_controller import AnalysisRequest
from pydantic import ValidationError

print("=" * 60)
print("Testing AnalysisRequest Number Range Normalization")
print("=" * 60)

passed = 0
failed = 0

def run_test(name, test_func, should_fail=False):
    global passed, failed
    try:
        test_func()
        if should_fail:
            print(f"✗ {name} - FAILED (expected error but passed)")
            failed += 1
        else:
            print(f"✓ {name}")
            passed += 1
    except ValidationError as e:
        if should_fail:
            print(f"✓ {name} (correctly raised ValidationError)")
            passed += 1
        else:
            print(f"✗ {name} - FAILED: {str(e.errors()[0])}")
            failed += 1
    except AssertionError as e:
        print(f"✗ {name} - FAILED: {e}")
        failed += 1
    except Exception as e:
        print(f"✗ {name} - FAILED with exception: {type(e).__name__}: {e}")
        failed += 1

# Test 1: Range [21, 25]
def test1():
    r = AnalysisRequest(number_range=[21, 25])
    assert r.number_range == [21, 22, 23, 24, 25], f"Got {r.number_range}"

run_test("Test 1: Range [21, 25] expands to [21..25]", test1)

# Test 2: Single [21] + end=25
def test2():
    r = AnalysisRequest(number_range=[21], number_range_end=25)
    assert r.number_range == [21, 22, 23, 24, 25], f"Got {r.number_range}"

run_test("Test 2: Single [21] + end=25 expands to [21..25]", test2)

# Test 3: Verbose list
def test3():
    r = AnalysisRequest(number_range=[21, 22, 23, 24, 25])
    assert r.number_range == [21, 22, 23, 24, 25], f"Got {r.number_range}"

run_test("Test 3: Verbose list [21,22,23,24,25] unchanged", test3)

# Test 4: None range
def test4():
    r = AnalysisRequest(number_range=None)
    assert r.number_range is None, f"Got {r.number_range}"

run_test("Test 4: None range stays None", test4)

# Test 5: Single number [42]
def test5():
    r = AnalysisRequest(number_range=[42])
    assert r.number_range == [42], f"Got {r.number_range}"

run_test("Test 5: Single number [42] stays [42]", test5)

# Test 6: Large range [1, 59]
def test6():
    r = AnalysisRequest(number_range=[1, 59])
    assert r.number_range == list(range(1, 60)), f"Got {len(r.number_range)} elements"

run_test("Test 6: Large range [1, 59] expands to 59 numbers", test6)

# Test 7: Reversed range [25, 21] (should fail)
def test7():
    r = AnalysisRequest(number_range=[25, 21])

run_test("Test 7: Reversed range [25, 21] raises error", test7, should_fail=True)

# Test 8: number_range_end without number_range (should fail)
def test8():
    r = AnalysisRequest(number_range_end=25)

run_test("Test 8: number_range_end without number_range raises error", test8, should_fail=True)

# Test 9: number_range_end with long list (should fail)
def test9():
    r = AnalysisRequest(number_range=[1, 2, 3], number_range_end=25)

run_test("Test 9: number_range_end with >2 element list raises error", test9, should_fail=True)

# Test 10: Empty list (should fail)
def test10():
    r = AnalysisRequest(number_range=[])

run_test("Test 10: Empty list [] raises error", test10, should_fail=True)

# Test 11: Defaults
def test11():
    r = AnalysisRequest()
    assert r.draws == 100, f"draws: {r.draws}"
    assert r.offset == 0, f"offset: {r.offset}"
    assert r.number_range is None, f"number_range: {r.number_range}"

run_test("Test 11: Default values (draws=100, offset=0, number_range=None)", test11)

# Test 12: Full request with range
def test12():
    r = AnalysisRequest(draws=50, offset=10, number_range=[20, 30])
    assert r.draws == 50
    assert r.offset == 10
    assert r.number_range == list(range(20, 31))

run_test("Test 12: Full request with draws, offset, and range", test12)

# Test 13: Single with same end
def test13():
    r = AnalysisRequest(number_range=[21], number_range_end=21)
    assert r.number_range == [21], f"Got {r.number_range}"

run_test("Test 13: Single with same end [21], end=21 stays [21]", test13)

# Test 14: Negative numbers
def test14():
    r = AnalysisRequest(number_range=[-5, -1])
    assert r.number_range == [-5, -4, -3, -2, -1]

run_test("Test 14: Negative range [-5, -1] expands correctly", test14)

# Test 15: Start > end with single + end (should fail)
def test15():
    r = AnalysisRequest(number_range=[25], number_range_end=21)

run_test("Test 15: Single [25] + end=21 raises error (start > end)", test15, should_fail=True)

print("\n" + "=" * 60)
print(f"RESULTS: {passed} passed, {failed} failed")
print("=" * 60)

if failed == 0:
    print("✅ All tests passed! Implementation is working correctly.")
    sys.exit(0)
else:
    print(f"❌ {failed} test(s) failed!")
    sys.exit(1)

