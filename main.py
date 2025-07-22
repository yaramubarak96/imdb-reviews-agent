import asyncio
from reviews.agents import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from reviews.app import call_agent_async


async def run_agent_query(query: str, runner: Runner, user_id: str, session_id: str):
    print(f"\nQuery: {query}")
    print("-" * 50)
    response = await call_agent_async(query, runner, user_id, session_id)
    print("\nAgent's response:")
    print(response)
    print("=" * 50)


async def main():
    # Setup agent
    user_id = "demo_user"
    session_id = "demo_session"
    
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
    
    # Run queries
    queries = [
        "Summarize reviews for  Return of the Jedi",
        "Get tags for Return of the Jedi",
        "Tell me about The Kite Runner" , 
        "Whats the movie A Funny Thing Happened on the Way to the Moon?" ,
    ]
    
    for query in queries:
        await run_agent_query(query, runner, user_id, session_id)


if __name__ == "__main__":
    asyncio.run(main()) 