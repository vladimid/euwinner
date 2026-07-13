"""
Schema Validation - Validates request schema for wheeling system
"""
from typing import Set
import logging

logger = logging.getLogger(__name__)


class SchemaValidation:
    """
    Validates that request contains all required parameters.
    """

    # Required parameters for building wheeling system
    REQUIRED_FIELDS = {
        "mainNumbersCombination",
        "mainGamePool",
        "mainGameSize",
        "mainSystemSize"
    }

    # Optional parameters
    OPTIONAL_FIELDS = {
        "bonusNumbers",
        "bonusPool",
        "bonusGameSize",
        "bonusSystemSize"
    }

    # All allowed fields
    ALL_ALLOWED_FIELDS = REQUIRED_FIELDS | OPTIONAL_FIELDS

    @staticmethod
    def valid_schema(keys: Set[str]) -> bool:
        """
        Validate that request contains all required fields and no invalid fields.

        Args:
            keys: Set of keys from the request

        Returns:
            True if schema is valid, False otherwise
        """
        # Check if all required fields are present
        if not SchemaValidation.REQUIRED_FIELDS.issubset(keys):
            missing = SchemaValidation.REQUIRED_FIELDS - keys
            logger.error(f"Missing required fields: {missing}")
            return False

        # Check for invalid/unknown fields
        invalid = keys - SchemaValidation.ALL_ALLOWED_FIELDS
        if invalid:
            logger.warning(f"Unknown fields in request: {invalid}")
            # Note: We still allow the request, just log the warning
            # Change this to return False if strict validation is needed

        logger.debug(f"Schema validation passed for fields: {keys}")
        return True

    @staticmethod
    def get_missing_fields(keys: Set[str]) -> Set[str]:
        """
        Get list of missing required fields.

        Args:
            keys: Set of keys from the request

        Returns:
            Set of missing required field names
        """
        return SchemaValidation.REQUIRED_FIELDS - keys

    @staticmethod
    def get_unknown_fields(keys: Set[str]) -> Set[str]:
        """
        Get list of unknown/invalid fields.

        Args:
            keys: Set of keys from the request

        Returns:
            Set of unknown field names
        """
        return keys - SchemaValidation.ALL_ALLOWED_FIELDS

