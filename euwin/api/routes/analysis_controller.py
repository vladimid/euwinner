from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class AnalysisRequest(BaseModel):
    draws: List[List[int]]
    number_range: int

class AnalysisResponse(BaseModel):
    most_frequent: List[int]
    least_frequent: List[int]
    drawn_together: dict

@router.post("/frequency")
async def analyze_frequency(request: AnalysisRequest):
    """Analyze number frequency from past draws"""
    try:
        # Call your analysis.SingleNumberFrequency logic
        return AnalysisResponse(
            most_frequent=[1,2,3],
            least_frequent=[45,46,47],
            drawn_together={}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))