from typing import Annotated
from typing_extensions import TypedDict
import random

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


# Define the weather tool
@tool
def get_weather(city: str) -> str:
    """Get current weather information for a city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        A string containing weather information including temperature, conditions, and humidity
    """
    # Mock weather data - in a real implementation this would call a weather API
    temperatures = [15, 18, 22, 25, 28, 30, 32, 35]
    conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Heavy Rain", "Thunderstorms", "Snow", "Foggy"]
    humidity_levels = [30, 40, 50, 60, 70, 80, 90]
    
    # Generate random but realistic weather data
    temp = random.choice(temperatures)
    condition = random.choice(conditions)
    humidity = random.choice(humidity_levels)
    
    return f"Current weather in {city}: {temp}°C, {condition}, Humidity: {humidity}%"


# Define the state schema - using the required format for evaluator compatibility
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Initialize the LLM with tools
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
tools = [get_weather]
llm_with_tools = llm.bind_tools(tools)


# Define the chatbot node
def chatbot(state: State):
    """Main chatbot node that processes messages and decides whether to use tools."""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Create the graph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

# Add edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")

# Compile the graph and export as 'app' for evaluator compatibility
app = graph_builder.compile()

