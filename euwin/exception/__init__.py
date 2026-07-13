"""
Exception package for EUWINNER lottery wheeling system.

Custom exception classes for error handling throughout the application.
"""


class EUWinnerException(Exception):
    """Base exception for EUWINNER system"""
    pass


class InvalidCombinationException(EUWinnerException):
    """Raised when a lottery combination is invalid"""
    pass


class InvalidDrawException(EUWinnerException):
    """Raised when a draw entry is invalid"""
    pass


class InvalidNumbersException(EUWinnerException):
    """Raised when random numbers are invalid"""
    pass


class DataAccessException(EUWinnerException):
    """Raised when data access operations fail"""
    pass


class AnalysisException(EUWinnerException):
    """Raised when analysis operations fail"""
    pass

