from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chat_models import init_chat_model

# State schema with messages field using add_messages reducer
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Custom weather tool function using @tool decorator
@tool
def get_weather(location: str) -> str:
    """Get the current weather for a given location/city.
    
    Args:
        location: The city or location to get weather for
        
    Returns:
        A string describing the current weather conditions
    """
    # Mock weather data for demonstration
    weather_data = {
        "new york": "Currently 72°F and sunny in New York with light winds from the west.",
        "london": "Currently 15°C and cloudy in London with occasional light rain.",
        "tokyo": "Currently 25°C and partly cloudy in Tokyo with high humidity.",
        "paris": "Currently 18°C and overcast in Paris with gentle breeze.",
        "sydney": "Currently 22°C and clear skies in Sydney with ocean breeze.",
        "san francisco": "Currently 16°C and foggy in San Francisco with cool ocean air.",
        "miami": "Currently 28°C and sunny in Miami with high humidity and light winds.",
        "chicago": "Currently 8°C and windy in Chicago with partly cloudy skies."
    }
    
    location_lower = location.lower().strip()
    
    # Check for exact matches first
    if location_lower in weather_data:
        return weather_data[location_lower]
    
    # Check for partial matches
    for city, weather in weather_data.items():
        if location_lower in city or city in location_lower:
            return weather
    
    # Default response for unknown locations
    return f"Currently 20°C and partly cloudy in {location} with light winds. (Note: This is mock weather data for demonstration purposes.)"

# Initialize chat model (prefer Anthropic as per guidelines)
try:
    llm = init_chat_model("anthropic:claude-3-5-sonnet-20241022")
except Exception:
    try:
        llm = init_chat_model("openai:gpt-4o")
    except Exception:
        try:
            llm = init_chat_model("google_genai:gemini-1.5-pro")
        except Exception:
            # Fallback to a basic model if others fail
            llm = init_chat_model("openai:gpt-3.5-turbo")

# Bind the weather tool to the LLM
tools = [get_weather]
llm_with_tools = llm.bind_tools(tools)

# Chatbot node that uses LLM with bound tools
def chatbot(state: State):
    """Main chatbot node that processes user messages and decides whether to use tools."""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Create ToolNode for executing weather tool calls
tool_node = ToolNode(tools)

# Build the StateGraph
graph_builder = StateGraph(State)

# Add nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

# Add edges
graph_builder.add_edge(START, "chatbot")

# Add conditional routing logic using tools_condition
# This routes to "tools" if the last AI message contains tool calls, otherwise to END
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

# After tools are executed, return to chatbot to formulate final response
graph_builder.add_edge("tools", "chatbot")

# Compile and export the graph as 'app' variable for the evaluator
app = graph_builder.compile()
