
from google.genai import types # For creating message Content/Parts

"""
FastAPI Application Setup for Movie Review Analysis Service

This module provides a FastAPI-based REST API for movie review analysis with three main endpoints.
The service uses structured logging, comprehensive error handling, and input validation.

FastAPI Setup:
-------------
- Uses FastAPI for modern, async-first API development
- Implements OpenAPI/Swagger documentation at /docs
- Request ID middleware for request tracing
- Health check endpoint at /health

For Production: 
- Add logging using ContextVars and Middleware
- Add Error handling with Fastapi 

request = {query:str, user_id : str , session_id : str}
Main Routes:
-----------
1. /reviews/chat [POST]
   - Main endpoint for the root agent
   - Handles generic movie review queries


2. /reviews/summary [POST]
   - Dedicated endpoint for review summarization
   - Provides concise summary and sentiment analysis
   - Request body: {"movie_title": "string"}
   - Returns: {"summary": "string"} 

3. /reviews/tags [POST]
   - Specialized endpoint for movie review tagging
   - Extracts and categorizes themes and aspects
   - Returns: {
       "tags": dict
       ) 
   - using pydantic should improve this 


"""

async def call_agent_async(query: str, runner, user_id, session_id):
  """Sends a query to the agent and prints the final response."""
  # Prepare the user's message in ADK format
  content = types.Content(role='user', parts=[types.Part(text=query)])

  final_response_text = "Agent did not produce a final response." # Default

  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
      #this is for DEBUG LOGGING 
      #print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

      if event.is_final_response():
          if event.content and event.content.parts:
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # Handle potential errors/escalations
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # Add more checks here if needed (e.g., specific error codes)
          break # Stop processing events once the final response is found

  return final_response_text


 


