from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import random

router = APIRouter()


# ==================== Request/Response Models ====================

class RandomNumbersRequest(BaseModel):
    """Request model for generating random numbers"""
    count: int = Field(..., ge=1, le=100, description="Number of random numbers to generate")
    min_number: int = Field(..., ge=1, description="Minimum number in range")
    max_number: int = Field(..., ge=1, description="Maximum number in range")
    include_bonus: bool = Field(default=False, description="Include bonus number generation")
    bonus_range: Optional[int] = Field(default=None, description="Range for bonus number (if include_bonus=true)")


class RandomNumbersResponse(BaseModel):
    """Response model for random number generation"""
    numbers: List[int] = Field(..., description="Generated random numbers")
    bonus: Optional[int] = Field(default=None, description="Generated bonus number if requested")
    count: int = Field(..., description="Total count of numbers generated")
    seed: Optional[int] = Field(default=None, description="Random seed used for generation")


class BulkRandomGenerationRequest(BaseModel):
    """Request model for bulk random number generation"""
    generations: int = Field(..., ge=1, le=1000, description="Number of generation requests")
    count: int = Field(..., ge=1, le=100, description="Numbers per generation")
    min_number: int = Field(..., ge=1, description="Minimum number in range")
    max_number: int = Field(..., ge=1, description="Maximum number in range")
    include_bonus: bool = Field(default=False, description="Include bonus number generation")
    bonus_range: Optional[int] = Field(default=None, description="Range for bonus number")


class BulkRandomGenerationResponse(BaseModel):
    """Response model for bulk random number generation"""
    results: List[RandomNumbersResponse] = Field(..., description="List of generated random number sets")
    total_sets: int = Field(..., description="Total number of sets generated")


class RandomNumberValidationRequest(BaseModel):
    """Request model for validating random numbers"""
    numbers: List[int] = Field(..., min_items=1, description="Numbers to validate")
    min_allowed: int = Field(..., ge=1, description="Minimum allowed value")
    max_allowed: int = Field(..., ge=1, description="Maximum allowed value")
    allow_duplicates: bool = Field(default=False, description="Whether duplicates are allowed")


class RandomNumberValidationResponse(BaseModel):
    """Response model for number validation"""
    is_valid: bool = Field(..., description="Whether all numbers are valid")
    errors: List[str] = Field(default_factory=list, description="List of validation errors if any")
    total_numbers: int = Field(..., description="Total numbers checked")


class SequentialNumbersRequest(BaseModel):
    """Request model for sequential number generation"""
    count: int = Field(..., ge=1, le=100, description="Number of sequential numbers to generate")
    min_number: int = Field(..., ge=1, description="Starting number")


class SequentialNumbersResponse(BaseModel):
    """Response model for sequential numbers"""
    numbers: List[int] = Field(..., description="Generated sequential numbers")
    count: int = Field(..., description="Total count of numbers")


# ==================== Endpoints ====================

