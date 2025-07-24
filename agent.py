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
    # Respond to general user inputs
    user_message = state['messages'][-1]['content'].lower()
    if 'weather' not in user_message:
        response = "I'm here to chat! How can I assist you today?"
        return {'messages': [{'role': 'assistant', 'content': response}]}
    return state

# Placeholder for weather-related query node
def weather_query_node(state: State):
    # This will be implemented in the next task
    pass

# Add entry and exit points
graph_builder.add_node("normal_conversation", normal_conversation_node)
graph_builder.add_node("weather_query", weather_query_node)

graph_builder.add_edge(START, "normal_conversation")
graph_builder.add_edge("normal_conversation", "weather_query")
graph_builder.add_edge("weather_query", END)

# Compile the graph
graph = graph_builder.compile()

# Export the compiled graph
compiled_graph = graph


