from typing import List, Dict
from reviews.data import fetch_reviews_by_movie_id, lookup_by_title
"""
Best Practice: Write clear, descriptive, and accurate docstrings for your tools. This is essential for the LLM to use the tool correctly.
"""

def get_movie_reviews(movie_id: str) -> List[Dict]:
    """
    Fetch movie reviews from BigQuery IMDB dataset for a specific movie.

    This function queries the BigQuery database to retrieve reviews and their associated
    sentiment analysis for a given movie ID.

    Args:
        movie_id (str): IMDB movie ID (e.g., 'tt0111161' for 'The Shawshank Redemption')

    Returns:
        List[Dict]: List of review dictionaries where each dictionary contains:
            - 'review' (str): The full text of the review
            - 'sentiment' (float): Sentiment score of the review
            - 'title' (str): Title of the movie being reviewed
            - 'reviewer_rating' (int): Rating of the reviewer
            etc... 

    Example return value:
        [
            {
                'review': 'An amazing cinematic masterpiece...',
                'sentiment': negative,
                'title': 'The Shawshank Redemption', 
                'reviewer_rating': 10, 
            },
            ...
        ]
    or an empty value 
        []
    """
    return fetch_reviews_by_movie_id(movie_id)


def get_movie_ids(title: str) -> List[Dict]:
    """
    Search for movie titles and return a list of matches with their IDs.
    
    This function helps the LLM find movie IDs by searching titles, which can then
    be used to fetch reviews using get_movie_reviews.
    
    This function is needed before you look up reviews!

    Args:
        search_term (str): Movie title or part of title to search for

    Returns:
        List[Dict]: List of movie dictionaries where each dictionary contains:
            - 'title' (str): The movie title
            - 'movie_id' (str): The IMDB movie ID
            - 'label' (str): The sentiment label if available
            
    Example return value:
        [
            {
                'title': 'The Shawshank Redemption',
                'movie_id': 'tt0111161',
                'label': 'Positive'
            },
            ...
        ]
    or an empty list if no matches found
    """
    return lookup_by_title(title)





