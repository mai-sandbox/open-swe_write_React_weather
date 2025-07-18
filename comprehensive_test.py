import agent
from langchain_core.messages import HumanMessage

print('=== Comprehensive Agent Testing ===')

# Test 1: Normal greeting
print('\nTest 1: Normal greeting')
state = {'messages': [HumanMessage(content='Hello')]}
result = agent.compiled_graph.invoke(state)
print(f'Response: {result["messages"][-1].content}')

# Test 2: Weather query with city
print('\nTest 2: Weather query with city')
state = {'messages': [HumanMessage(content='What is the weather in Paris?')]}
result = agent.compiled_graph.invoke(state)
print(f'Response: {result["messages"][-1].content}')

# Test 3: General question
print('\nTest 3: General question')
state = {'messages': [HumanMessage(content='How are you doing today?')]}
result = agent.compiled_graph.invoke(state)
print(f'Response: {result["messages"][-1].content}')

# Test 4: Weather query different format
print('\nTest 4: Weather query different format')
state = {'messages': [HumanMessage(content='Tell me about London weather')]}
result = agent.compiled_graph.invoke(state)
print(f'Response: {result["messages"][-1].content}')

# Test 5: Weather query without city
print('\nTest 5: Weather query without city')
state = {'messages': [HumanMessage(content='What is the weather like?')]}
result = agent.compiled_graph.invoke(state)
print(f'Response: {result["messages"][-1].content}')

print('\n=== All tests completed successfully! ===')
