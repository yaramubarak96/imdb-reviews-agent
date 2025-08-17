
import streamlit as st
import asyncio
from reviews.agents import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from reviews.app import call_agent_async
import re 


async def run_agent_query(query: str, runner: Runner, user_id: str, session_id: str):
    response = await call_agent_async(query, runner, user_id, session_id)
    return response

def clean_event(event): 
    identifiers = ('name', 'Author', 'Event', 'args', 'role')
    
    name_match = re.search(r"name='([^']+)'", event)
    name = name_match.group(1) if name_match else None
    
    author_match = re.search(r"Author: ([^,]+)", event)
    author = author_match.group(1) if author_match else None
    
    
    args_match = re.search(r"args=({[^}]+})", event)
    args = args_match.group(1) if args_match else None
    
    role_match = re.search(r"role='([^']+)'", event)
    role = role_match.group(1) if role_match else None

    response_match = re.search(r"response=", event)
    response = "Response Found" if response_match else None
    
    if response_match :
        event_type = "Function Response"
    elif name == "transfer_to_agent":
        event_type = "Agent Transfer"
    else:
        event_type = "Function Call"

    agent_name = re.search(r"agent_name': '([^']+)'", args).group(1) if event_type == 'Agent Transfer' and args else None
    args = None if agent_name else args 
    
    return {"Event Type": event_type , 
    "Initiator" : author, 
    "Function Name": name, 
    "Agent Name": agent_name,
    "Function Arguments": args , 
    "Function Response": response,
    "Role": role,
    "full stack": event}

async def main_streamlit():
    st.title("Movie Review Agent")

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
    
    query = st.text_input("Enter your query about a movie review:")
    
    if st.button("Chat with Movie Review Agents") and query:
        with st.spinner("Agents are Working..."):        
            response, debug_events = await run_agent_query(query, runner, user_id, session_id)
            
            # Display Agent Trace first with pretty formatting
            st.subheader("🤖 Agent Trace")
            
            for i, event in enumerate(debug_events, 1):
                result_dict = clean_event(event)
                
                # Create expandable section for each event with prettier header
                event_type = result_dict.get('Event Type', 'Unknown Event')
                function_name = result_dict.get('Function Name', '')
                agent_name = result_dict.get('Agent Name', '')
                
                # Choose emoji and display name based on event type
                if event_type == 'Agent Transfer':
                    emoji = "🔄"
                    display_name = f"**{agent_name}**" if agent_name else "**Agent Transfer**"
                elif event_type == 'Function Response':
                    emoji = "💬"
                    display_name = f"**{function_name}** Response" if function_name else "**Function Response**"
                else:  # Function Call
                    emoji = "⚡"
                    display_name = f"**{function_name}**" if function_name else "**Function Call**"
                
                with st.expander(f"## {emoji} Step {i}: {display_name}", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if result_dict.get('Initiator'):
                            st.write(f"**🎭 Initiator:** {result_dict['Initiator']}")
                        if result_dict.get('Function Name'):
                            st.write(f"**⚡ Function:** {result_dict['Function Name']}")
                        if result_dict.get('Agent Name'):
                            st.write(f"**🤖 Agent:** {result_dict['Agent Name']}")
                        if result_dict.get('Role'):
                            st.write(f"**👤 Role:** {result_dict['Role']}")
                    
                    with col2:
                        if result_dict.get('Function Arguments'):
                            st.write(f"**📝 Arguments:** {result_dict['Function Arguments']}")
                        if result_dict.get('Function Response'):
                            st.write(f"**💬 Response:** {result_dict['Function Response']}")
                    
                    # Show raw event in a code block without nested expander
                    st.write("**🔍 Raw Event Details:**")
                    st.code(result_dict['full stack'], language='python')
            
            st.divider()
            
            # Display final response
            st.subheader("✨ Final Response")
            st.success(response) 

if __name__ == "__main__":
    asyncio.run(main_streamlit())
