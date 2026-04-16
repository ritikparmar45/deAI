import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

models_to_try = [
    'gemini-1.5-flash',
    'gemini-2.0-flash-exp',
    'gemini-1.5-flash-8b',
    'gemini-1.5-pro',
    'gemini-flash-latest',
    'gemini-2.0-flash-001'
]

print("Testing models for a successful response...")
for model_name in models_to_try:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hi")
        print(f"SUCCESS: {model_name} is working!")
        # Stop at the first working model
        with open("working_model.txt", "w") as f:
            f.write(model_name)
        break
    except Exception as e:
        print(f"FAILED: {model_name} - {str(e)[:100]}")
