from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import uuid
import os
from typing import List, Optional

app = FastAPI(title="Mock IT Admin Panel")

# Templates setup
templates = Jinja2Templates(directory="templates")

# Mock User Data Store
class User(BaseModel):
    id: str
    name: str
    email: str
    password: str = "password123"

users_db: List[User] = [
    User(id=str(uuid.uuid4()), name="Ritik Admin", email="admin@company.com"),
    User(id=str(uuid.uuid4()), name="John Doe", email="john@company.com"),
]

# Admin Panel Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    # Dummy auth
    if email == "admin@company.com" and password == "admin":
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user_count": len(users_db)})

@app.get("/users", response_class=HTMLResponse)
async def users_list(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users_db})

@app.post("/create-user")
async def create_user(request: Request, name: str = Form(...), email: str = Form(...)):
    new_user = User(id=str(uuid.uuid4()), name=name, email=email)
    users_db.append(new_user)
    return RedirectResponse(url="/users", status_code=303)

@app.post("/reset-password/{user_id}")
async def reset_password(user_id: str):
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # In a real app, we'd update the DB. Here we just log it.
    print(f"PASSWORD RESET TRIGGERED FOR: {user.email}")
    return {"status": "success", "message": f"Password reset for {user.email}"}

from .agent import SupportAgent

# Task Runner Endpoint
class TaskRequest(BaseModel):
    task: str

@app.post("/run-task")
async def run_task(task_req: TaskRequest):
    # Initialize agent with current base URL
    agent = SupportAgent(base_url="http://localhost:8000")
    
    # Run the task
    result = await agent.run(task_req.task)
    
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
