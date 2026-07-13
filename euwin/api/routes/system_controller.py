from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import sys
from datetime import datetime, timezone
from euwin.process.wheeling_system_builder import WheelingSystemBuilder
from euwin.exception.exceptions import (
    NullParameterException,
    InvalidSchemaException,
    OutOfRangeException
)

router = APIRouter()
wheeling_builder = WheelingSystemBuilder()


def get_utc_timestamp() -> str:
    """Get current UTC timestamp as ISO format string"""
    return datetime.now(timezone.utc).isoformat()


# ==================== Request/Response Models ====================

class SystemStatus(BaseModel):
    """System status information"""
    status: str
    version: str = "1.0.0"
    timestamp: str
    python_version: str
    uptime_seconds: Optional[float] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""
    healthy: bool
    message: str
    timestamp: str


class SystemInfoResponse(BaseModel):
    """System information response"""
    application_name: str
    description: str
    version: str
    environment: str
    python_version: str
    timestamp: str


class ConfigurationResponse(BaseModel):
    """Configuration information (non-sensitive)"""
    environment: str
    debug_mode: bool
    api_version: str
    max_workers: Optional[int] = None


# ==================== Wheeling System Models ====================

class WheelingSystemRequest(BaseModel):
    """Request model for building a wheeling system"""
    mainNumbersCombination: List[int] = None
    mainGamePool: int = None
    mainGameSize: int = None
    mainSystemSize: int = None
    bonusNumbers: Optional[List[int]] = None
    bonusPool: Optional[int] = None
    bonusGameSize: Optional[int] = None
    bonusSystemSize: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "mainNumbersCombination": [1, 2, 3, 4, 5, 6],
                "mainGamePool": 59,
                "mainGameSize": 5,
                "mainSystemSize": 3,
                "bonusNumbers": [1, 2],
                "bonusPool": 11,
                "bonusGameSize": 2,
                "bonusSystemSize": 1
            }
        }


class WheelingSystemResponse(BaseModel):
    """Response model for wheeling system results"""
    main_combinations: List[List[int]]
    bonus_combinations: Optional[List[List[int]]] = None
    total_main_combinations: int
    total_bonus_combinations: int
    coverage: Dict[str, Any]
    parameters: Dict[str, Any]
    timestamp: str = None


class RandomWheelingSystemRequest(BaseModel):
    """Request model for building a random wheeling system"""
    mainGamePoolSize: int
    fullSystemSize: int
    bonusGamePoolSize: int
    bonusSize: int
    mainGameSize: int
    mainSystemSize: int
    bonusSystemSize: int

    class Config:
        json_schema_extra = {
            "example": {
                "mainGamePoolSize": 59,
                "fullSystemSize": 6,
                "bonusGamePoolSize": 11,
                "bonusSize": 2,
                "mainGameSize": 5,
                "mainSystemSize": 3,
                "bonusSystemSize": 1
            }
        }


# ==================== Endpoints ====================

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint.

    Returns:
        HealthCheckResponse indicating system health status
    """
    try:
        return HealthCheckResponse(
            healthy=True,
            message="System is operational",
            timestamp=get_utc_timestamp()
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Health check failed: {str(e)}"
        )


@router.get("/status", response_model=SystemStatus)
async def get_system_status():
    """
    Get detailed system status.

    Returns:
        SystemStatus with current system information
    """
    try:
        return SystemStatus(
            status="operational",
            version="1.0.0",
            timestamp=get_utc_timestamp(),
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving system status: {str(e)}"
        )


@router.get("/info", response_model=SystemInfoResponse)
async def get_system_info():
    """
    Get system and application information.

    Returns:
        SystemInfoResponse with application details
    """
    try:
        return SystemInfoResponse(
            application_name="EUWINNER",
            description="Lottery Wheeling System",
            version="1.0.0",
            environment="development",
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            timestamp=get_utc_timestamp()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving system info: {str(e)}"
        )


@router.get("/config", response_model=ConfigurationResponse)
async def get_configuration():
    """
    Get current application configuration (non-sensitive).

    Returns:
        ConfigurationResponse with configuration details
    """
    try:
        return ConfigurationResponse(
            environment="development",
            debug_mode=True,
            api_version="1.0.0",
            max_workers=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving configuration: {str(e)}"
        )


@router.get("/version")
async def get_version():
    """
    Get application version.

    Returns:
        Dictionary with version information
    """
    try:
        return {
            "application": "EUWINNER",
            "version": "1.0.0",
            "api_version": "1.0.0",
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving version: {str(e)}"
        )


@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint for deployment orchestration.

    Returns:
        Dictionary indicating readiness status
    """
    try:
        return {
            "ready": True,
            "timestamp": get_utc_timestamp()
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service not ready: {str(e)}"
        )


@router.post("", response_model=WheelingSystemResponse)
@router.post("/", response_model=WheelingSystemResponse)
async def build_wheeling_system_default(request: WheelingSystemRequest):
    """
    Build a wheeling (shorthand) system of lottery combinations.

    Default POST handler for /api/system endpoint.
    A wheeling system covers all or most possible combinations of selected numbers,
    reducing cost while improving odds of winning.

    Args:
        request: WheelingSystemRequest with lottery numbers and parameters

    Returns:
        WheelingSystemResponse with combinations and coverage statistics

    Raises:
        HTTPException: For validation errors or processing failures
    """
    try:
        # Convert Pydantic model to dict for builder
        request_dict = request.model_dump(exclude_none=True)

        # Build wheeling system
        result = wheeling_builder.build_wheeling_system(request_dict)

        return WheelingSystemResponse(
            main_combinations=result.get("main_combinations", []),
            bonus_combinations=result.get("bonus_combinations"),
            total_main_combinations=result.get("total_main_combinations", 0),
            total_bonus_combinations=result.get("total_bonus_combinations", 0),
            coverage=result.get("coverage", {}),
            parameters=result.get("parameters", {}),
            timestamp=get_utc_timestamp()
        )

    except NullParameterException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid request: {str(e)}"
        )
    except InvalidSchemaException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Schema validation failed: {str(e)}"
        )
    except OutOfRangeException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Value out of range: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error building wheeling system: {str(e)}"
        )



@router.post("/wheeling/random", response_model=WheelingSystemResponse)
async def build_random_wheeling_system(request: RandomWheelingSystemRequest):
    """
    Build a wheeling system with randomly generated numbers.

    Generates random combinations from specified pool sizes and builds
    a wheeling system from them.

    Args:
        request: RandomWheelingSystemRequest with pool sizes and parameters

    Returns:
        WheelingSystemResponse with random wheeling combinations

    Raises:
        HTTPException: For validation errors or processing failures
    """
    try:
        # Convert Pydantic model to dict for builder
        request_dict = request.model_dump()

        # Build random wheeling system
        result = wheeling_builder.build_random_wheeling_system(request_dict)

        return WheelingSystemResponse(
            main_combinations=result.get("main_combinations", []),
            bonus_combinations=result.get("bonus_combinations"),
            total_main_combinations=result.get("total_main_combinations", 0),
            total_bonus_combinations=result.get("total_bonus_combinations", 0),
            coverage=result.get("coverage", {}),
            parameters=result.get("parameters", {}),
            timestamp=get_utc_timestamp()
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error building random wheeling system: {str(e)}"
        )


