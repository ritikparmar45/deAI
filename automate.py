import subprocess
import time
import sys
import os
import requests
import signal
import asyncio
from backend.agent import SupportAgent
from dotenv import load_dotenv

load_dotenv(override=True)

def start_backend():
    """Starts the FastAPI backend in a separate process."""
    print(">> Starting Mock IT Admin Panel (Backend)...")
    # Using 'sys.executable -m backend.main' to ensure we use the same python interpreter
    process = subprocess.Popen(
        [sys.executable, "-m", "backend.main"],
        # On windows, we need to handle termination carefully
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )
    return process

def wait_for_server(url="http://127.0.0.1:8000/login", timeout=30):
    """Waits for the server to be ready."""
    print("... Waiting for server to be ready (Timeout: 30s)...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                print("[OK] Server is UP!")
                return True
        except requests.exceptions.ConnectionError:
            # Expected during startup
            pass
        except Exception as e:
            print(f"  (Wait Debug: {e})")
        time.sleep(1)
        if int(time.time() - start_time) % 5 == 0:
            print(f"  ...still waiting ({int(time.time() - start_time)}s)")
    return False

async def run_automate(task_text):
    backend_process = None
    try:
        # 1. Start backend
        backend_process = start_backend()
        
        # 2. Wait for it
        if not wait_for_server():
            print("[ERROR] Server failed to start in time.")
            return

        # 3. Initialize Agent
        print(f"[AGENT] Taking over for task: '{task_text}'")
        # We run it with headless=False so you can see it working "apne aap"
        agent = SupportAgent(base_url="http://127.0.0.1:8000", headless=False)
        
        # 4. Run the task
        result = await agent.run(task_text)
        
        print("\n" + "="*30)
        print(f"TASK RESULT: {result.get('status')}")
        if "message" in result:
            print(f"MESSAGE: {result.get('message')}")
        if "error" in result:
            print(f"ERROR: {result.get('error')}")
        print("="*30)

    except Exception as e:
        print(f"[ERROR] Unexpected Error: {e}")
    finally:
        if backend_process:
            print("[SHUTDOWN] Shutting down backend...")
            if os.name == 'nt':
                # On Windows, taskkill is more reliable for process groups
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(backend_process.pid)], capture_output=True)
            else:
                os.killpg(os.getpgid(backend_process.pid), signal.SIGTERM)
            print("[DONE] All cleaned up!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python automate.py \"Your task description here\"")
        sys.exit(1)
    
    task = sys.argv[1]
    asyncio.run(run_automate(task))
