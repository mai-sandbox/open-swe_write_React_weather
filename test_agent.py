#!/usr/bin/env python3

# Simple test script to verify the agent works
from agent import app
from langchain_core.messages import HumanMessage

def test_basic_chat():
    """Test basic chat functionality"""
    try:
        result = app.invoke({"messages": [HumanMessage(content="Hello, how are you?")]})
        print("✓ Basic chat test passed")
        return True
    except Exception as e:
        print(f"✗ Basic chat test failed: {e}")
        return False

def test_weather_query():
    """Test weather functionality"""
    try:
        result = app.invoke({"messages": [HumanMessage(content="What's the weather like in New York?")]})
        print("✓ Weather query test passed")
        return True
    except Exception as e:
        print(f"✗ Weather query test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing agent...")
    test_basic_chat()
    test_weather_query()
    print("Agent tests completed")
