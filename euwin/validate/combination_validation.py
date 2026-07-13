"""
Combination Validation - Validates lottery number combinations
"""
from typing import List, Set
import logging

logger = logging.getLogger(__name__)


class CombinationValidation:
    """
    Validates lottery number combinations for range, duplicates, and constraints.
    """

    @staticmethod
    def invalid_range(numbers: List[int], max_value: int) -> str:
        """
        Check if numbers are within valid range (1 to max_value).

        Args:
            numbers: List of numbers to validate
            max_value: Maximum allowed value

        Returns:
            Error message string if invalid, empty string if valid
        """
        if not numbers:
            return "Numbers list cannot be empty"

        invalid_numbers = []

        for num in numbers:
            if num < 1 or num > max_value:
                invalid_numbers.append(num)

        if invalid_numbers:
            error_msg = (
                f"Numbers out of range [1, {max_value}]: {invalid_numbers}. "
                f"All numbers must be between 1 and {max_value}."
            )
            logger.warning(error_msg)
            return error_msg

        logger.debug(f"Numbers {numbers} are within valid range [1, {max_value}]")
        return ""

    @staticmethod
    def has_duplicates(numbers: List[int]) -> bool:
        """
        Check if list contains duplicate numbers.

        Args:
            numbers: List of numbers to check

        Returns:
            True if duplicates found, False otherwise
        """
        return len(numbers) != len(set(numbers))

    @staticmethod
    def get_duplicates(numbers: List[int]) -> List[int]:
        """
        Get list of duplicate numbers.

        Args:
            numbers: List of numbers to check

        Returns:
            List of numbers that appear more than once
        """
        seen: Set[int] = set()
        duplicates: Set[int] = set()

        for num in numbers:
            if num in seen:
                duplicates.add(num)
            else:
                seen.add(num)

        return sorted(list(duplicates))

    @staticmethod
    def validate_combination_size(numbers: List[int], max_size: int) -> str:
        """
        Validate that combination doesn't exceed maximum size.

        Args:
            numbers: List of numbers
            max_size: Maximum allowed size

        Returns:
            Error message if invalid, empty string if valid
        """
        if len(numbers) > max_size:
            error_msg = f"Combination size {len(numbers)} exceeds maximum {max_size}"
            logger.warning(error_msg)
            return error_msg

        return ""

    @staticmethod
    def validate_all(numbers: List[int], max_value: int) -> List[str]:
        """
        Perform all validations on a combination.

        Args:
            numbers: Numbers to validate
            max_value: Maximum allowed value

        Returns:
            List of error messages (empty if all valid)
        """
        errors = []

        if not numbers:
            errors.append("Numbers list cannot be empty")
            return errors

        # Check range
        range_error = CombinationValidation.invalid_range(numbers, max_value)
        if range_error:
            errors.append(range_error)

        # Check duplicates
        if CombinationValidation.has_duplicates(numbers):
            duplicates = CombinationValidation.get_duplicates(numbers)
            errors.append(f"Duplicate numbers found: {duplicates}")

        return errors

