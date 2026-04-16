# 🤖 DeAI: AI-Powered IT Support Agent

A cutting-edge IT support agent that automates administrative tasks using **Groq (Llama 3.3)** and **Playwright**. It navigates a mock admin panel just like a human, clicking buttons and filling forms to execute complex requests.

---

## 🚀 Key Features

*   **🧠 Intelligent Reasoning**: Powered by **Llama 3.3-70B** (via Groq) for high-speed, accurate task planning.
*   **🖱️ Human-Like Interaction**: Uses Playwright to interact with a real web UI (headless or headed).
*   **📂 All-in-One Automation**: A single script handles backend startup, agent execution, and cleanup.
*   **🛠️ Mock Admin Panel**: Built with FastAPI, featuring user management, dashboards, and secure login.

---

## 📁 Project Structure

```text
├── backend/
│   ├── main.py        # FastAPI Backend (Mock Admin Panel)
│   ├── agent.py       # Orchestrates the LLM and Browser
│   ├── planner.py     # Llama 3.3 Reasoning Logic
│   └── executor.py    # Playwright Browser Controls
├── automate.py        # 🌟 ALL-IN-ONE execution script
├── templates/         # UI for the Mock Admin Panel
├── requirements.txt   # Python Dependencies
└── .env               # API Keys (Groq)
```

---

## 🛠️ Setup Instructions

### 1. Install Dependencies
Ensure you have Python 3.9+ installed, then run:
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Environment
Create a `.env` file in the root directory and add your Groq API Key:
```env
GROQ_API_KEY=your_groq_api_key_here
BASE_URL=http://localhost:8000
```

---

## ⚡ Quick Start (The Easy Way)

Use the `automate.py` script to run the backend and the agent simultaneously with a single command. The script will automatically clean up the backend process when finished.

```bash
python automate.py "Create a user named Alice with email alice@company.com"
```

**What happens next?**
1.  The **Backend** starts automatically.
2.  The **AI Agent** wakes up and receives your task.
3.  A **Browser window opens**, and you watch the agent log in and perform the task.
4.  The script provides a summary and shuts everything down.

---

## 🧪 Manual Testing & Docs

If you prefer to run things separately:

### 1. Run Backend Only
```bash
python -m backend.main
```
*   **Admin Panel**: [http://localhost:8000/login](http://localhost:8000/login)
*   **Interactive API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
*   **Credentials**: `admin@company.com` / `admin`

### 2. Trigger via API
Send a POST request to `/run-task` with a JSON body:
```json
{
  "task": "Reset password for john@company.com"
}
```

---

## 🌟 Example Prompts to Try
*   *"Create a new user john@company.com and set his name to John Doe"*
*   *"Check if Alice exists on the users page, if so, reset her password."*
*   *"Log in and tell me how many users are in the system."*

---

## ⚠️ Notes
*   **Headed Mode**: By default, the browser is visible (`headless=False`) so you can witness the automation.
*   **In-Memory DB**: The user database resets every time the backend restarts.
*   **Model**: Optimized for `llama-3.3-70b-versatile` for the best reasoning performance.
