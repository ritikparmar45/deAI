import asyncio
import os
import sys

# Add the root directory to sys.path so we can import from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.agent import SupportAgent

async def test():
    print("Testing SupportAgent...")
    agent = SupportAgent(base_url="http://localhost:8000")
    try:
        # We need the backend to be running for this to work fully, 
        # but let's see if it even starts Playwright or fails at the planner.
        result = await agent.run("Test task")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Caught exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
