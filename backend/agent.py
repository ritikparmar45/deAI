from .executor import PlaywrightExecutor
from .planner import TaskPlanner
import asyncio
import os

class SupportAgent:
    def __init__(self, base_url="http://localhost:8000"):
        self.executor = PlaywrightExecutor(headless=False) # Headless=False to see it in action
        self.planner = TaskPlanner()
        self.base_url = base_url
        self.history = []

    async def run(self, task):
        print(f"Starting task: {task}")
        await self.executor.start()
        
        # Initial navigation
        await self.executor.navigate(f"{self.base_url}/login")
        
        max_steps = 15
        step = 0
        
        try:
            while step < max_steps:
                step += 1
                state = await self.executor.get_state()
                plan = await self.planner.plan_next_step(task, state, self.history)
                
                print(f"Step {step}: {plan['reasoning']}")
                action = plan['action']
                self.history.append(action)
                
                action_type = action.get('type')
                
                if action_type == "navigate":
                    # Make sure URL is absolute if it's relative
                    url = action['url']
                    if url.startswith("/"):
                        url = f"{self.base_url}{url}"
                    await self.executor.navigate(url)
                
                elif action_type == "click":
                    await self.executor.click(action['text'])
                
                elif action_type == "type":
                    await self.executor.type(action['field'], action['value'])
                    # If it's a login or form, sometimes we need to press enter or click submit
                    # The planner might decide to click 'Login' or 'Create User' next
                
                elif action_type == "wait":
                    await asyncio.sleep(action.get('seconds', 2))
                
                elif action_type == "done":
                    print(f"Goal achieved: {action.get('message', 'Success')}")
                    return {"status": "completed", "message": action.get('message')}
                
                elif action_type == "error":
                    print(f"Error: {action.get('message')}")
                    return {"status": "failed", "error": action.get('message')}
                
                else:
                    print(f"Unknown action type: {action_type}")
                    break
                    
        finally:
            await asyncio.sleep(2) # Give a moment to see the result
            await self.executor.stop()
            
        return {"status": "timeout", "error": "Maximum steps reached"}

async def main():
    agent = SupportAgent()
    # Example test run
    # result = await agent.run("Create a new user test@test.com")
    # print(result)

if __name__ == "__main__":
    asyncio.run(main())