@router.post("/generate", response_model=RandomNumbersResponse)
async def generate_random_numbers(request: RandomNumbersRequest):
    """
    Generate random numbers within specified range.

    Args:
        request: RandomNumbersRequest containing count, min/max range, and optional bonus

    Returns:
        RandomNumbersResponse with generated numbers and optional bonus

    Raises:
        HTTPException: If parameters are invalid
    """
    try:
        # Validate range
        if request.min_number >= request.max_number:
            raise HTTPException(
                status_code=400,
                detail="min_number must be less than max_number"
            )

        # Check if requested count exceeds available numbers
        available_numbers = request.max_number - request.min_number + 1
        if request.count > available_numbers:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot generate {request.count} unique numbers from range [{request.min_number}, {request.max_number}]"
            )

        # Generate random numbers
        number_range = list(range(request.min_number, request.max_number + 1))
        generated_numbers = sorted(random.sample(number_range, request.count))

        # Generate bonus number if requested
        bonus = None
        if request.include_bonus and request.bonus_range:
            if request.bonus_range < 1:
                raise HTTPException(
                    status_code=400,
                    detail="bonus_range must be at least 1"
                )
            bonus = random.randint(1, request.bonus_range)

        return RandomNumbersResponse(
            numbers=generated_numbers,
            bonus=bonus,
            count=len(generated_numbers)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating random numbers: {str(e)}")


@router.post("/generate-bulk", response_model=BulkRandomGenerationResponse)
async def generate_bulk_random_numbers(request: BulkRandomGenerationRequest):
    """
    Generate multiple sets of random numbers in bulk.

    Useful for generating multiple lottery draw combinations at once.

    Args:
        request: BulkRandomGenerationRequest with generation parameters

    Returns:
        BulkRandomGenerationResponse with all generated sets

    Raises:
        HTTPException: If parameters are invalid
    """
    try:
        # Validate range
        if request.min_number >= request.max_number:
            raise HTTPException(
                status_code=400,
                detail="min_number must be less than max_number"
            )

        # Check if requested count exceeds available numbers
        available_numbers = request.max_number - request.min_number + 1
        if request.count > available_numbers:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot generate {request.count} unique numbers from range [{request.min_number}, {request.max_number}]"
            )

        results = []
        number_range = list(range(request.min_number, request.max_number + 1))

        for _ in range(request.generations):
            # Generate random numbers
            generated_numbers = sorted(random.sample(number_range, request.count))

            # Generate bonus if requested
            bonus = None
            if request.include_bonus and request.bonus_range:
                bonus = random.randint(1, request.bonus_range)

            results.append(RandomNumbersResponse(
                numbers=generated_numbers,
                bonus=bonus,
                count=len(generated_numbers)
            ))

        return BulkRandomGenerationResponse(
            results=results,
            total_sets=len(results)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in bulk generation: {str(e)}")


@router.post("/validate", response_model=RandomNumberValidationResponse)
async def validate_random_numbers(request: RandomNumberValidationRequest):
    """
    Validate a set of random numbers against specified criteria.

    Args:
        request: RandomNumberValidationRequest with numbers and validation rules

    Returns:
        RandomNumberValidationResponse with validation result and any errors
    """
    try:
        errors = []

        # Check number count
        if not request.numbers:
            errors.append("Numbers list cannot be empty")

        # Validate each number
        for num in request.numbers:
            if num < request.min_allowed or num > request.max_allowed:
                errors.append(
                    f"Number {num} is outside allowed range [{request.min_allowed}, {request.max_allowed}]"
                )

        # Check for duplicates if not allowed
        if not request.allow_duplicates and len(request.numbers) != len(set(request.numbers)):
            errors.append("Duplicate numbers found but not allowed")

        is_valid = len(errors) == 0

        return RandomNumberValidationResponse(
            is_valid=is_valid,
            errors=errors,
            total_numbers=len(request.numbers)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@router.get("/sequential")
async def get_sequential_numbers(
    count: int = Query(..., ge=1, le=100, description="Number of sequential numbers"),
    start: int = Query(..., ge=1, description="Starting number")
) -> SequentialNumbersResponse:
    """
    Generate sequential numbers starting from a given number.

    Useful for creating number pools or ranges for lottery analysis.

    Args:
        count: How many sequential numbers to generate
        start: Starting number

    Returns:
        SequentialNumbersResponse with sequential numbers
    """
    try:
        numbers = list(range(start, start + count))
        return SequentialNumbersResponse(
            numbers=numbers,
            count=len(numbers)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sequential numbers: {str(e)}")


@router.get("/range-info")
async def get_range_info(
    min_number: int = Query(..., ge=1, description="Minimum number in range"),
    max_number: int = Query(..., ge=1, description="Maximum number in range")
):
    """
    Get information about a number range.

    Useful for understanding what random selections are possible from a range.

    Args:
        min_number: Minimum value in range
        max_number: Maximum value in range

    Returns:
        Dictionary with range statistics
    """
    try:
        if min_number >= max_number:
            raise HTTPException(
                status_code=400,
                detail="min_number must be less than max_number"
            )

        available_count = max_number - min_number + 1

        return {
            "min": min_number,
            "max": max_number,
            "available_numbers": available_count,
            "middle": (min_number + max_number) / 2,
            "sum": sum(range(min_number, max_number + 1))
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating range info: {str(e)}")


@router.post("/seed-generate", response_model=RandomNumbersResponse)
async def generate_with_seed(
    request: RandomNumbersRequest,
    seed: int = Query(..., description="Random seed for reproducible generation")
):
    """
    Generate random numbers using a specific seed for reproducibility.

    Useful for testing or creating reproducible lottery drawings.

    Args:
        request: RandomNumbersRequest with generation parameters
        seed: Random seed value

    Returns:
        RandomNumbersResponse with generated numbers
    """
    try:
        # Validate range
        if request.min_number >= request.max_number:
            raise HTTPException(
                status_code=400,
                detail="min_number must be less than max_number"
            )

        # Check if requested count exceeds available numbers
        available_numbers = request.max_number - request.min_number + 1
        if request.count > available_numbers:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot generate {request.count} unique numbers from range [{request.min_number}, {request.max_number}]"
            )

        # Set seed for reproducibility
        random.seed(seed)

        # Generate random numbers
        number_range = list(range(request.min_number, request.max_number + 1))
        generated_numbers = sorted(random.sample(number_range, request.count))

        # Generate bonus number if requested
        bonus = None
        if request.include_bonus and request.bonus_range:
            bonus = random.randint(1, request.bonus_range)

        return RandomNumbersResponse(
            numbers=generated_numbers,
            bonus=bonus,
            count=len(generated_numbers),
            seed=seed
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating seeded random numbers: {str(e)}")

