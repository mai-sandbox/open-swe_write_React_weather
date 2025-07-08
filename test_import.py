# Test imports to find the correct add_messages import
try:
    from langgraph.graph.message import add_messages
    print("✓ add_messages from langgraph.graph.message works")
except ImportError as e:
    print(f"✗ langgraph.graph.message import failed: {e}")

try:
    from langchain_core.messages.utils import add_messages
    print("✓ add_messages from langchain_core.messages.utils works")
except ImportError as e:
    print(f"✗ langchain_core.messages.utils import failed: {e}")

