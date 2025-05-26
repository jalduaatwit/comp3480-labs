from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# 1. Root route
@app.get("/")
async def root():
    return {"message": "Welcome to Lab 1 FastAPI Service!"}

# 2. Query string: /greet?name=Aniket
@app.get("/greet")
async def greet(name: str = "Guest"):
    return {"greeting": f"Hello, {name}!"}