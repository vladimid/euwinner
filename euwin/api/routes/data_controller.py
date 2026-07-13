from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import csv
import os

router = APIRouter()

# Define request/response models
class DrawEntryRequest(BaseModel):
    draw_id: int
    numbers: List[int]
    bonus: Optional[int] = None

class DrawEntryResponse(BaseModel):
    draw_id: int
    numbers: List[int]
    bonus: Optional[int]

# Path to the CSV file
CSV_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../../tests/data/lotto-draw-historyaa.csv"
)

# Translate your Spring @RestController endpoints
@router.get("/draws/{draw_id}")
async def get_draw(draw_id: int):
    """Get a specific draw by ID from lotto-draw-historyaa.csv"""
    try:
        # Read from CSV file
        csv_path = os.path.abspath(CSV_FILE_PATH)

        if not os.path.exists(csv_path):
            raise HTTPException(
                status_code=404,
                detail=f"CSV file not found at {csv_path}"
            )

        with open(csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row and row.get('DrawNumber'):
                    if int(row['DrawNumber']) == draw_id:
                        # Extract the 6 main balls
                        numbers = [
                            int(row['Ball 1']),
                            int(row['Ball 2']),
                            int(row['Ball 3']),
                            int(row['Ball 4']),
                            int(row['Ball 5']),
                            int(row['Ball 6']),
                        ]
                        bonus = int(row['Bonus Ball']) if row.get('Bonus Ball') else None

                        return DrawEntryResponse(
                            draw_id=draw_id,
                            numbers=sorted(numbers),
                            bonus=bonus
                        )

        # If we get here, draw_id was not found
        raise HTTPException(
            status_code=404,
            detail=f"Draw with ID {draw_id} not found in CSV"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/draws")
async def create_draw(draw: DrawEntryRequest):
    """Create a new draw entry"""
    # Your business logic here
    return draw