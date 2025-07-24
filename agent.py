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
    # Handle normal conversation for non-weather related queries
    user_message = state['messages'][-1]['content']
    user_message_lower = user_message.lower()
    
    # Check if this is NOT a weather-related query
    weather_keywords = ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cloudy', 'storm']
    is_weather_query = any(keyword in user_message_lower for keyword in weather_keywords)
    
    if not is_weather_query:
        # Provide friendly conversational responses
        if any(greeting in user_message_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            response = "Hello! I'm a friendly chatbot. I can chat with you about various topics or help you check the weather in any city. What would you like to talk about?"
        elif any(question in user_message_lower for question in ['how are you', 'how do you do']):
            response = "I'm doing great, thank you for asking! I'm here and ready to help. How can I assist you today?"
        elif 'thank' in user_message_lower:
            response = "You're very welcome! Is there anything else I can help you with?"
        else:
            response = "That's interesting! I'm here to chat and help with various topics. I can also check the weather for any city if you'd like. What else would you like to know?"
            
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



