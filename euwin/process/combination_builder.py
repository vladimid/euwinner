"""
Combination Builder - Creates wheeling system combinations
Translates lottery number combinations into wheeling systems
"""
from typing import List, Optional, Dict, Any
import logging
import random

logger = logging.getLogger(__name__)


class CombinationBuilder:
    """
    Builds wheeling system combinations from lottery numbers.

    A wheeling system is a method of covering all or most possible
    combinations of numbers selected from a larger pool.
    """

    @staticmethod
    def create_wheeling_combinations(
        main_numbers: List[int],
        bonus_numbers: Optional[List[int]],
        main_game_size: int,
        main_system_size: int,
        bonus_size: Optional[int],
        bonus_system_size: Optional[int]
    ) -> Dict[str, Any]:
        """
        Create wheeling system combinations from given numbers.

        A wheeling system works by:
        1. Generating all possible combinations of main_game_size from main_numbers
        2. Randomly selecting main_system_size combinations from the total pool

        Args:
            main_numbers: List of main game numbers to select from
            bonus_numbers: List of bonus numbers to select from (optional)
            main_game_size: Size of each main combination (e.g., 5 means 5 numbers per line)
            main_system_size: Number of main combinations to randomly select (wheeling size)
            bonus_size: Size of each bonus combination (e.g., 2 means 2 numbers per line)
            bonus_system_size: Number of bonus combinations to randomly select

        Returns:
            Dictionary containing wheeling combinations with coverage statistics
        """
        logger.debug(f"Creating wheeling combinations with main_numbers={main_numbers}, "
                    f"bonus_numbers={bonus_numbers}, main_game_size={main_game_size}, "
                    f"main_system_size={main_system_size}")

        combinations = {
            "main_combinations": [],
            "bonus_combinations": [],
            "total_main_combinations": 0,
            "total_bonus_combinations": 0,
            "available_main_combinations": 0,
            "available_bonus_combinations": 0,
            "parameters": {
                "main_game_size": main_game_size,
                "main_system_size": main_system_size,
                "bonus_size": bonus_size,
                "bonus_system_size": bonus_system_size
            }
        }

        # Generate main number combinations
        if main_numbers and main_game_size and main_system_size:
            # Generate all possible combinations
            all_main_combos = CombinationBuilder._generate_combinations(
                main_numbers,
                main_game_size
            )
            combinations["available_main_combinations"] = len(all_main_combos)

            # Randomly select main_system_size combinations
            selected_combos = CombinationBuilder._select_random_combinations(
                all_main_combos,
                main_system_size
            )
            combinations["main_combinations"] = selected_combos
            combinations["total_main_combinations"] = len(selected_combos)

            logger.debug(f"Generated {len(all_main_combos)} total main combinations, "
                        f"selected {len(selected_combos)} for wheeling system")

        # Generate bonus number combinations if provided
        if bonus_numbers and bonus_size and bonus_system_size:
            # Generate all possible combinations
            all_bonus_combos = CombinationBuilder._generate_combinations(
                bonus_numbers,
                bonus_size
            )
            combinations["available_bonus_combinations"] = len(all_bonus_combos)

            # Randomly select bonus_system_size combinations
            selected_bonus_combos = CombinationBuilder._select_random_combinations(
                all_bonus_combos,
                bonus_system_size
            )
            combinations["bonus_combinations"] = selected_bonus_combos
            combinations["total_bonus_combinations"] = len(selected_bonus_combos)

            logger.debug(f"Generated {len(all_bonus_combos)} total bonus combinations, "
                        f"selected {len(selected_bonus_combos)} for wheeling system")

        # Calculate coverage statistics
        combinations["coverage"] = CombinationBuilder._calculate_coverage(
            len(main_numbers),
            main_game_size,
            main_game_size  # Draw size is same as game size
        )

        return combinations

    @staticmethod
    def _select_random_combinations(
        all_combinations: List[List[int]],
        count: int
    ) -> List[List[int]]:
        """
        Randomly select a subset of combinations from the full set.
        
        Args:
            all_combinations: List of all possible combinations
            count: Number of combinations to randomly select
            
        Returns:
            Randomly selected combinations (count or fewer if not enough available)
        """
        if count >= len(all_combinations):
            # If requesting more than available, return all
            return all_combinations
        
        if count <= 0:
            return []
        
        # Randomly select without replacement
        selected = random.sample(all_combinations, count)
        
        # Sort for consistent output
        return sorted([sorted(combo) for combo in selected])

    @staticmethod
    def _generate_combinations(numbers: List[int], r: int) -> List[List[int]]:
        """
        Generate all combinations of size r from numbers.
        Uses iterative approach for efficiency.

        Args:
            numbers: List of numbers to combine
            r: Size of each combination

        Returns:
            List of all possible combinations
        """
        if r > len(numbers) or r < 1:
            return []

        if r == 1:
            return [[n] for n in numbers]

        if r == len(numbers):
            return [sorted(numbers)]

        combinations = []
        n = len(numbers)

        # Use bit manipulation for combination generation
        from itertools import combinations as itertools_combinations
        for combo in itertools_combinations(numbers, r):
            combinations.append(list(combo))

        return combinations

    @staticmethod
    def _calculate_coverage(
        pool_size: int,
        system_size: int,
        draw_size: int
    ) -> Dict[str, Any]:
        """
        Calculate coverage statistics for wheeling system.

        Args:
            pool_size: Total numbers in pool
            system_size: Numbers selected for system
            draw_size: Numbers drawn in lottery

        Returns:
            Dictionary with coverage statistics
        """
        from math import factorial

        def combinations_count(n: int, k: int) -> int:
            if k > n or k < 0:
                return 0
            return factorial(n) // (factorial(k) * factorial(n - k))

        total_combinations = combinations_count(pool_size, draw_size)
        covered_combinations = combinations_count(system_size, draw_size)

        coverage_percent = (covered_combinations / total_combinations * 100) if total_combinations > 0 else 0

        return {
            "total_possible_combinations": total_combinations,
            "covered_combinations": covered_combinations,
            "coverage_percentage": round(coverage_percent, 2)
        }

