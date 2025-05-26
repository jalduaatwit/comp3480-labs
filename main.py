from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# 1. Root route
@app.get("/")
async def root():
    return {"message": "Welcome to Lab 1 FastAPI Service!"}