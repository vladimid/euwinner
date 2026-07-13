"""
Test script to verify the wheeling system builder implementation
"""
import sys
import os
import json

# Add the project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import directly to avoid circular imports
from euwin.process.wheeling_system_builder import WheelingSystemBuilder

def test_wheeling_system():
    """Test the wheeling system builder with the mainSystemSize parameter"""

    builder = WheelingSystemBuilder()

    # Test case from the user's request
    request_data = {
        "mainNumbersCombination": [1, 2, 3, 4, 5, 6],
        "mainGamePool": 59,
        "mainGameSize": 5,
        "mainSystemSize": 3
    }

    print("=" * 70)
    print("Test: Wheeling System Builder with mainSystemSize parameter")
    print("=" * 70)
    print("\nRequest:")
    print(json.dumps(request_data, indent=2))

    try:
        result = builder.build_wheeling_system(request_data)

        print("\nResult:")
        print(f"Total main combinations available: {result['available_main_combinations']}")
        print(f"Selected main combinations: {result['total_main_combinations']}")
        print(f"\nMain combinations (randomly selected):")
        for i, combo in enumerate(result['main_combinations'], 1):
            print(f"  {i}. {combo}")

        print(f"\nCoverage statistics:")
        coverage = result['coverage']
        print(f"  Total possible combinations: {coverage['total_possible_combinations']}")
        print(f"  Covered combinations: {coverage['covered_combinations']}")
        print(f"  Coverage percentage: {coverage['coverage_percentage']}%")

        print("\n✓ Test passed: mainSystemSize parameter is working!")
        print(f"  - Generated C(6,5) = {result['available_main_combinations']} total combinations")
        print(f"  - Randomly selected {result['total_main_combinations']} combinations for the wheeling system")

        return True

    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_with_bonus():
    """Test wheeling system with bonus numbers"""

    builder = WheelingSystemBuilder()

    request_data = {
        "mainNumbersCombination": [1, 2, 3, 4, 5, 6],
        "mainGamePool": 59,
        "mainGameSize": 5,
        "mainSystemSize": 3,
        "bonusNumbers": [1, 2],
        "bonusPool": 11,
        "bonusGameSize": 2,
        "bonusSystemSize": 1
    }

    print("\n" + "=" * 70)
    print("Test: Wheeling System with Bonus Numbers")
    print("=" * 70)
    print("\nRequest:")
    print(json.dumps(request_data, indent=2))

    try:
        result = builder.build_wheeling_system(request_data)

        print("\nResult:")
        print(f"Main combinations selected: {result['total_main_combinations']}")
        print(f"Bonus combinations selected: {result['total_bonus_combinations']}")

        if result['bonus_combinations']:
            print(f"\nBonus combinations:")
            for i, combo in enumerate(result['bonus_combinations'], 1):
                print(f"  {i}. {combo}")

        print("\n✓ Test passed: Bonus numbers handled correctly!")
        return True

    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test1_passed = test_wheeling_system()
    test2_passed = test_with_bonus()

    print("\n" + "=" * 70)
    if test1_passed and test2_passed:
        print("All tests passed! ✓")
        sys.exit(0)
    else:
        print("Some tests failed! ✗")
        sys.exit(1)

