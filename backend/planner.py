import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()

class TaskPlanner:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.client = openai.OpenAI(api_key=self.api_key)

    async def plan_next_step(self, task, current_state, history):
        """
        Asks the LLM to decide the next action based on the task and current page state.
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
        - Format your output as a JSON object with 'reasoning' and 'action'.
        
        Example Output:
        {
            "reasoning": "I am on the login page. I need to enter the admin credentials.",
            "action": {"type": "type", "field": "email", "value": "admin@company.com"}
        }
        """

        user_prompt = f"""
        TASK: {task}
        CURRENT URL: {current_state['url']}
        PAGE TEXT: {current_state['text'][:1000]}... (truncated)
        INTERACTIVE ELEMENTS: {json.dumps(current_state['elements'][:20])}
        ACTION HISTORY: {history}
        
        What is the next step?
        """

        response = self.client.chat.completions.create(
            model="gpt-4o", # Using gpt-4o for better performance
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)
