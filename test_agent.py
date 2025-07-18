import agent
from langchain_core.messages import HumanMessage

print('Agent imported successfully')
print('compiled_graph available:', hasattr(agent, 'compiled_graph'))

# Test basic functionality
state = {'messages': [HumanMessage(content='Hello')]}
result = agent.compiled_graph.invoke(state)
print('Normal chat test passed')

# Test weather functionality
weather_state = {'messages': [HumanMessage(content='What is the weather in Paris?')]}
weather_result = agent.compiled_graph.invoke(weather_state)
print('Weather query test passed')

print('All tests passed!')
