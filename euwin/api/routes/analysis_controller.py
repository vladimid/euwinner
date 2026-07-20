from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from euwin.analysis.frequency_analyzer import analyze_frequency as perform_frequency_analysis

router = APIRouter()

class AnalysisRequest(BaseModel):
    draws: Optional[int] = Field(default=100, description="Number of draws to analyze (default: 100)")
    offset: Optional[int] = Field(default=0, description="Number of draws to skip from the beginning (default: 0)")
    number_range: Optional[List[int]] = Field(default=None, description="List of numbers to analyze (default: [1-59])")

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