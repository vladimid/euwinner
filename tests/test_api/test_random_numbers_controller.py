"""
Tests for random_numbers_controller endpoints.
"""

import pytest


class TestGenerateRandomNumbers:
    """Tests for POST /api/random/generate endpoint"""

    def test_generate_basic(self, client, sample_random_numbers_request):
        """Test basic random number generation"""
        response = client.post("/api/random/generate", json=sample_random_numbers_request)

        assert response.status_code == 200
        data = response.json()
        assert "numbers" in data
        assert "count" in data
        assert data["count"] == 6
        assert len(data["numbers"]) == 6
        assert all(1 <= num <= 49 for num in data["numbers"])

    def test_generate_with_bonus(self, client):
        """Test random number generation with bonus"""
        request = {
            "count": 6,
            "min_number": 1,
            "max_number": 49,
            "include_bonus": True,
            "bonus_range": 10
        }
        response = client.post("/api/random/generate", json=request)

        assert response.status_code == 200
        data = response.json()
        assert "bonus" in data
        assert data["bonus"] is not None
        assert 1 <= data["bonus"] <= 10

    def test_generate_without_bonus(self, client):
        """Test random number generation without bonus"""
        request = {
            "count": 6,
            "min_number": 1,
            "max_number": 49,
            "include_bonus": False
        }
        response = client.post("/api/random/generate", json=request)

        assert response.status_code == 200
        data = response.json()
        assert data["bonus"] is None

    def test_invalid_range(self, client):
        """Test error when min_number >= max_number"""
        request = {
            "count": 6,
            "min_number": 49,
            "max_number": 1,
            "include_bonus": False
        }
        response = client.post("/api/random/generate", json=request)

        assert response.status_code == 400
        assert "min_number must be less than max_number" in response.json()["detail"]

    def test_count_exceeds_available(self, client):
        """Test error when count exceeds available numbers"""
        request = {
            "count": 100,
            "min_number": 1,
            "max_number": 49,
            "include_bonus": False
        }
        response = client.post("/api/random/generate", json=request)

        assert response.status_code == 400
        assert "Cannot generate" in response.json()["detail"]

    def test_numbers_are_sorted(self, client):
        """Test that generated numbers are sorted"""
        request = {
            "count": 10,
            "min_number": 1,
            "max_number": 100,
            "include_bonus": False
        }
        response = client.post("/api/random/generate", json=request)

        assert response.status_code == 200
        numbers = response.json()["numbers"]
        assert numbers == sorted(numbers)

    def test_numbers_are_unique(self, client):
        """Test that generated numbers are unique"""
        request = {
            "count": 20,
            "min_number": 1,
            "max_number": 100,
            "include_bonus": False
        }
        response = client.post("/api/random/generate", json=request)

        assert response.status_code == 200
        numbers = response.json()["numbers"]
        assert len(numbers) == len(set(numbers))


class TestGenerateBulk:
    """Tests for POST /api/random/generate-bulk endpoint"""

    def test_bulk_generate_basic(self, client, sample_bulk_generation):
        """Test basic bulk generation"""
        response = client.post("/api/random/generate-bulk", json=sample_bulk_generation)

        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total_sets" in data
        assert data["total_sets"] == 5
        assert len(data["results"]) == 5

    def test_bulk_generate_all_valid(self, client):
        """Test that all results in bulk generation are valid"""
        request = {
            "generations": 10,
            "count": 6,
            "min_number": 1,
            "max_number": 49,
            "include_bonus": False
        }
        response = client.post("/api/random/generate-bulk", json=request)

        assert response.status_code == 200
        data = response.json()
        for result in data["results"]:
            assert len(result["numbers"]) == 6
            assert all(1 <= num <= 49 for num in result["numbers"])

    def test_bulk_invalid_range(self, client):
        """Test bulk generation with invalid range"""
        request = {
            "generations": 5,
            "count": 6,
            "min_number": 49,
            "max_number": 1,
            "include_bonus": False
        }
        response = client.post("/api/random/generate-bulk", json=request)

        assert response.status_code == 400


