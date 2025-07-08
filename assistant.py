"""Main LangGraph implementation for weather chatbot."""

import re
import logging
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Literal, Dict, Any
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from tools import get_weather

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class State(TypedDict):
    """State schema for conversation management."""
    messages: Annotated[list[BaseMessage], add_messages]


def detect_weather_query(message: str) -> bool:
    """
    Detect if a message is asking about weather information.
    
    Simple detection logic that checks for city names and weather keywords.
    
    Args:
        message: The user message to analyze
        
    Returns:
        True if the message appears to be a weather query, False otherwise
    """
    message_lower = message.lower()
    
    # Weather-related keywords
    weather_keywords = [
        'weather', 'temperature', 'temp', 'forecast', 'rain', 'sunny', 'cloudy',
        'hot', 'cold', 'humid', 'wind', 'storm', 'snow', 'climate'
    ]
    
    # Check if message contains weather keywords
    has_weather_keyword = any(keyword in message_lower for keyword in weather_keywords)
    
    # Simple city detection - look for patterns like "in [city]" or "weather [city]"
    city_patterns = [
        r'\bin\s+([a-zA-Z\s]+)',  # "in New York"
        r'weather\s+(?:in\s+)?([a-zA-Z\s]+)',  # "weather in Paris" or "weather Paris"
        r'temperature\s+(?:in\s+)?([a-zA-Z\s]+)',  # "temperature in London"
        r'forecast\s+(?:for\s+)?([a-zA-Z\s]+)',  # "forecast for Tokyo"
    ]
    
    has_city_mention = any(re.search(pattern, message_lower) for pattern in city_patterns)
    
    # Also check for direct city mentions with weather context
    if has_weather_keyword and len(message.split()) <= 10:  # Short messages more likely to be weather queries
        return True
    
    return has_weather_keyword and has_city_mention


def extract_city_from_message(message: str) -> str:
    """
    Extract city name from a weather query message.
    
    Args:
        message: The user message containing a city name
        
    Returns:
        The extracted city name, or the original message if no clear city is found
    """
    message_lower = message.lower()
    
    # City extraction patterns
    city_patterns = [
        r'\bin\s+([a-zA-Z\s]+?)(?:\s|$|\?|!|\.)',  # "in New York"
        r'weather\s+(?:in\s+)?([a-zA-Z\s]+?)(?:\s|$|\?|!|\.)',  # "weather in Paris"
        r'temperature\s+(?:in\s+)?([a-zA-Z\s]+?)(?:\s|$|\?|!|\.)',  # "temperature in London"
        r'forecast\s+(?:for\s+)?([a-zA-Z\s]+?)(?:\s|$|\?|!|\.)',  # "forecast for Tokyo"
    ]
    
    for pattern in city_patterns:
        match = re.search(pattern, message_lower)
        if match:
            city = match.group(1).strip()
            # Clean up common words that might be captured
            stop_words = ['the', 'a', 'an', 'is', 'are', 'was', 'were', 'today', 'tomorrow']
            city_words = [word for word in city.split() if word not in stop_words]
            if city_words:
                return ' '.join(city_words).title()
    
    # If no pattern matches, return the message for the tool to handle
    return message


def chat_node(state: State) -> Dict[str, Any]:
    """
    Handle normal conversation using the LLM.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with LLM response
    """
    # Initialize the LLM
    llm = ChatAnthropic(model_name="claude-3-haiku-20240307", temperature=0.7, timeout=30, stop=[])
    
    # Generate response
    response = llm.invoke(state["messages"])
    
    return {"messages": [response]}


def weather_tool_node(state: State) -> Dict[str, Any]:
    """
    Handle weather queries using the weather tool.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with weather information
    """
    last_message = state["messages"][-1]
    user_message = last_message.content if hasattr(last_message, 'content') and isinstance(last_message.content, str) else str(last_message)
    
    # Extract city from the message
    city = extract_city_from_message(user_message)
    
    # Call the weather tool
    weather_info = get_weather(city)
    
    # Return the weather information as an AI message
    return {"messages": [AIMessage(content=weather_info)]}


def route_message(state: State) -> Literal["chat", "weather"]:
    """
    Route messages to either chat or weather tool based on content.
    
    Args:
        state: Current conversation state
        
    Returns:
        The next node to execute ("chat" or "weather")
    """
    # Get the last message
    last_message = state["messages"][-1]
    user_message = last_message.content if hasattr(last_message, 'content') and isinstance(last_message.content, str) else str(last_message)
    
    # Check if it's a weather query
    if detect_weather_query(user_message):
        logger.info(f"Routing to weather tool for message: {user_message[:50]}...")
        return "weather"
    else:
        logger.info(f"Routing to chat for message: {user_message[:50]}...")
        return "chat"


def create_graph() -> CompiledStateGraph:
    """
    Create and compile the LangGraph workflow.
    
    Returns:
        Compiled StateGraph for the weather chatbot
    """
    # Create the graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("chat", chat_node)
    workflow.add_node("weather", weather_tool_node)
    
    # Add routing logic
    workflow.add_conditional_edges(
        START,
        route_message,
        {
            "chat": "chat",
            "weather": "weather"
        }
    )
    
    # Both nodes end the conversation
    workflow.add_edge("chat", END)
    workflow.add_edge("weather", END)
    
    # Compile the graph
    return workflow.compile()


# Create the compiled graph  
app = create_graph()


if __name__ == "__main__":
    # Example usage
    print("Weather Chatbot initialized!")
    print("You can ask about weather in any city or chat normally.")
    
    # Test with a weather query
    test_state = {"messages": [HumanMessage(content="What's the weather in Paris?")]}
    result = app.invoke(test_state)
    print(f"Response: {result['messages'][-1].content}")









