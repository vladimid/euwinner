"""
Demonstration: Random selection of wheeling combinations
Shows that the same pool generates different random selections each time
"""
import json
from euwin.process.wheeling_system_builder import WheelingSystemBuilder

def demo_random_selection():
    """
    Demonstrate that mainSystemSize properly randomly selects combinations
    from the full pool, rather than taking the first N or last N
    """

    builder = WheelingSystemBuilder()

    request_data = {
        "mainNumbersCombination": [1, 2, 3, 4, 5, 6],
        "mainGamePool": 59,
        "mainGameSize": 5,
        "mainSystemSize": 3
    }

    print("=" * 70)
    print("DEMONSTRATION: Random Selection of Wheeling Combinations")
    print("=" * 70)
    print("\nRequest parameters:")
    print(f"  Numbers selected: {request_data['mainNumbersCombination']}")
    print(f"  Combination size: {request_data['mainGameSize']} numbers per line")
    print(f"  System size: {request_data['mainSystemSize']} lines to select")

    print("\nMath:")
    print(f"  Total combinations available: C(6, 5) = 6")
    print(f"  All possible 5-from-6 combinations:")
    print(f"    [1, 2, 3, 4, 5]")
    print(f"    [1, 2, 3, 4, 6]")
    print(f"    [1, 2, 3, 5, 6]")
    print(f"    [1, 2, 4, 5, 6]")
    print(f"    [1, 3, 4, 5, 6]")
    print(f"    [2, 3, 4, 5, 6]")

    print("\n" + "-" * 70)
    print("Running 5 independent generations (each randomly selects 3):")
    print("-" * 70)

    for run in range(1, 6):
        result = builder.build_wheeling_system(request_data)
        print(f"\nRun {run}:")
        for i, combo in enumerate(result['main_combinations'], 1):
            print(f"  {i}. {combo}")

    print("\n" + "=" * 70)
    print("✓ Notice how each run produces different random selections!")
    print("  This proves the algorithm randomly picks N from the full pool")
    print("=" * 70)


def demo_comparison():
    """
    Compare different mainSystemSize values
    """
    builder = WheelingSystemBuilder()

    request_data = {
        "mainNumbersCombination": [1, 2, 3, 4, 5, 6, 7],
        "mainGamePool": 59,
        "mainGameSize": 4,
    }

    print("\n" + "=" * 70)
    print("DEMONSTRATION: Different System Sizes")
    print("=" * 70)
    print("\nRequest: 7 numbers, 4 per combination")
    print(f"Total possible: C(7, 4) = 35 combinations")

    for system_size in [5, 10, 20]:
        request_data['mainSystemSize'] = system_size
        result = builder.build_wheeling_system(request_data)

        print(f"\nWith mainSystemSize = {system_size}:")
        print(f"  Available combinations: {result['available_main_combinations']}")
        print(f"  Selected combinations: {result['total_main_combinations']}")
        print(f"  First 3 selected: {result['main_combinations'][:3]}")


if __name__ == "__main__":
    demo_random_selection()
    demo_comparison()

