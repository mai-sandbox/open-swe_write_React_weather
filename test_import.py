#!/usr/bin/env python3

try:
    import agent
    print("Import successful")
    print(f"App object exists: {hasattr(agent, 'app')}")
    if hasattr(agent, 'app'):
        print(f"App type: {type(agent.app)}")
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
