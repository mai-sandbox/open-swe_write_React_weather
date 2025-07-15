"""Simple weather chatbot implementation using LangGraph."""

from typing import Annotated
import requests
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


class State(TypedDict):
    """State definition for the chatbot with message history."""
    messages: Annotated[list, add_messages]


@tool
def get_weather(city: str) -> str:
    """Get current weather information for a given city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        Weather information as a string
    """
    try:
        # Using a simple mock weather API for demonstration
        # In production, you would use a real weather API like OpenWeatherMap
        mock_weather_data = {
            "new york": "Sunny, 72°F (22°C), light breeze",
            "london": "Cloudy, 59°F (15°C), moderate rain expected",
            "tokyo": "Partly cloudy, 68°F (20°C), humid conditions",
            "paris": "Overcast, 61°F (16°C), light winds",
            "sydney": "Clear skies, 75°F (24°C), perfect beach weather"
        }
        
        city_lower = city.lower().strip()
        if city_lower in mock_weather_data:
            return f"Weather in {city}: {mock_weather_data[city_lower]}"
        else:
            return f"Weather in {city}: Sunny, 70°F (21°C), pleasant conditions (mock data)"
            
    except Exception as e:
        return f"Sorry, I couldn't get weather information for {city} right now."


# Initialize the language model
llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

# Create tools list and bind to LLM
tools = [get_weather]
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State) -> dict:
    """Main chatbot node that processes messages and decides on tool usage."""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Build the state graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))

# Add edges for routing
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

# Compile the graph
graph = graph_builder.compile()

# Export the compiled graph for evaluation
compiled_graph = graph

