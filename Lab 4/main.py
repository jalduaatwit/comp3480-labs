from fastapi import FastAPI, Header, HTTPException, Cookie
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

API_KEY = "mysecretkey"

# 1. Root route
@app.get("/")
async def root():
    return {"message": "Welcome to Lab 4 FastAPI Service!"}

# 2. Query string: /greet?name=Aniket
@app.get("/greet")
async def greet(name: str = "Guest"):
    return {"greeting": f"Hello, {name}!"}

# 3. Path param: /cube/3
@app.get("/cube/{number}")
async def cube(number: int):
    return {"number": number, "cube": number ** 3}

# 4. Query string math: /add?a=5&b=7
@app.get("/add")
async def add(a: int, b: int):
    return {"sum": a + b}

# 5. Path param calculation: /factorial/5
@app.get("/factorial/{n}")
async def factorial(n: int):
    result = 1
    for i in range(2, n+1):
        result *= i
    return {"n": n, "factorial": result}

# 6. POST with Pydantic: /person
class Person(BaseModel):
    name: str
    age: int

@app.post("/person")
async def person_info(person: Person):
    status = "minor" if person.age < 18 else "adult"
    return {
        "message": f"{person.name} is {person.age} years old and is an {status}."
    }

# 7. Path route with string: /city/Boston
@app.get("/city/{city_name}")
async def city_info(city_name: str):
    facts = {
        "boston": "Boston is a city that experiences all four seasons.",
        "newyork": "New York is a very busy place with lots of tall buildings.",
        "seattle": "Seattle gets a fair amount of rain each year.",
        "miami": "Miami is known for being warm and having many beaches.",
        "dallas": "Dallas is located in Texas and is pretty big."
    }
    info = facts.get(city_name.lower(), "No info for this city.")
    return {"city": city_name, "info": info}

# 8. POST: Calculate area
class Rectangle(BaseModel):
    width: float
    height: float

@app.post("/area/rectangle")
async def rectangle_area(rect: Rectangle):
    return {"width": rect.width, "height": rect.height, "area": rect.width * rect.height}

# 9. Path and Query: /power/2?exp=8
@app.get("/power/{base}")
async def power(base: int, exp: int = 2):
    return {"base": base, "exp": exp, "result": base ** exp}

# 10. GET list: /colors
@app.get("/colors")
async def list_colors():
    return {"colors": ["red", "blue", "green", "yellow"]}

# 11. Header: /protected-data
@app.get("/protected-data")
async def protected_data(api_key: Optional[str] = Header(None)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")
    return {"data": "This is protected data."}

# 12. Cookie: /cookie-greet
@app.get("/cookie-greet")
async def personal_greet(username: Optional[str] = Cookie(None)):
    if username:
        return {"greeting": f"Welcome back, {username}!"}
    else:
        return {"greeting": "Hello, new visitor!"}
