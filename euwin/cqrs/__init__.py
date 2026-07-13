"""
CQRS package for EUWINNER lottery wheeling system.

Contains domain models and data transfer objects following CQRS patterns.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Draw:
    """Draw domain model"""
    draw_id: int
    draw_date: datetime
    numbers: List[int]
    bonus: Optional[int] = None
    lotto_type: str = "EUROMILLIONS"


@dataclass
class DrawEntry:
    """Draw entry data model"""
    draw_id: int
    numbers: List[int]
    bonus: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class Combination:
    """Lottery combination model"""
    combination_id: int
    numbers: List[int]
    bonus: Optional[int] = None
    odds: Optional[float] = None


__all__ = ["Draw", "DrawEntry", "Combination"]

