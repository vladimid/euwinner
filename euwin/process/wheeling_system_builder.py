"""
Wheeling System Builder - Main class for building lottery wheeling systems
Translates Java com.vld.euwin.process.WheelingSystemBuilder to Python
"""
from typing import Dict, Any, List, Optional
import logging
from euwin.process.combination_builder import CombinationBuilder
from euwin.process.random_numbers_generator import RandomNumbersGenerator
from euwin.validate.combination_validation import CombinationValidation
from euwin.validate.schema_validation import SchemaValidation
from euwin.exception.exceptions import (
    NullParameterException,
    InvalidSchemaException,
    OutOfRangeException
)

logger = logging.getLogger(__name__)


class WheelingSystemBuilder:
    """
    Builds wheeling (shorthand) systems of lottery lines (combinations).

    A wheeling system is a method of covering all or most possible combinations
    of numbers selected from a larger pool, reducing cost while improving odds.

    Translated from Java: com.vld.euwin.process.WheelingSystemBuilder
    """

    # Field names
    BONUS_SYSTEM_SIZE = "bonusSystemSize"
    BONUS_GAME_SIZE = "bonusGameSize"
    MAIN_GAME_POOL = "mainGamePool"
    BONUS_POOL = "bonusPool"
    MAIN_NUMBERS_COMBINATION = "mainNumbersCombination"
    BONUS_NUMBERS = "bonusNumbers"
    MAIN_GAME_SIZE = "mainGameSize"
    MAIN_SYSTEM_SIZE = "mainSystemSize"

    RETURN_JSON = "Numbers returned:\n %s"
    EMPTY_JSON_ERROR = "Request parameters cannot be null or empty"

    def __init__(self):
        """Initialize the WheelingSystemBuilder with validators and builders"""
        self.combination_builder = CombinationBuilder()
        self.random_numbers_generator = RandomNumbersGenerator()
        self.combination_validation = CombinationValidation()
        self.schema_validation = SchemaValidation()

    def build_wheeling_system(self, request_parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build a shorthand (wheeling) system of lottery lines (combinations).

        Args:
            request_parameters: Dictionary containing:
                - mainNumbersCombination (list of ints): Numbers for main game
                - mainGamePool (int): Maximum number in main pool
                - mainGameSize (int): Numbers drawn in main game
                - mainSystemSize (int): Numbers to use in system
                - bonusNumbers (list of ints, optional): Bonus numbers
                - bonusPool (int, optional): Maximum bonus number
                - bonusSystemSize (int, optional): Bonus system size

        Returns:
            Dictionary with wheeling system combinations and metadata

        Raises:
            NullParameterException: If parameters are null/empty
            InvalidSchemaException: If required fields are missing
            OutOfRangeException: If numbers are outside valid range
        """
        logger.info("WheelingSystemBuilder.build_wheeling_system")

        if request_parameters is None:
            logger.error(self.EMPTY_JSON_ERROR)
            raise NullParameterException(self.EMPTY_JSON_ERROR)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Request parameters: {request_parameters}")

        # Validate schema
        if not self.schema_validation.valid_schema(set(request_parameters.keys())):
            missing = self.schema_validation.get_missing_fields(set(request_parameters.keys()))
            error_msg = f"Request is missing parameters: {missing}"
            logger.error(error_msg)
            raise InvalidSchemaException(error_msg)

        # Extract and validate parameters
        main_game_pool: int = request_parameters.get(self.MAIN_GAME_POOL) or 0

        # Get main numbers combination - remove duplicates and sort
        main_numbers_combination: List[int] = list(
            sorted(set(request_parameters.get(self.MAIN_NUMBERS_COMBINATION, [])))
        )

        # Validate main numbers range
        invalid_range = self.combination_validation.invalid_range(
            main_numbers_combination,
            main_game_pool
        )
        if invalid_range:
            logger.error(invalid_range)
            raise OutOfRangeException(invalid_range)

        # Get bonus pool and numbers (optional)
        bonus_pool: Optional[int] = request_parameters.get(self.BONUS_POOL)
        bonus_numbers: Optional[List[int]] = None

        if self.BONUS_NUMBERS in request_parameters and request_parameters.get(self.BONUS_NUMBERS):
            bonus_numbers = list(
                sorted(set(request_parameters.get(self.BONUS_NUMBERS, [])))
            )

            # Validate bonus numbers range
            if bonus_pool:
                invalid_range = self.combination_validation.invalid_range(
                    bonus_numbers,
                    bonus_pool
                )
                if invalid_range:
                    logger.error(invalid_range)
                    raise OutOfRangeException(invalid_range)

        # Get game sizes
        main_game_size: int = request_parameters.get(self.MAIN_GAME_SIZE) or 0
        main_system_size: int = request_parameters.get(self.MAIN_SYSTEM_SIZE) or 0
        bonus_game_size: Optional[int] = request_parameters.get(self.BONUS_GAME_SIZE)
        bonus_system_size: Optional[int] = request_parameters.get(self.BONUS_SYSTEM_SIZE)

        # Use provided bonus_game_size or default to full bonus numbers set
        bonus_size = bonus_game_size if bonus_game_size else (len(bonus_numbers) if bonus_numbers else None)

        # Build wheeling system
        wheeling_system = self.combination_builder.create_wheeling_combinations(
            main_numbers_combination,
            bonus_numbers,
            main_game_size,
            main_system_size,
            bonus_size,
            bonus_system_size
        )

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Wheeling system created: {wheeling_system}")

        return wheeling_system

    def build_random_wheeling_system(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a shorthand system of combinations of random numbers.

        Args:
            request_data: Dictionary containing:
                - mainGamePoolSize (int): Size of main number pool
                - fullSystemSize (int): Full system size for main numbers
                - bonusGamePoolSize (int): Size of bonus pool
                - bonusSize (int): Size for bonus selection
                - mainGameSize (int): Numbers drawn in main game
                - mainSystemSize (int): Main system size
                - bonusSystemSize (int): Bonus system size

        Returns:
            Dictionary with random wheeling system

        Raises:
            NullParameterException: If parameters are null/empty
        """
        logger.info("WheelingSystemBuilder.build_random_wheeling_system")

        if request_data is None:
            logger.error(self.EMPTY_JSON_ERROR)
            raise NullParameterException(self.EMPTY_JSON_ERROR)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Request data: {request_data}")

        # Extract parameters
        main_game_pool_size: int = request_data.get("mainGamePoolSize") or 0
        full_system_size: int = request_data.get("fullSystemSize") or 0

        # Generate random main combination
        main_numbers_combination = self.random_numbers_generator.get_random_combination(
            main_game_pool_size,
            full_system_size
        )

        # Extract bonus parameters and generate bonus numbers
        bonus_game_pool_size: int = request_data.get("bonusGamePoolSize") or 0
        bonus_size: int = request_data.get("bonusSize") or 0
        bonus_numbers = self.random_numbers_generator.get_random_combination(
            bonus_game_pool_size,
            bonus_size
        )

        # Extract game sizes
        main_game_size: int = request_data.get(self.MAIN_GAME_SIZE) or 0
        main_system_size: int = request_data.get(self.MAIN_SYSTEM_SIZE) or 0
        bonus_system_size: int = request_data.get(self.BONUS_SYSTEM_SIZE) or 0

        # Build wheeling system with random numbers
        wheeling_system = self.combination_builder.create_wheeling_combinations(
            main_numbers_combination,
            bonus_numbers,
            main_game_size,
            main_system_size,
            bonus_size,
            bonus_system_size
        )

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Random wheeling system created: {wheeling_system}")

        return wheeling_system

    def get_sieved_wheeling_system(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs validation of system before it is processed into a wheeling system,
        sieves undesirable combinations.

        Args:
            request_data: System data to validate and sieve

        Returns:
            Validated/sieved system data
        """
        logger.info("WheelingSystemBuilder.get_sieved_wheeling_system")

        # Placeholder implementation
        # In Java version, this just returns the requestData as-is
        return request_data



