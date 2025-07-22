from typing import List, Dict
from reviews.config import config
from google.cloud import bigquery


def fetch_reviews_by_movie_id(movie_id: str) -> List[Dict]:
    """
    Fetch all reviews for a given movie_id from the IMDB reviews public dataset using BigQuery.

    Args:
        movie_id (str): The movie_id to fetch the reviews for.

    Returns:
        List[Dict]: A list of dictionaries, each representing a review row.
    """
    client = config.get_bigquery_client()
    query = """
        SELECT *
        FROM `bigquery-public-data.imdb.reviews`
        WHERE movie_id = @movie_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("movie_id", "STRING", movie_id)
        ]
    )
    try:
        query_job = client.query(query, job_config=job_config)
        results = list(query_job.result())
        return [dict(row) for row in results]
    except Exception as e:
        # In production, log
        print(f"Error fetching reviews for movie_id {movie_id}: {e}")
        return []


def lookup_by_title(title: str) -> List[Dict]:
    """
    Simple case-insensitive title search using LIKE.
    
    Args:
        title (str): Movie title to search for
        
    Returns:
        List[Dict]: Matching reviews
    """
    client = config.get_bigquery_client()
    formatted_title = title.lower().strip()
    
    # this needs to be improved like the one above to handle special characters like apostrophes 
    query = f"""
        SELECT *
        FROM `bigquery-public-data.imdb.reviews`
        WHERE LOWER(title) LIKE '%{formatted_title}%'
    """
    
    try:
        query_job = client.query(query)
        results = list(query_job.result())
        return [dict(row) for row in results]
    except Exception as e:
        print(f"Error searching for title '{title}': {e}")
        return [] 