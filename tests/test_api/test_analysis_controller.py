"""
Tests for analysis_controller endpoints.
"""

import pytest
from euwin.api.routes.analysis_controller import AnalysisRequest


class TestAnalysisRequestRangeNormalization:
    """Tests for number_range normalization in AnalysisRequest"""

    def test_verbose_list_unchanged(self):
        """Test that a verbose list is kept as-is"""
        request = AnalysisRequest(number_range=[21, 22, 23, 24, 25])
        assert request.number_range == [21, 22, 23, 24, 25]

    def test_two_element_list_as_range(self):
        """Test that 2-element list is interpreted as range [start, end] inclusive"""
        request = AnalysisRequest(number_range=[21, 25])
        assert request.number_range == [21, 22, 23, 24, 25]

    def test_two_element_range_with_same_start_end(self):
        """Test 2-element range where start equals end"""
        request = AnalysisRequest(number_range=[21, 21])
        assert request.number_range == [21]

    def test_two_element_range_invalid_reversed(self):
        """Test that reversed range raises error"""
        with pytest.raises(ValueError, match="start.*cannot be greater than end"):
            AnalysisRequest(number_range=[25, 21])

    def test_single_element_with_number_range_end(self):
        """Test single number with number_range_end field"""
        request = AnalysisRequest(number_range=[21], number_range_end=25)
        assert request.number_range == [21, 22, 23, 24, 25]

    def test_single_element_without_number_range_end(self):
        """Test single number without number_range_end"""
        request = AnalysisRequest(number_range=[21])
        assert request.number_range == [21]

    def test_single_element_with_invalid_range_end(self):
        """Test single number with end < start"""
        with pytest.raises(ValueError, match="start.*cannot be greater than"):
            AnalysisRequest(number_range=[25], number_range_end=21)

    def test_none_range_stays_none(self):
        """Test that None number_range stays None"""
        request = AnalysisRequest(number_range=None)
        assert request.number_range is None

    def test_empty_list_raises_error(self):
        """Test that empty list raises error"""
        with pytest.raises(ValueError, match="cannot be empty"):
            AnalysisRequest(number_range=[])

    def test_number_range_end_without_number_range_raises_error(self):
        """Test that number_range_end without number_range raises error"""
        with pytest.raises(ValueError, match="number_range_end can only be used"):
            AnalysisRequest(number_range_end=25)

    def test_number_range_end_with_long_list_raises_error(self):
        """Test that number_range_end with >2 element list raises error"""
        with pytest.raises(ValueError, match="number_range_end can only be used"):
            AnalysisRequest(number_range=[1, 2, 3], number_range_end=25)

    def test_number_range_end_with_two_element_range(self):
        """Test number_range_end with 2-element range (end should be ignored or override)"""
        # The validator allows this (it's not an error), but the field_validator
        # will treat [21, 25] as a range and ignore number_range_end
        request = AnalysisRequest(number_range=[21, 25], number_range_end=30)
        # The 2-element list is treated as range, so [21, 25] becomes [21,22,23,24,25]
        assert request.number_range == [21, 22, 23, 24, 25]


class TestAnalysisRequestDefaults:
    """Tests for default values in AnalysisRequest"""

    def test_default_values(self):
        """Test that defaults are applied correctly"""
        request = AnalysisRequest()
        assert request.draws == 100
        assert request.offset == 0
        assert request.number_range is None

    def test_draws_default(self):
        """Test draws default value"""
        request = AnalysisRequest(offset=5, number_range=[1, 10])
        assert request.draws == 100

    def test_offset_default(self):
        """Test offset default value"""
        request = AnalysisRequest(draws=50, number_range=[1, 10])
        assert request.offset == 0


class TestAnalysisRequestEdgeCases:
    """Tests for edge cases in number_range handling"""

    def test_large_range(self):
        """Test with large range"""
        request = AnalysisRequest(number_range=[1, 59])
        assert request.number_range == list(range(1, 60))
        assert len(request.number_range) == 59

    def test_single_number_with_same_end(self):
        """Test single number where number_range_end equals the number"""
        request = AnalysisRequest(number_range=[21], number_range_end=21)
        assert request.number_range == [21]

    def test_range_with_negative_numbers(self):
        """Test range with negative numbers"""
        request = AnalysisRequest(number_range=[-5, -1])
        assert request.number_range == [-5, -4, -3, -2, -1]

    def test_range_with_large_numbers(self):
        """Test range with large numbers"""
        request = AnalysisRequest(number_range=[1000, 1005])
        assert request.number_range == [1000, 1001, 1002, 1003, 1004, 1005]

    def test_preserves_explicit_large_list(self):
        """Test that explicitly passing large list is preserved"""
        explicit_list = list(range(1, 100))
        request = AnalysisRequest(number_range=explicit_list)
        assert request.number_range == explicit_list


class TestAnalysisRequestIntegration:
    """Integration tests with full request"""

    def test_full_request_with_range(self):
        """Test full request with range specification"""
        request = AnalysisRequest(
            draws=50,
            offset=10,
            number_range=[20, 30]
        )
        assert request.draws == 50
        assert request.offset == 10
        assert request.number_range == list(range(20, 31))

    def test_full_request_with_single_and_end(self):
        """Test full request with single number and end"""
        request = AnalysisRequest(
            draws=75,
            offset=5,
            number_range=[21],
            number_range_end=25
        )
        assert request.draws == 75
        assert request.offset == 5
        assert request.number_range == [21, 22, 23, 24, 25]

    def test_full_request_verbose_range(self):
        """Test full request with verbose range"""
        request = AnalysisRequest(
            draws=100,
            offset=0,
            number_range=[5, 10, 15, 20, 25]
        )
        assert request.draws == 100
        assert request.offset == 0
        assert request.number_range == [5, 10, 15, 20, 25]

