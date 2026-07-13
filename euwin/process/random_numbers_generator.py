"""
Random Numbers Generator - Generates random number combinations for lottery systems
"""
from typing import List
import random
import logging

logger = logging.getLogger(__name__)


class RandomNumbersGenerator:
    """
    Generates random number combinations for lottery systems.
    Used for creating random wheeling systems.
    """

    @staticmethod
    def get_random_combination(
        pool_size: int,
        combination_size: int,
        seed: int = None
    ) -> List[int]:
        """
        Generate a random combination of numbers.

        Args:
            pool_size: Maximum number value (1 to pool_size)
            combination_size: How many numbers to select
            seed: Optional seed for reproducibility

        Returns:
            Sorted list of random unique numbers

        Raises:
            ValueError: If combination_size > pool_size
        """
        if combination_size > pool_size:
            raise ValueError(
                f"Cannot select {combination_size} numbers from pool of {pool_size}"
            )

        if seed is not None:
            random.seed(seed)

        # Generate random combination
        number_pool = list(range(1, pool_size + 1))
        combination = random.sample(number_pool, combination_size)

        logger.debug(f"Generated random combination from pool {pool_size}: {sorted(combination)}")

        return sorted(combination)

    @staticmethod
    def get_random_combinations(
        pool_size: int,
        combination_size: int,
        count: int,
        seed: int = None
    ) -> List[List[int]]:
        """
        Generate multiple random combinations.

        Args:
            pool_size: Maximum number value (1 to pool_size)
            combination_size: How many numbers in each combination
            count: How many combinations to generate
            seed: Optional seed for reproducibility

        Returns:
            List of random combinations, each being a sorted list

        Raises:
            ValueError: If parameters are invalid
        """
        if combination_size > pool_size:
            raise ValueError(
                f"Cannot select {combination_size} numbers from pool of {pool_size}"
            )

        if seed is not None:
            random.seed(seed)

        combinations = []
        for _ in range(count):
            number_pool = list(range(1, pool_size + 1))
            combination = random.sample(number_pool, combination_size)
            combinations.append(sorted(combination))

        logger.debug(f"Generated {len(combinations)} random combinations")

        return combinations

    @staticmethod
    def shuffle_numbers(numbers: List[int]) -> List[int]:
        """
        Randomly shuffle a list of numbers.

        Args:
            numbers: List of numbers to shuffle

        Returns:
            Shuffled list (original list is not modified)
        """
        shuffled = numbers.copy()
        random.shuffle(shuffled)
        return shuffled

