import pytest
from unittest.mock import patch, MagicMock
from reviews.data import fetch_reviews_by_movie_id, lookup_by_title

def test_fetch_reviews_by_movie_id_empty():
    results = fetch_reviews_by_movie_id('123w34Sdf')
    assert isinstance(results, list)
    assert len(results) == 0

def test_fetch_reviews_by_movie_id_real():
    """Test fetch_reviews_by_movie_id with a real movie_id."""
    results = fetch_reviews_by_movie_id('tt0085540')
    assert isinstance(results, list)
    assert len(results) > 0
    for review in results:
        assert review['movie_id'] == 'tt0085540'
        assert review['label'] in ('Positive', 'Negative', 'Neutral')

def test_lookup_by_title():
    """Test lookup_by_title with 'Trespass '."""
    results = lookup_by_title('Trespass ')
    assert isinstance(results, list)
    assert len(results) > 0
    for review in results:
        assert 'trespass' in  review['title'].lower()

def test_lookup_by_title_empty():
    """Test lookup_by_title with a title that shouldn't exist."""
    results = lookup_by_title('ThisMovieDefinitelyDoesNotExist12345')
    assert isinstance(results, list)
    assert len(results) == 0 