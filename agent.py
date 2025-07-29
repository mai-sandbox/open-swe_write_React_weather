from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model
import random


# Define the State schema with messages field and add_messages reducer
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Custom weather tool that simulates weather lookup for any city
@tool
def get_weather(city: str) -> str:
    """Get current weather information for a city.
    
    Args:
        city: The name of the city to get weather for
    """
    # Simulate weather data for any city
    weather_conditions = [
        "sunny", "cloudy", "partly cloudy", "rainy", "snowy", "foggy", "windy"
    ]
    temperatures = list(range(-10, 35))  # Temperature range in Celsius
    
    condition = random.choice(weather_conditions)
    temp = random.choice(temperatures)
    humidity = random.randint(30, 90)
    
    return f"Current weather in {city}: {condition.title()}, {temp}°C, humidity {humidity}%. Have a great day!"


# Initialize the LLM - using Anthropic as preferred model
try:
    llm = init_chat_model("anthropic:claude-3-5-sonnet-20241022")
except Exception as e:
    try:
        llm = init_chat_model("openai:gpt-4o")
    except Exception:
        try:
            llm = init_chat_model("google_genai:gemini-1.5-pro")
        except Exception:
            # Fallback to a basic model if others fail
            llm = init_chat_model("anthropic:claude-3-haiku-20240307")


# Create tools list and bind to LLM
tools = [get_weather]
llm_with_tools = llm.bind_tools(tools)


# Chatbot node that uses LLM with bound tools
def chatbot(state: State):
    """Main chatbot node that processes messages and can call tools."""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Create the StateGraph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("chatbot", chatbot)

# Create tool node using ToolNode for executing weather tool
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

# Add edges
graph_builder.add_edge(START, "chatbot")

# Use conditional edges with tools_condition to route between chatbot and tools
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

# Any time a tool is called, return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")

# Compile the graph and export as 'app' for evaluator compatibility
app = graph_builder.compile()
