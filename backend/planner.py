import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv(override=True)

class TaskPlanner:
    def __init__(self):
        # Explicitly reload dotenv in ctor to be safe
        load_dotenv(override=True)
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            print("WARNING: GROQ_API_KEY not found in environment. Please add it to your .env file.")
            
        self.client = Groq(api_key=self.api_key)
        # Using Llama 3.3 70B for high-quality reasoning
        self.model = "llama-3.3-70b-versatile"

    async def plan_next_step(self, task, current_state, history):
        """
        Asks Groq to decide the next action based on the task and current page state.
        """
        system_prompt = """
        You are an AI IT Support Agent that controls a web browser.
        Your goal is to complete the task by performing one action at a time.
        
        ALLOWED ACTIONS:
        1. navigate(url): Go to a specific URL.
        2. click(text): Click a button, link, or element with the specified text.
        3. type(field, value): Type text into a field (placeholder or name).
        4. wait(seconds): Wait for a bit.
        5. done(message): Use this when the task is successfully completed.
        6. error(message): Use this if you are stuck or encountered a problem.

        CONTEXT:
        - Admin Login: /login (admin@company.com / admin)
        - Dashboard: /dashboard
        - Users Page: /users
        
        RULES:
        - You must reason step-by-step.
        - Look at the 'elements' and 'text' of the current page to decide what to do.
        - If you see a login page, you must login first.
        - If you need to find a user, go to the Users page.
        - Format your output as a JSON object with 'reasoning' (string) and 'action' (object).
        
        Example Output:
        {
            "reasoning": "I am on the login page. I need to enter the admin credentials.",
            "action": {"type": "type", "field": "email", "value": "admin@company.com"}
        }
        """

        user_prompt = f"""
        TASK: {task}
        CURRENT URL: {current_state.get('url', 'Unknown')}
        PAGE TEXT: {current_state.get('text', '')[:1500]}... (truncated)
        INTERACTIVE ELEMENTS: {json.dumps(current_state.get('elements', [])[:25])}
        ACTION HISTORY: {history}
        
        What is the next step?
        """

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )

            content = completion.choices[0].message.content
            if not content:
                raise ValueError("Empty response from Groq")

            return json.loads(content)
        except Exception as e:
            print(f"Error in Groq planning: {e}")
            # If the user hasn't added the key yet, this will fail gracefully
            if "API key" in str(e) or "401" in str(e):
                return {
                    "reasoning": "GROQ_API_KEY is missing or invalid.",
                    "action": {"type": "error", "message": "Please add your GROQ_API_KEY to the .env file."}
                }
            raise e
