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

# 3. Path param: /cube/3
@app.get("/cube/{number}")
async def cube(number: int):
    return {"number": number, "cube": number ** 3}