"""
Custom exceptions for EUWINNER application
"""


class EUWinnerException(Exception):
    """Base exception class for EUWINNER application"""
    pass


class NullParameterException(EUWinnerException):
    """Raised when a required parameter is null or missing"""
    pass


class InvalidSchemaException(EUWinnerException):
    """Raised when request schema is invalid (missing or wrong parameters)"""
    pass


class OutOfRangeException(EUWinnerException):
    """Raised when a value is outside the allowed range"""
    pass


class InvalidCombinationException(EUWinnerException):
    """Raised when a number combination is invalid"""
    pass

