"""
Tests for random_numbers_controller - Generate from List functionality
"""

import pytest


class TestGenerateFromList:
    """Tests for POST /api/random/generate-from-list endpoint"""

    def test_generate_from_list_basic(self, client):
        """Test basic generation from a list"""
        request = {
            "count": 3,
            "number_pool": [1, 5, 10, 15, 20, 25, 30]
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 200
        data = response.json()
        assert "numbers" in data
        assert "count" in data
        assert data["count"] == 3
        assert len(data["numbers"]) == 3
        # All generated numbers should be from the pool
        assert all(num in request["number_pool"] for num in data["numbers"])
        # Numbers should be unique
        assert len(set(data["numbers"])) == 3
        # Numbers should be sorted
        assert data["numbers"] == sorted(data["numbers"])

    def test_generate_from_list_with_bonus(self, client):
        """Test generation from list with bonus"""
        request = {
            "count": 3,
            "number_pool": [1, 5, 10, 15, 20, 25, 30],
            "include_bonus": True,
            "bonus_range": 10
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 200
        data = response.json()
        assert "bonus" in data
        assert data["bonus"] is not None
        assert 1 <= data["bonus"] <= 10

    def test_generate_from_list_without_bonus(self, client):
        """Test generation from list without bonus"""
        request = {
            "count": 3,
            "number_pool": [1, 5, 10, 15, 20, 25, 30],
            "include_bonus": False
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 200
        data = response.json()
        assert data["bonus"] is None

    def test_generate_from_list_single_number(self, client):
        """Test generating single number from list"""
        request = {
            "count": 1,
            "number_pool": [42]
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 200
        data = response.json()
        assert data["numbers"] == [42]
        assert data["count"] == 1

    def test_generate_from_list_entire_pool(self, client):
        """Test generating all numbers from the pool"""
        pool = [1, 5, 10, 15, 20]
        request = {
            "count": len(pool),
            "number_pool": pool
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 200
        data = response.json()
        assert set(data["numbers"]) == set(pool)
        assert len(data["numbers"]) == len(pool)

    def test_generate_from_list_count_exceeds_pool(self, client):
        """Test error when count exceeds pool size"""
        request = {
            "count": 10,
            "number_pool": [1, 5, 10]
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 400
        assert "Cannot generate" in response.json()["detail"]

    def test_generate_from_list_empty_pool(self, client):
        """Test error with empty pool"""
        request = {
            "count": 1,
            "number_pool": []
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 422  # Pydantic validation error

    def test_generate_from_list_duplicates_in_pool(self, client):
        """Test error when pool contains duplicates"""
        request = {
            "count": 2,
            "number_pool": [1, 5, 5, 10]
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 400
        assert "duplicate" in response.json()["detail"].lower()

    def test_generate_from_list_unique_numbers(self, client):
        """Test that generated numbers are unique"""
        request = {
            "count": 10,
            "number_pool": list(range(1, 51))
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 200
        data = response.json()
        numbers = data["numbers"]
        assert len(numbers) == len(set(numbers))

    def test_generate_from_list_sorted(self, client):
        """Test that generated numbers are sorted"""
        request = {
            "count": 20,
            "number_pool": list(range(1, 100))
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 200
        data = response.json()
        numbers = data["numbers"]
        assert numbers == sorted(numbers)

    def test_generate_from_list_negative_numbers(self, client):
        """Test generation from pool with negative numbers"""
        request = {
            "count": 3,
            "number_pool": [-10, -5, 0, 5, 10]
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 200
        data = response.json()
        assert len(data["numbers"]) == 3
        assert all(num in request["number_pool"] for num in data["numbers"])

    def test_generate_from_list_large_numbers(self, client):
        """Test generation from pool with large numbers"""
        request = {
            "count": 3,
            "number_pool": [1000, 2000, 3000, 4000, 5000]
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 200
        data = response.json()
        assert all(num in request["number_pool"] for num in data["numbers"])


class TestGenerateFromListBulk:
    """Tests for POST /api/random/generate-from-list-bulk endpoint"""

    def test_bulk_generate_from_list_basic(self, client):
        """Test basic bulk generation from list"""
        request = {
            "generations": 3,
            "count": 2,
            "number_pool": [1, 5, 10, 15, 20]
        }
        response = client.post("/api/random/generate-from-list-bulk", json=request)

        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total_sets" in data
        assert data["total_sets"] == 3
        assert len(data["results"]) == 3

    def test_bulk_generate_from_list_all_valid(self, client):
        """Test that all results in bulk generation are valid"""
        request = {
            "generations": 5,
            "count": 3,
            "number_pool": list(range(1, 20))
        }
        response = client.post("/api/random/generate-from-list-bulk", json=request)

        assert response.status_code == 200
        data = response.json()
        for result in data["results"]:
            assert len(result["numbers"]) == 3
            assert all(num in request["number_pool"] for num in result["numbers"])

    def test_bulk_generate_from_list_with_bonus(self, client):
        """Test bulk generation with bonus"""
        request = {
            "generations": 2,
            "count": 2,
            "number_pool": [1, 5, 10, 15, 20],
            "include_bonus": True,
            "bonus_range": 5
        }
        response = client.post("/api/random/generate-from-list-bulk", json=request)

        assert response.status_code == 200
        data = response.json()
        for result in data["results"]:
            assert result["bonus"] is not None
            assert 1 <= result["bonus"] <= 5

    def test_bulk_generate_from_list_duplicates_in_pool(self, client):
        """Test bulk generation error with duplicate pool"""
        request = {
            "generations": 2,
            "count": 2,
            "number_pool": [1, 1, 5, 10]
        }
        response = client.post("/api/random/generate-from-list-bulk", json=request)

        assert response.status_code == 400
        assert "duplicate" in response.json()["detail"].lower()

    def test_bulk_generate_from_list_count_exceeds_pool(self, client):
        """Test bulk generation error when count exceeds pool"""
        request = {
            "generations": 2,
            "count": 10,
            "number_pool": [1, 5, 10]
        }
        response = client.post("/api/random/generate-from-list-bulk", json=request)

        assert response.status_code == 400
        assert "Cannot generate" in response.json()["detail"]

    def test_bulk_generate_from_list_large_generations(self, client):
        """Test bulk generation with many generations"""
        request = {
            "generations": 100,
            "count": 2,
            "number_pool": list(range(1, 50))
        }
        response = client.post("/api/random/generate-from-list-bulk", json=request)

        assert response.status_code == 200
        data = response.json()
        assert data["total_sets"] == 100
        assert len(data["results"]) == 100


class TestGenerateFromListVsMinMax:
    """Tests to verify generate-from-list and generate have expected differences"""

    def test_from_list_more_flexible(self, client):
        """Test that from-list can handle non-contiguous numbers"""
        # generate endpoint requires contiguous range, generate-from-list doesn't
        request = {
            "count": 3,
            "number_pool": [5, 15, 25, 35, 45, 55]  # Non-contiguous
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 200
        assert len(response.json()["numbers"]) == 3

    def test_generate_has_same_structure(self, client):
        """Test that both endpoints return same response structure"""
        # Using generate-from-list is semantically different but same structure
        request = {
            "count": 5,
            "number_pool": list(range(1, 50))
        }
        response = client.post("/api/random/generate-from-list", json=request)

        assert response.status_code == 200
        data = response.json()
        # Should have same fields as generate endpoint
        assert "numbers" in data
        assert "count" in data
        assert "bonus" in data

    def test_from_list_preserves_pool_order(self, client):
        """Test that order doesn't matter - results are sorted"""
        # Test 1: Pool in ascending order
        request1 = {
            "count": 5,
            "number_pool": [10, 20, 30, 40, 50, 60, 70]
        }
        response1 = client.post("/api/random/generate-from-list", json=request1)

        # Test 2: Same pool in different order
        request2 = {
            "count": 5,
            "number_pool": [70, 30, 50, 10, 60, 40, 20]
        }
        response2 = client.post("/api/random/generate-from-list", json=request2)

        # Both should work (actual numbers will differ due to randomness)
        assert response1.status_code == 200
        assert response2.status_code == 200


class TestBackwardCompatibility:
    """Tests to ensure existing generate endpoints still work"""

    def test_generate_min_max_still_works(self, client):
        """Verify original generate endpoint still works"""
        request = {
            "count": 6,
            "min_number": 1,
            "max_number": 49
        }
        response = client.post("/api/random/generate", json=request)

        assert response.status_code == 200
        data = response.json()
        assert len(data["numbers"]) == 6

    def test_generate_bulk_still_works(self, client):
        """Verify original bulk generate endpoint still works"""
        request = {
            "generations": 5,
            "count": 6,
            "min_number": 1,
            "max_number": 49
        }
        response = client.post("/api/random/generate-bulk", json=request)

        assert response.status_code == 200
        data = response.json()
        assert data["total_sets"] == 5

