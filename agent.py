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
    # Detect weather-related queries and extract city information
    user_message = state['messages'][-1]['content']
    user_message_lower = user_message.lower()
    
    # Check for weather-related keywords
    weather_keywords = ['weather', 'temperature', 'forecast', 'rain', 'sunny', 'cloudy', 'storm']
    has_weather_keyword = any(keyword in user_message_lower for keyword in weather_keywords)
    
    if has_weather_keyword:
        # Common city names and patterns to detect cities
        # This is a simplified approach - in production, you'd use NER or a comprehensive city database
        common_cities = [
            'new york', 'london', 'paris', 'tokyo', 'berlin', 'madrid', 'rome', 'moscow',
            'beijing', 'sydney', 'toronto', 'vancouver', 'montreal', 'chicago', 'boston',
            'los angeles', 'san francisco', 'seattle', 'miami', 'denver', 'atlanta',
            'houston', 'dallas', 'phoenix', 'philadelphia', 'detroit', 'minneapolis',
            'amsterdam', 'barcelona', 'vienna', 'prague', 'budapest', 'warsaw',
            'stockholm', 'oslo', 'copenhagen', 'helsinki', 'dublin', 'lisbon',
            'mumbai', 'delhi', 'bangalore', 'chennai', 'kolkata', 'hyderabad',
            'singapore', 'hong kong', 'seoul', 'bangkok', 'jakarta', 'manila'
        ]
        
        # Look for city mentions in the user message
        detected_city = None
        for city in common_cities:
            if city in user_message_lower:
                detected_city = city.title()
                break
        
        # Also check for patterns like "in [City]" or "weather in [City]"
        import re
        city_pattern = r'\bin\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        match = re.search(city_pattern, user_message)
        if match and not detected_city:
            detected_city = match.group(1)
        
        if detected_city:
            # Weather query detected with city - this will be handled by weather tool in next task
            return {'messages': [{'role': 'assistant', 'content': f'I can help you check the weather in {detected_city}. Let me get that information for you.'}]}
        else:
            # Weather query without specific city
            return {'messages': [{'role': 'assistant', 'content': 'I can help you check the weather! Please specify which city you\'d like to know about.'}]}
    
    # If no weather keywords detected, pass through unchanged
    return state

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