class TestValidateRandomNumbers:
    """Tests for POST /api/random/validate endpoint"""

    def test_validate_valid_numbers(self, client, sample_numbers_to_validate):
        """Test validation of valid numbers"""
        response = client.post("/api/random/validate", json=sample_numbers_to_validate)

        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is True
        assert len(data["errors"]) == 0
        assert data["total_numbers"] == 6

    def test_validate_out_of_range(self, client):
        """Test validation of numbers outside allowed range"""
        request = {
            "numbers": [3, 15, 27, 35, 41, 100],
            "min_allowed": 1,
            "max_allowed": 49,
            "allow_duplicates": False
        }
        response = client.post("/api/random/validate", json=request)

        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is False
        assert len(data["errors"]) > 0

    def test_validate_duplicates_not_allowed(self, client):
        """Test validation with duplicate numbers when not allowed"""
        request = {
            "numbers": [3, 15, 27, 35, 41, 41],
            "min_allowed": 1,
            "max_allowed": 49,
            "allow_duplicates": False
        }
        response = client.post("/api/random/validate", json=request)

        assert response.status_code == 200
        data = response.json()
        assert data["is_valid"] is False
        assert any("Duplicate" in error for error in data["errors"])

    def test_validate_duplicates_allowed(self, client):
        """Test validation with duplicate numbers when allowed"""
        request = {
            "numbers": [3, 15, 27, 35, 41, 41],
            "min_allowed": 1,
            "max_allowed": 49,
            "allow_duplicates": True
        }
        response = client.post("/api/random/validate", json=request)

        assert response.status_code == 200
        data = response.json()
        # Should pass since duplicates are allowed and all are in range
        assert data["is_valid"] is True


class TestSequentialNumbers:
    """Tests for GET /api/random/sequential endpoint"""

    def test_sequential_basic(self, client):
        """Test sequential number generation"""
        response = client.get("/api/random/sequential?count=10&start=1")

        assert response.status_code == 200
        data = response.json()
        assert data["numbers"] == list(range(1, 11))
        assert data["count"] == 10

    def test_sequential_custom_start(self, client):
        """Test sequential numbers with custom start"""
        response = client.get("/api/random/sequential?count=5&start=10")

        assert response.status_code == 200
        data = response.json()
        assert data["numbers"] == list(range(10, 15))
        assert data["count"] == 5


class TestRangeInfo:
    """Tests for GET /api/random/range-info endpoint"""

    def test_range_info_basic(self, client):
        """Test getting range information"""
        response = client.get("/api/random/range-info?min_number=1&max_number=49")

        assert response.status_code == 200
        data = response.json()
        assert data["min"] == 1
        assert data["max"] == 49
        assert data["available_numbers"] == 49
        assert data["middle"] == 25.0

    def test_range_info_invalid(self, client):
        """Test range info with invalid range"""
        response = client.get("/api/random/range-info?min_number=49&max_number=1")

        assert response.status_code == 400


class TestSeedGenerate:
    """Tests for POST /api/random/seed-generate endpoint"""

    def test_seed_generate_reproducible(self, client):
        """Test that same seed produces same numbers"""
        request = {
            "count": 6,
            "min_number": 1,
            "max_number": 49,
            "include_bonus": False
        }

        # First generation
        response1 = client.post("/api/random/seed-generate?seed=12345", json=request)
        data1 = response1.json()

        # Second generation with same seed
        response2 = client.post("/api/random/seed-generate?seed=12345", json=request)
        data2 = response2.json()

        assert data1["numbers"] == data2["numbers"]
        assert data1["seed"] == 12345

    def test_seed_generate_different_seeds(self, client):
        """Test that different seeds produce different numbers"""
        request = {
            "count": 6,
            "min_number": 1,
            "max_number": 49,
            "include_bonus": False
        }

        response1 = client.post("/api/random/seed-generate?seed=123", json=request)
        data1 = response1.json()

        response2 = client.post("/api/random/seed-generate?seed=456", json=request)
        data2 = response2.json()

        # Very likely different (not guaranteed but extremely probable)
        assert data1["numbers"] != data2["numbers"]

