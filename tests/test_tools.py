import pytest
from reviews.tools import get_movie_reviews

def test_basic_movie_review():
    """Test getting reviews for a specific movie ID"""
    result = get_movie_reviews("tt0105636")  # Trespass
    print("\nReviews for Trespass:")
    print(result)
    assert isinstance(result, list)
    assert len(result) > 0  # Should return some reviews


def test_empty_movie():
    """Test getting reviews for a movie with no reviews"""
    result = get_movie_reviews("asdfsdfs")  # Non-existent movie
    print("\nReviews for non-existent movie:")
    print(result)
    assert isinstance(result, list)
    assert len(result) == 0  # Should return empty string
