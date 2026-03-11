from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import datetime
#intialize the FastApi Application with a title
app = FastAPI(title="To-Do List API")
#in-memory database(data will reset when the server restarts)
tasks = {} # dictionary to store task {id; task_data}
task_counter = 0 # auto-incrementing ID
creation_log = [] # stores the date each task was created
#schame for creating a new task
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    completed: bool = False
    #schema for updating existing task option to allow partial updates
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# verify if the API is online
@app.get("/")
def root():
    return {"message": "To-Do List API is running!"}

# retrieve all tasks currently stored in memory
@app.get("/tasks")
def get_all_tasks():
    return {"tasks": list(tasks.values()), "total": len(tasks)}

# retrieve a specific task by its ID; returns 404 if not found
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

# Create a new task, increment the ID, and timestamp the entry
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global task_counter
    task_counter += 1
    now = datetime.datetime.now().isoformat()
    
    new_task = {
        "id": task_counter,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": now,
    }
    
    tasks[task_counter] = new_task
    creation_log.append(now[:10])  # Log the date for the bar chart
    return new_task

# Update existing task fields based on the provided ID
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    stored = tasks[task_id]
    # Update only the fields provided in the request
    if task.title is not None:
        stored["title"] = task.title
    if task.description is not None:
        stored["description"] = task.description
    if task.completed is not None:
        stored["completed"] = task.completed
    return stored

# Remove a task from the dictionary
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    deleted = tasks.pop(task_id)
    return {"message": f"Task '{deleted['title']}' deleted"}

#summary statistics for the Streamlit dashboard 
@app.get("/stats")
def get_stats():
    total = len(tasks)
    completed = sum(1 for t in tasks.values() if t["completed"])
    pending = total - completed
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "creation_log": creation_log,
    }
#to run the server directly via 'python main.py'
if __name__ == "__main__":
    import uvicorn
    # reload=True enables hot-reloading when code changes are saved
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

