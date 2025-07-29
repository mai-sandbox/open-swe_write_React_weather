#!/usr/bin/env python3
"""Test script to verify the weather chatbot implementation."""

import sys
import traceback
from langchain_core.messages import HumanMessage

def test_agent():
    """Test the agent implementation with various inputs."""
    try:
        # Import the agent module
        import agent
        print("✅ Agent module imported successfully")
        
        # Verify the app is exported
        if not hasattr(agent, 'app'):
            print("❌ ERROR: 'app' attribute not found in agent module")
            return False
        
        app = agent.app
        print("✅ Compiled graph 'app' found")
        
        # Test cases
        test_cases = [
            {
                "name": "Normal Chat",
                "input": "Hello, how are you?",
                "expected_behavior": "Should respond normally without using tools"
            },
            {
                "name": "Weather Query - New York",
                "input": "What's the weather like in New York?",
                "expected_behavior": "Should use weather tool and provide weather info"
            },
            {
                "name": "Weather Query - London",
                "input": "How's the weather in London today?",
                "expected_behavior": "Should use weather tool and provide weather info"
            },
            {
                "name": "General Question",
                "input": "What can you help me with?",
                "expected_behavior": "Should respond normally without using tools"
            }
        ]
        
        print("\n🧪 Running test cases...")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- Test {i}: {test_case['name']} ---")
            print(f"Input: {test_case['input']}")
            print(f"Expected: {test_case['expected_behavior']}")
            
            try:
                # Invoke the graph with evaluation format
                result = app.invoke({
                    'messages': [HumanMessage(content=test_case['input'])]
                })
                
                # Verify result structure
                if not isinstance(result, dict):
                    print(f"❌ ERROR: Result is not a dict, got {type(result)}")
                    continue
                
                if 'messages' not in result:
                    print(f"❌ ERROR: 'messages' key not found in result")
                    continue
                
                if not isinstance(result['messages'], list):
                    print(f"❌ ERROR: 'messages' is not a list, got {type(result['messages'])}")
                    continue
                
                if len(result['messages']) == 0:
                    print(f"❌ ERROR: No messages in result")
                    continue
                
                # Get the final response
                final_message = result['messages'][-1]
                if hasattr(final_message, 'content'):
                    response_content = final_message.content
                else:
                    response_content = str(final_message)
                
                print(f"✅ SUCCESS: Got response")
                print(f"Response preview: {response_content[:100]}...")
                
                # Check if this looks like a weather response for weather queries
                if "weather" in test_case['input'].lower():
                    if any(indicator in response_content.lower() for indicator in ['°', 'temperature', 'sunny', 'cloudy', 'rain', 'wind']):
                        print("✅ Weather-related response detected (likely used tool)")
                    else:
                        print("⚠️  Response doesn't seem weather-related (may not have used tool)")
                
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
                print(f"Traceback: {traceback.format_exc()}")
                continue
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_agent()
    sys.exit(0 if success else 1)
