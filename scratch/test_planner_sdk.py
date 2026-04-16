import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = "You are a helpful assistant. Return JSON."
user_prompt = "Say hello in JSON."

print("Testing generate_content with gemini-1.5-flash...")
try:
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
        )
    )
    print(f"Success: {response.text}")
except Exception as e:
    print(f"Failed: {e}")

print("\nTesting with models/gemini-1.5-flash...")
try:
    response = client.models.generate_content(
        model='models/gemini-1.5-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
        )
    )
    print(f"Success: {response.text}")
except Exception as e:
    print(f"Failed: {e}")
