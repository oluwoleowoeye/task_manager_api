from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Data models
class User(BaseModel):
    username: str
    email: str

class Task(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    user_id: int

# User endpoints
@app.post("/users/")
def create_user(user: User):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (%s, %s)",
            (user.username, user.email)
        )
        connection.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            return user
        else:
            return {"error": "User not found"}
    finally:
        cursor.close()
        connection.close()

# Task endpoints
@app.post("/tasks/")
def create_task(task: Task):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO tasks (title, description, status, user_id) VALUES (%s, %s, %s, %s)",
            (task.title, task.description, task.status, task.user_id)
        )
        connection.commit()
        return {"message": "Task created successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        task = cursor.fetchone()
        if task:
            return task
        else:
            return {"error": "Task not found"}
    finally:
        cursor.close()
        connection.close()

@app.get("/")
def home():
    return {"message": "Welcome to the Task Manager API"}