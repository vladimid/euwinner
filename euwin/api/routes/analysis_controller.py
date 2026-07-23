from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Dict
from euwin.analysis.frequency_analyzer import analyze_frequency as perform_frequency_analysis

router = APIRouter()

class AnalysisRequest(BaseModel):
    draws: Optional[int] = Field(default=100, description="Number of draws to analyze (default: 100)")
    offset: Optional[int] = Field(default=0, description="Number of draws to skip from the beginning (default: 0)")
    number_range: Optional[List[int]] = Field(default=None, description="List of numbers to analyze. Can be: verbose list [21,22,23,24,25], range [21,25], or single number [21]. (default: [1-59])")
    number_range_end: Optional[int] = Field(default=None, description="Upper limit of range when number_range contains a single number")

    @model_validator(mode='before')
    @classmethod
    def validate_range_fields(cls, data):
        """Validate that number_range_end is only used when appropriate"""
        number_range_end = data.get('number_range_end')
        number_range = data.get('number_range')

        # number_range_end can only be used with a single-element number_range or when number_range is a 2-element range
        if number_range_end is not None:
            if number_range is None or not isinstance(number_range, list):
                raise ValueError("number_range_end can only be used with number_range")
            # It's valid if number_range is 1 element (will be combined with number_range_end)
            # OR if number_range is 2 elements (will be treated as range, number_range_end will be ignored)
            if len(number_range) > 2:
                raise ValueError("number_range_end can only be used when number_range is a single number or a 2-element range")

        return data

    @model_validator(mode='after')
    def normalize_number_range(self):
        """
        Normalize number_range to a verbose list.
        Supports:
        - None: uses default [1-59]
        - [n1, n2, ..., nN]: verbose list (kept as-is if more than 2 elements)
        - [n1, n2]: interpreted as range from n1 to n2 (inclusive)
        - [n1]: interpreted as single number, combined with number_range_end if provided
        """
        v = self.number_range
        
        if v is None:
            return self

        if len(v) == 0:
            raise ValueError("number_range cannot be empty")

        # If we have 2 elements, treat as range [start, end]
        if len(v) == 2:
            start, end = v[0], v[1]
            if start > end:
                raise ValueError(f"number_range start ({start}) cannot be greater than end ({end})")
            self.number_range = list(range(start, end + 1))
            return self

        # If we have 1 element and number_range_end is provided, treat as [start, number_range_end]
        if len(v) == 1:
            if self.number_range_end is not None:
                start = v[0]
                if start > self.number_range_end:
                    raise ValueError(f"number_range start ({start}) cannot be greater than number_range_end ({self.number_range_end})")
                self.number_range = list(range(start, self.number_range_end + 1))
            # If only one element and no number_range_end, keep as-is (single number)
            return self

        # If we have more than 2 elements, keep as verbose list
        return self


class FrequencyStats(BaseModel):
    number: int
    count: int

class AnalysisResponse(BaseModel):
    draws_analyzed: int
    offset: int
    number_range: List[int]
    most_frequent: List[int]
    least_frequent: List[int]
    never_drawn: List[int]
    frequency: Dict[int, int]
    total_balls_drawn: int

@router.post("/frequency")
async def analyze_frequency(request: Optional[AnalysisRequest] = None):
    """
    Analyze number frequency from lottery draws.

    Query Parameters:
    - draws: Number of draws to analyze (default: 100)
    - offset: Number of draws to skip from the beginning (default: 0)
    - number_range: List of numbers to analyze (default: [1-59])
    """
    try:
        if request is None:
            request = AnalysisRequest()

        # Perform the frequency analysis
        result = perform_frequency_analysis(
            draws=request.draws,
            offset=request.offset,
            number_range=request.number_range
        )

        return AnalysisResponse(
            draws_analyzed=result["draws_analyzed"],
            offset=result["offset"],
            number_range=result["number_range"],
            most_frequent=result["most_frequent"],
            least_frequent=result["least_frequent"],
            never_drawn=result["never_drawn"],
            frequency=result["frequency"],
            total_balls_drawn=result["total_balls_drawn"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))