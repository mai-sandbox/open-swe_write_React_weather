#!/usr/bin/env python3
"""Test script to verify the weather chatbot structure without requiring API keys."""

import sys
import traceback
from langchain_core.messages import HumanMessage

def test_agent_structure():
    """Test the agent implementation structure and components."""
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
        
        # Verify the State class exists and has correct structure
        if not hasattr(agent, 'State'):
            print("❌ ERROR: 'State' class not found in agent module")
            return False
        
        print("✅ State class found")
        
        # Verify the weather tool exists
        if not hasattr(agent, 'get_weather'):
            print("❌ ERROR: 'get_weather' tool function not found")
            return False
        
        print("✅ Weather tool function found")
        
        # Test the weather tool directly (without LLM)
        try:
            weather_result = agent.get_weather("New York")
            if isinstance(weather_result, str) and len(weather_result) > 0:
                print("✅ Weather tool works correctly")
                print(f"   Sample output: {weather_result[:80]}...")
            else:
                print("❌ ERROR: Weather tool returned invalid result")
                return False
        except Exception as e:
            print(f"❌ ERROR: Weather tool failed: {str(e)}")
            return False
        
        # Test weather tool with different cities
        test_cities = ["London", "Tokyo", "Unknown City"]
        for city in test_cities:
            try:
                result = agent.get_weather(city)
                if isinstance(result, str) and len(result) > 0:
                    print(f"✅ Weather tool works for {city}")
                else:
                    print(f"❌ ERROR: Weather tool failed for {city}")
                    return False
            except Exception as e:
                print(f"❌ ERROR: Weather tool failed for {city}: {str(e)}")
                return False
        
        # Verify graph structure
        try:
            graph_dict = app.get_graph()
            nodes = list(graph_dict.nodes.keys())
            print(f"✅ Graph nodes found: {nodes}")
            
            # Check for required nodes
            required_nodes = ["chatbot", "tools"]
            for node in required_nodes:
                if node not in nodes:
                    print(f"❌ ERROR: Required node '{node}' not found in graph")
                    return False
                else:
                    print(f"✅ Required node '{node}' found")
            
            # Check edges
            edges = list(graph_dict.edges)
            print(f"✅ Graph edges found: {len(edges)} edges")
            
        except Exception as e:
            print(f"❌ ERROR: Failed to analyze graph structure: {str(e)}")
            return False
        
        # Verify the tools list exists
        if not hasattr(agent, 'tools'):
            print("❌ ERROR: 'tools' list not found")
            return False
        
        if not isinstance(agent.tools, list) or len(agent.tools) == 0:
            print("❌ ERROR: 'tools' is not a valid list or is empty")
            return False
        
        print("✅ Tools list found and populated")
        
        # Verify LLM with tools exists
        if not hasattr(agent, 'llm_with_tools'):
            print("❌ ERROR: 'llm_with_tools' not found")
            return False
        
        print("✅ LLM with bound tools found")
        
        # Verify tool node exists
        if not hasattr(agent, 'tool_node'):
            print("❌ ERROR: 'tool_node' not found")
            return False
        
        print("✅ Tool node found")
        
        print("\n🎉 All structural tests passed!")
        print("\nNote: Full functionality testing requires API keys, but the structure is correct.")
        print("The agent should work properly when API keys are provided in the evaluation environment.")
        
        return True
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_agent_structure()
    sys.exit(0 if success else 1)
