from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Define the State class
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize the StateGraph
graph_builder = StateGraph(State)

# Placeholder for normal conversation node
def normal_conversation_node(state: State):
    # This will be implemented in the next task
    pass

# Placeholder for weather-related query node
def weather_query_node(state: State):
    # This will be implemented in the next task
    pass

# Add entry and exit points
graph_builder.add_edge(START, "normal_conversation")
graph_builder.add_edge("normal_conversation", "weather_query")
graph_builder.add_edge("weather_query", END)

# Compile the graph
graph = graph_builder.compile()

# Export the compiled graph
compiled_graph = graph

