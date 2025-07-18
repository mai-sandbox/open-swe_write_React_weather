"""
Simple Weather Chatbot with LangGraph

A basic chatbot that can have normal conversations and check weather for cities.
Uses LangGraph for workflow management with automatic routing between chat and weather lookup.
"""

from typing import TypedDict, List, Literal
import re
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    """State class for managing conversation history."""
    messages: List[BaseMessage]


def weather_tool(city: str) -> str:
    """
    Simulates weather lookup for cities.
    
    Args:
        city: Name of the city to get weather for
        
    Returns:
        Simulated weather information for the city
    """
    # Simple weather simulation with varied responses
    weather_conditions = [
        f"The weather in {city} is sunny with a temperature of 72°F (22°C). Perfect day to go outside!",
        f"It's partly cloudy in {city} with a temperature of 68°F (20°C). Light breeze from the west.",
        f"Currently raining in {city} with a temperature of 65°F (18°C). Don't forget your umbrella!",
        f"The weather in {city} is overcast with a temperature of 70°F (21°C). Might clear up later.",
        f"It's a beautiful clear day in {city} with a temperature of 75°F (24°C). Great weather for outdoor activities!"
    ]
    
    # Use city name length to determine which weather condition to return (for consistency)
    weather_index = len(city) % len(weather_conditions)
    return weather_conditions[weather_index]


def chatbot_node(state: State) -> State:
    """
    Handles normal conversation without weather lookup.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with chatbot response
    """
    last_message = state["messages"][-1]
    
    # Generate a friendly conversational response
    if "hello" in last_message.content.lower() or "hi" in last_message.content.lower():
        response = "Hello! I'm here to help you with weather information or just have a chat. How can I assist you today?"
    elif "how are you" in last_message.content.lower():
        response = "I'm doing great, thank you for asking! I'm ready to help you with weather information or answer any questions you might have."
    elif "thank" in last_message.content.lower():
        response = "You're very welcome! Is there anything else I can help you with?"
    elif "bye" in last_message.content.lower() or "goodbye" in last_message.content.lower():
        response = "Goodbye! Feel free to come back anytime if you need weather information or just want to chat!"
    else:
        response = "That's interesting! I'm here to help with weather information for any city, or we can continue chatting about other topics. What would you like to know?"
    
    # Add the AI response to the conversation
    ai_message = AIMessage(content=response)
    return {"messages": state["messages"] + [ai_message]}


def weather_node(state: State) -> State:
    """
    Handles weather-related queries using the weather tool.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with weather information
    """
    last_message = state["messages"][-1]
    
    # Extract city name from the message
    city = extract_city_from_message(last_message.content)
    
    if city:
        # Use the weather tool to get weather information
        weather_info = weather_tool(city)
        response = weather_info
    else:
        # Fallback if no city is detected
        response = "I'd be happy to help you check the weather! Could you please specify which city you'd like to know about?"
    
    # Add the AI response to the conversation
    ai_message = AIMessage(content=response)
    return {"messages": state["messages"] + [ai_message]}


def extract_city_from_message(message: str) -> str:
    """
    Extracts city name from a message.
    
    Args:
        message: User message to extract city from
        
    Returns:
        Extracted city name or empty string if not found
    """
    # Simple city extraction - look for capitalized words that might be cities
    # This is a basic implementation that looks for patterns like "weather in Paris" or "Paris weather"
    
    # Common patterns for weather queries
    patterns = [
        r"weather in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        r"weather for ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*) weather",
        r"temperature in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        r"how.*weather.*in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        r"what.*weather.*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    # If no pattern matches, look for any capitalized word that might be a city
    words = message.split()
    for word in words:
        if word and word[0].isupper() and len(word) > 2:
            # Skip common non-city words
            if word.lower() not in ['the', 'what', 'how', 'when', 'where', 'weather', 'temperature', 'today', 'tomorrow']:
                return word
    
    return ""


def router(state: State) -> Literal["chatbot", "weather"]:
    """
    Routes messages to either chatbot or weather node based on content.
    
    Args:
        state: Current conversation state
        
    Returns:
        Node name to route to ("chatbot" or "weather")
    """
    last_message = state["messages"][-1]
    message_content = last_message.content.lower()
    
    # Weather-related keywords
    weather_keywords = [
        "weather", "temperature", "temp", "forecast", "rain", "sunny", "cloudy", 
        "snow", "hot", "cold", "warm", "cool", "climate", "conditions"
    ]
    
    # Check if message contains weather keywords
    has_weather_keyword = any(keyword in message_content for keyword in weather_keywords)
    
    # Check if message contains a potential city name (capitalized word)
    has_city = bool(extract_city_from_message(last_message.content))
    
    # Route to weather node if both weather keyword and city are present, or if strong weather intent
    if (has_weather_keyword and has_city) or any(phrase in message_content for phrase in [
        "weather in", "weather for", "temperature in", "how's the weather", "what's the weather"
    ]):
        return "weather"
    
    # Default to chatbot for general conversation
    return "chatbot"


# Build the StateGraph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("chatbot", chatbot_node)
graph_builder.add_node("weather", weather_node)

# Add edges - use conditional edges from START with router function
graph_builder.add_conditional_edges(START, router)
graph_builder.add_edge("chatbot", END)
graph_builder.add_edge("weather", END)

# Compile the graph
graph = graph_builder.compile()

# Export the compiled graph as required by evaluation script
compiled_graph = graph
