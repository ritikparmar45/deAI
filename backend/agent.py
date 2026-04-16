from .executor import PlaywrightExecutor
from .planner import TaskPlanner
import asyncio
import os

class SupportAgent:
    def __init__(self, base_url="http://localhost:8000", headless=True):
        self.executor = PlaywrightExecutor(headless=headless)
        self.planner = TaskPlanner()
        self.base_url = base_url
        self.history = []

    async def run(self, task):
        print(f"Starting task: {task}")
        try:
            await self.executor.start()
            
            # Initial navigation
            await self.executor.navigate(f"{self.base_url}/login")
            
            max_steps = 15
            step = 0
            
            while step < max_steps:
                step += 1
                print(f"\n--- STEP {step} ---")
                state = await self.executor.get_state()
                if "error" in state:
                    print(f"Browser/State Error: {state['error']}")
                    return {"status": "failed", "error": state['error']}
                
                # Plan next step with retry logic for 429
                plan = None
                for attempt in range(4):
                    try:
                        plan = await self.planner.plan_next_step(task, state, self.history)
                        break
                    except Exception as e:
                        if "429" in str(e) or "ResourceExhausted" in str(e):
                            wait_time = 35 + (attempt * 10)
                            print(f"Rate limit hit, waiting {wait_time}s... (Attempt {attempt+1}/4)")
                            await asyncio.sleep(wait_time)
                        else:
                            raise e

                if not plan or "action" not in plan:
                    print(f"Error: Planner returned invalid plan: {plan}")
                    return {"status": "failed", "error": "Invalid plan from AI"}
                
                print(f"Reasoning: {plan.get('reasoning')}")
                action = plan.get('action')
                print(f"Action: {action.get('type')} -> {action}")
                
                # Guard against infinite loops of the same action
                if len(self.history) > 2 and action == self.history[-1] == self.history[-2]:
                    print("Error: Detected action loop. AI is stuck.")
                    return {"status": "failed", "error": "Action loop detected"}
                
                self.history.append(action)
                
                action_type = action.get('type')
                
                if action_type == "navigate":
                    url = action['url']
                    if url.startswith("/"):
                        url = f"{self.base_url}{url}"
                    await self.executor.navigate(url)
                
                elif action_type == "click":
                    await self.executor.click(action['text'])
                
                elif action_type == "type":
                    await self.executor.type(action['field'], action['value'])
                
                elif action_type == "wait":
                    await asyncio.sleep(action.get('seconds', 2))
                
                elif action_type == "done":
                    print(f"Goal achieved: {action.get('message', 'Success')}")
                    return {"status": "completed", "message": action.get('message')}
                
                elif action_type == "error":
                    print(f"Model Error: {action.get('message')}")
                    return {"status": "failed", "error": action.get('message')}
                
                else:
                    print(f"Unknown action type: {action_type}")
                    break
                    
        except Exception as e:
            print(f"Agent Execution Exception: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "failed", "error": str(e)}
        finally:
            print("Cleaning up agent resources...")
            await asyncio.sleep(1) 
            await self.executor.stop()
            
        return {"status": "timeout", "error": "Maximum steps reached"}

async def main():
    agent = SupportAgent()
    # Example test run
    # result = await agent.run("Create a new user test@test.com")
    # print(result)

if __name__ == "__main__":
    asyncio.run(main())
