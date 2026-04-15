# AI-Powered IT Support Agent

A complete project for an AI agent that performs administrative tasks on a web-based admin panel using human-like browser automation.

## 🚀 Features

- **Mock Admin Panel**: A full FastAPI application with login, dashboard, and user management.
- **AI Agent**: A Python agent powered by OpenAI and Playwright that reasons step-by-step.
- **Human-Like Interation**: The agent clicks buttons, fills forms, and navigates pages just like a user.
- **Natural Language Tasks**: Trigger tasks like "Reset password for john@company.com" or "Create a new user Alice".

## 📁 Project Structure

```text
/backend
  main.py       # FastAPI application & API endpoints
  agent.py      # AI Agent orchestrator
  planner.py    # LLM-based reasoning & planning
  executor.py   # Playwright-based browser control
/templates      # HTML templates for the mock panel
requirements.txt
.env            # Environment variables (OpenAI API Key)
README.md
```

## 🛠️ Setup Instructions

### 1. Install Dependencies
Make sure you have Python 3.9+ installed.
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Environment
Create a `.env` file in the root directory and add your OpenAI API Key:
```env
OPENAI_API_KEY=your_openai_api_key_here
BASE_URL=http://localhost:8000
```

### 3. Run the Backend
Start the FastAPI server:
```bash
python -m backend.main
```
The server will run at `http://localhost:8000`.

## 🤖 Demo Steps

### 1. Manual Access
You can visit the admin panel manually at [http://localhost:8000/login](http://localhost:8000/login).
Credentials: `admin@company.com` / `admin`.

### 2. Trigger the AI Agent
Use a tool like Postman, cURL, or the interactive docs at `/docs` to send a POST request:

**Endpoint**: `POST /run-task`
**Body**:
```json
{
  "task": "Create a user named Alice with email alice@company.com and then reset her password."
}
```

### 🌟 Example Prompts to Test
- "Create a new user john@company.com"
- "Reset password for john@company.com"
- "Check if John Doe exists, if not create him and then reset his password."

## ⚠️ Notes
- The agent runs Playwright in **headed mode** by default (configured in `agent.py`) so you can watch it perform the actions.
- The user database is **in-memory**, so it will reset every time you restart the server.
