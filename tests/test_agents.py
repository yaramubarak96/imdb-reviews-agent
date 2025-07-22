import pytest
from unittest.mock import patch, MagicMock
from reviews.agents import summary_agent, tag_agent, root_agent
from reviews.config import config
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts
from google.adk.sessions import InMemorySessionService
from reviews.app import call_agent_async


MOCK_REVIEWS = [
    {"movie_id": "tt0085540", "label": "Positive", "review_text": "Amazing film, a true masterpiece"},
    {"movie_id": "tt0085540", "label": "Positive", "review_text": "Brilliant storytelling and acting"}
]


@pytest.mark.asyncio
async def test_summary_agent():
    user_id = "user_1"
    session_id = "session_001"
    """Test the review agent with real BigQuery call"""
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="movie_reviews_app", 
        user_id=user_id, 
        session_id=session_id
    )
    
    runner = Runner(
        agent=summary_agent,
        app_name="movie_reviews_app",
        session_service=session_service  # Pass the service, not the session
    )
    
    query = "Get reviews for Trespass"
    content = types.Content(role='user', parts=[types.Part(text=query)])
    final_response_text = "Agent did not produce a final response." # Default
    final_response_text = await call_agent_async(query,
                                        runner=runner,
                                        user_id=user_id,
                                        session_id=session_id)
    print("\nAgent's response:")
    print(final_response_text)
    
    assert final_response_text != "Agent did not produce a final response."
    assert isinstance(final_response_text, str), 'its not a string'
    assert len(final_response_text) > 0


@pytest.mark.asyncio
async def test_tag_agent():
    user_id = "test_user"
    session_id = "test_session"
    
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="movie_reviews_app",
        user_id=user_id,
        session_id=session_id
    )
    
    runner = Runner(
        agent=tag_agent,
        app_name="movie_reviews_app",
        session_service=session_service
    )
    
    query = "Get tags for The Matrix"
    response = await call_agent_async(query, runner, user_id, session_id)
    
    print("\nAgent's response:")
    print(response)
    
    assert response != "Agent did not produce a final response."
    assert isinstance(response, str)
    assert len(response) > 0
    assert "GENRE TAGS:" in response
    assert "TECHNICAL TAGS:" in response
    assert "REVIEW COUNT:" in response


@pytest.mark.asyncio
async def test_root_agent():
    user_id = "test_user"
    session_id = "test_session"
    
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="movie_reviews_app",
        user_id=user_id,
        session_id=session_id
    )
    
    runner = Runner(
        agent=root_agent,
        app_name="movie_reviews_app",
        session_service=session_service
    )
    
    # Test generic query (should get both summary and tags)
    query = "Tell me about The Matrix reviews"
    response = await call_agent_async(query, runner, user_id, session_id)
    print("\nRoot Agent's response (generic query):")
    print(response)
    
    assert response != "Agent did not produce a final response."
    assert isinstance(response, str)
    assert len(response) > 0
    assert "SUMMARY:" in response
    assert "TAGS AND THEMES:" in response
    
    # Test specific summary query
    query = "Summarize reviews for The Matrix"
    response = await call_agent_async(query, runner, user_id, session_id)
    print("\nRoot Agent's response (summary query):")
    print(response)
    
    assert response != "Agent did not produce a final response."
    assert isinstance(response, str)
    assert len(response) > 0
    assert "Overall sentiment" in response.lower()
    
    # Test specific tags query
    query = "Get tags for The Matrix"
    response = await call_agent_async(query, runner, user_id, session_id)
    print("\nRoot Agent's response (tags query):")
    print(response)
    
    assert response != "Agent did not produce a final response."
    assert isinstance(response, str)
    assert len(response) > 0
    assert "GENRE TAGS:" in response 