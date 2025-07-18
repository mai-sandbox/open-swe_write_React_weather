"""
Simple Weather Chatbot with LangGraph

A basic chatbot that can chat normally and check weather for cities when needed.
Uses LangGraph StateGraph for workflow management with automatic routing between
chat and weather lookup functionality.
"""

from typing import TypedDict, List, Literal
import os
import re
from typing import cast
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

# Load environment variables
load_dotenv()


class State(TypedDict):
    """State class for conversation history management."""
    messages: List[BaseMessage]


def weather_tool(city: str) -> str:
    """
    Simulates weather lookup for cities.
    
    Args:
        city: Name of the city to get weather for
        
    Returns:
        Simulated weather information for the city
    """
    # Simulate weather data - in a real implementation this would call a weather API
    weather_conditions = [
        "sunny", "cloudy", "rainy", "partly cloudy", "overcast", "clear"
    ]
    temperatures = ["72°F (22°C)", "68°F (20°C)", "75°F (24°C)", "70°F (21°C)", "65°F (18°C)"]
    
    # Simple hash-based selection for consistent results
    condition_idx = hash(city.lower()) % len(weather_conditions)
    temp_idx = hash(city.lower() + "temp") % len(temperatures)
    
    condition = weather_conditions[condition_idx]
    temperature = temperatures[temp_idx]
    
    return f"The weather in {city} is currently {condition} with a temperature of {temperature}."


def chat_node(state: State) -> State:
    """
    Chat node for normal conversation using LLM.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with LLM response
    """
    # Initialize LLM
    api_key = os.getenv("OPENAI_API_KEY", "dummy-key-for-testing")
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        api_key=api_key
    )
    
    # Get response from LLM
    response = llm.invoke(state["messages"])
    
    # Update state with new message
    return {
        "messages": state["messages"] + [response]
    }


def weather_node(state: State) -> State:
    """
    Weather node that calls the weather tool.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with weather information
    """
    # Get the last human message
    last_message = state["messages"][-1]
    if isinstance(last_message, HumanMessage):
        message_text = str(last_message.content).lower()
        
        # Extract city name from the message
        # Simple pattern matching for city names
        city_patterns = [
            r"weather in ([a-zA-Z\s]+)",
            r"weather for ([a-zA-Z\s]+)",
            r"how.*weather.*in ([a-zA-Z\s]+)",
            r"what.*weather.*in ([a-zA-Z\s]+)",
            r"([a-zA-Z\s]+) weather"
        ]
        
        city = None
        for pattern in city_patterns:
            match = re.search(pattern, message_text)
            if match:
                city = match.group(1).strip()
                break
        
        if not city:
            # Fallback: look for common city names
            common_cities = ["new york", "london", "paris", "tokyo", "sydney", "berlin", "madrid", "rome"]
            for common_city in common_cities:
                if common_city in message_text:
                    city = common_city
                    break
        
        if city:
            # Get weather information
            weather_info = weather_tool(city.title())
            response = AIMessage(content=weather_info)
        else:
            # Fallback if no city found
            response = AIMessage(content="I'd be happy to help with weather information! Could you please specify which city you'd like to know about?")
    else:
        response = AIMessage(content="I'd be happy to help with weather information! Could you please specify which city you'd like to know about?")
    
    return {
        "messages": state["messages"] + [response]
    }


def router_function(state: State) -> Literal["chat", "weather"]:
    """
    Router function that detects weather questions by checking for city names and weather-related keywords.
    
    Args:
        state: Current conversation state
        
    Returns:
        "weather" if weather-related question detected, "chat" otherwise
    """
    # Get the last human message
    last_message = state["messages"][-1]
    if not isinstance(last_message, HumanMessage):
        return "chat"
    
    message_text = str(last_message.content).lower()
    
    # Weather-related keywords
    weather_keywords = [
        "weather", "temperature", "temp", "forecast", "rain", "sunny", "cloudy",
        "snow", "hot", "cold", "warm", "cool", "humid", "dry", "windy"
    ]
    
    # Check if message contains weather keywords
    has_weather_keyword = any(keyword in message_text for keyword in weather_keywords)
    
    # Check for city indicators
    city_indicators = [
        "in ", "at ", "for ", " weather", "weather in", "weather for",
        "how is", "what is", "what's the"
    ]
    
    has_city_indicator = any(indicator in message_text for indicator in city_indicators)
    
    # Route to weather if both weather keyword and city indicator are present
    if has_weather_keyword and has_city_indicator:
        return "weather"
    
    # Also route to weather for direct weather questions
    weather_patterns = [
        r"weather.*in",
        r"weather.*for",
        r"how.*weather",
        r"what.*weather",
        r"temperature.*in",
        r"temp.*in"
    ]
    
    for pattern in weather_patterns:
        if re.search(pattern, message_text):
            return "weather"
    
    return "chat"


# Create StateGraph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("chat", chat_node)
graph_builder.add_node("weather", weather_node)

# Add edges
graph_builder.add_edge(START, "chat")
graph_builder.add_conditional_edges(
    "chat",
    router_function,
    {
        "chat": "chat",
        "weather": "weather"
    }
)
graph_builder.add_edge("weather", END)
graph_builder.add_edge("chat", END)

# Compile the graph
compiled_graph = graph_builder.compile()


