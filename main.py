from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from datetime import datetime
from typing import List
from models import TaskCreate, TaskUpdate, Task
from database import get_tasks_collection

app = FastAPI(
    title="TODO API",
    description="A simple TODO app with FastAPI and MongoDB",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks_collection = get_tasks_collection()


@app.get("/api", tags=["Root"])
async def root():
    """Root endpoint - API is running"""
    return {
        "message": "TODO API is running!",
        "version": "1.0.0",
        "endpoints": {
            "create_task": "POST /api/tasks",
            "get_all_tasks": "GET /api/tasks",
            "get_task_by_id": "GET /api/tasks/{task_id}",
            "update_task": "PUT /api/tasks/{task_id}",
            "delete_task": "DELETE /api/tasks/{task_id}"
        }
    }


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(task: TaskCreate):
    """Create a new task"""
    task_data = {
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "start_date": task.start_date,
        "end_date": task.end_date,
        "priority": task.priority,
        "progress_status": task.progress_status
    }
    
    result = tasks_collection.insert_one(task_data)
    
    created_task = tasks_collection.find_one({"_id": result.inserted_id})
    
    return {
        "id": str(created_task["_id"]),
        "title": created_task["title"],
        "description": created_task["description"],
        "completed": created_task["completed"],
        "created_at": created_task["created_at"],
        "updated_at": created_task["updated_at"],
        "start_date": created_task.get("start_date"),
        "end_date": created_task.get("end_date"),
        "priority": created_task.get("priority"),
        "progress_status": created_task.get("progress_status")
    }


@app.get("/tasks", response_model=List[Task], tags=["Tasks"])
async def get_all_tasks():
    """Get all tasks"""
    tasks = list(tasks_collection.find())
    
    if not tasks:
        return []
    
    return [
        {
            "id": str(task["_id"]),
            "title": task["title"],
            "description": task["description"],
            "completed": task["completed"],
            "created_at": task["created_at"],
            "updated_at": task["updated_at"],
            "start_date": task.get("start_date"),
            "end_date": task.get("end_date"),
            "priority": task.get("priority"),
            "progress_status": task.get("progress_status")
        }
        for task in tasks
    ]


@app.get("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def get_task_by_id(task_id: str):
    """Get a specific task by ID"""
    try:
        task_object_id = ObjectId(task_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )
    
    task = tasks_collection.find_one({"_id": task_object_id})
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task["description"],
        "completed": task["completed"],
        "created_at": task["created_at"],
        "updated_at": task["updated_at"],
        "start_date": task.get("start_date"),
        "end_date": task.get("end_date"),
        "priority": task.get("priority"),
        "progress_status": task.get("progress_status")
    }


@app.put("/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def update_task(task_id: str, task_update: TaskUpdate):
    """Update a task"""
    try:
        task_object_id = ObjectId(task_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )
    
    task = tasks_collection.find_one({"_id": task_object_id})
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Prepare update data
    update_data = {}
    if task_update.title is not None:
        update_data["title"] = task_update.title
    if task_update.description is not None:
        update_data["description"] = task_update.description
    if task_update.completed is not None:
        update_data["completed"] = task_update.completed
    if task_update.start_date is not None:
        update_data["start_date"] = task_update.start_date
    if task_update.end_date is not None:
        update_data["end_date"] = task_update.end_date
    if task_update.priority is not None:
        update_data["priority"] = task_update.priority
    if task_update.progress_status is not None:
        update_data["progress_status"] = task_update.progress_status
    
    update_data["updated_at"] = datetime.utcnow()
    
    tasks_collection.update_one(
        {"_id": task_object_id},
        {"$set": update_data}
    )
    
    updated_task = tasks_collection.find_one({"_id": task_object_id})
    
    return {
        "id": str(updated_task["_id"]),
        "title": updated_task["title"],
        "description": updated_task["description"],
        "completed": updated_task["completed"],
        "created_at": updated_task["created_at"],
        "updated_at": updated_task["updated_at"],
        "start_date": updated_task.get("start_date"),
        "end_date": updated_task.get("end_date"),
        "priority": updated_task.get("priority"),
        "progress_status": updated_task.get("progress_status")
    }


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_task(task_id: str):
    """Delete a task"""
    try:
        task_object_id = ObjectId(task_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )
    
    result = tasks_collection.delete_one({"_id": task_object_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return None
