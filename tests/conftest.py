"""
Pytest configuration and fixtures for EUWINNER tests.
"""

import pytest
from fastapi.testclient import TestClient
from euwin.api.main import app


@pytest.fixture
def client():
    """Provides TestClient for FastAPI testing"""
    return TestClient(app)


@pytest.fixture
def sample_random_numbers_request():
    """Sample random number generation request"""
    return {
        "count": 6,
        "min_number": 1,
        "max_number": 49,
        "include_bonus": True,
        "bonus_range": 10
    }


@pytest.fixture
def sample_draw_entry():
    """Sample draw entry"""
    return {
        "draw_id": 1,
        "numbers": [3, 15, 27, 35, 41, 48],
        "bonus": 7
    }


@pytest.fixture
def sample_numbers_to_validate():
    """Sample numbers for validation"""
    return {
        "numbers": [3, 15, 27, 35, 41, 48],
        "min_allowed": 1,
        "max_allowed": 49,
        "allow_duplicates": False
    }


@pytest.fixture
def sample_bulk_generation():
    """Sample bulk generation request"""
    return {
        "generations": 5,
        "count": 6,
        "min_number": 1,
        "max_number": 49,
        "include_bonus": True,
        "bonus_range": 10
    }

