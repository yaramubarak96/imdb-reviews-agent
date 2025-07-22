from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm 
from reviews.tools import get_movie_reviews, get_movie_ids
from typing import List, Dict
import os 


##handle this better in production ... this is just for testing 
assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY is not set"


# Configure litellm
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
AGENT_MODEL = LiteLlm(model="openai/gpt-4o-mini")  # Using OpenAI's GPT-4 via litellm
ROOT_AGENT_MODEL = LiteLlm(model="openai/gpt-4o")

# Define the summary agent
summary_agent = Agent(
    name="summary_agent",
    description="I fetch and summarize movie reviews from IMDB.",
    tools=[get_movie_reviews, get_movie_ids],
    model = AGENT_MODEL,
    instruction="""
    You are a movie review assistant. When given a movie ID:
    1. Use get_movie_reviews to fetch the reviews
    2. Analyze the sentiment and content of the reviews
    3. Provide a brief, clear summary of what people think about the movie
    
    Always mention:
    - Overall sentiment (positive/negative/mixed)
    - Key points mentioned in reviews
    - Number of reviews analyzed

    Return in a one a paragraph summary.
    """
)

# Define the tag agent
tag_agent = Agent(
    name="tag_agent",
    description="I analyze movie reviews and extract relevant tags and themes.",
    tools=[get_movie_reviews, get_movie_ids],
    model = AGENT_MODEL,
    instruction="""
    You are a movie review tagging assistant. When given a movie title:
    1. Use get_movie_ids to find the movie ID
    2. Use get_movie_reviews to fetch the reviews
    3. Analyze the reviews and extract relevant tags in these categories:
        - Genre tags (e.g., action, drama, comedy)
        - Technical tags (e.g., cinematography, special effects, soundtrack)
        - Story tags (e.g., plot-driven, character-focused, twist ending)
        - Emotional tags (e.g., heartwarming, suspenseful, thought-provoking)
        - Content tags (e.g., violence, family-friendly, mature themes)
    
    Format your response as:
    
    GENRE TAGS:
    - tag1
    - tag2
    
    TECHNICAL TAGS:
    - tag1
    - tag2
    
    STORY TAGS:
    - tag1
    - tag2
    
    EMOTIONAL TAGS:
    - tag1
    - tag2
    
    CONTENT TAGS:
    - tag1
    - tag2
    
    REVIEW COUNT: [number of reviews analyzed]
    
    Only include tags that are mentioned or strongly implied by multiple reviews.
    Sort tags within each category by frequency of mention.
    """
)

# Define the root agent that coordinates between summary and tag agents
root_agent = Agent(
    name="movie_review_coordinator",
    description="I coordinate between summary and tagging agents to provide comprehensive movie review analysis.",
    tools=[get_movie_reviews, get_movie_ids],
    model=AGENT_MODEL,
    instruction="""
    You are the main Movie Review Coordinator. Your job is to analyze user queries and provide comprehensive movie review analysis.
    
    You have two specialized sub-agents:
    1. 'summary_agent': Provides concise summaries of movie reviews and overall sentiment
    2. 'tag_agent': Analyzes reviews and extracts relevant tags/themes in different categories
    
    How to handle queries:
    1. If the query explicitly asks for ONLY tags (e.g., "get tags for Matrix"), delegate to tag_agent
    2. If the query explicitly asks for ONLY summary (e.g., "summarize reviews for Matrix"), delegate to summary_agent
    3. For generic queries (e.g., "tell me about Matrix reviews"), first get the  summary and then the tags
    
    For generic queries, format your response as:
    
    SUMMARY:
    [summary from summary_agent]
    
    TAGS AND THEMES:
    [tags from tag_agent]
    
    Always ensure you're providing the most comprehensive analysis unless specifically asked to focus on one aspect.
    """,
    sub_agents=[summary_agent, tag_agent]
) 