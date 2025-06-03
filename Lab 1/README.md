# COMP3480 Lab 1 - Introduction

This project is a beginner friendly FastAPI service created as a programming lab assignment. The main goal is to learn how to build an API service using Python and the FastAPI framework. 

## Project Purpose

- Learn to design and implement API endpoints
- Practice using query strings, path parameters, and POST requests with FastAPI
- Understand documentation in APIs (/docs)
- Demonstrate the ability to handle different types of HTTP requests (GET, POST)

## Features

- **10 API routes**: Showcasing path, query, and POST usage
- **Simple mathematical operations**: Routes to add, cube, and compute factorials
- **User data handling**: Accepts and processes JSON inputs through POST

## How To Use

### Prerequisites
- Python 3.8 or newer
- `pip` package manager

### Installation

1. **Install FastAPI and Uvicorn:**
```bash
pip install fastapi uvicorn
```

2. **Install requests for testing:**
```bash
pip install requests
```

### Running the API Server
```bash
cd "Lab 1"
uvicorn main:app --port 8080 --reload
```

### API Documentation
Interactive documentation is automatically available at:
- http://localhost:8080/docs (Swagger UI)
- http://localhost:8080/redoc (ReDoc)

## API Endpoints

| Method | Endpoint            | Description                | Example Input                   |
| ------ | ------------------- | -------------------------- | ------------------------------- |
| GET    | `/`                 | Welcome message            | N/A                             |
| GET    | `/greet`            | Greet by name (query)      | `/greet?name=Aniket`            |
| GET    | `/cube/{number}`    | Cube a number (path)       | `/cube/3`                       |
| GET    | `/add`              | Add two numbers (query)    | `/add?a=5&b=7`                  |
| GET    | `/factorial/{n}`    | Calculate factorial (path) | `/factorial/5`                  |
| POST   | `/person`           | Person info (JSON)         | `{"name": "Alex", "age": 17}`   |
| GET    | `/city/{city_name}` | Get info on a city (path)  | `/city/Boston`                  |
| POST   | `/area/rectangle`   | Rectangle area (JSON)      | `{"width": 4.0, "height": 5.0}` |
| GET    | `/power/{base}`     | Exponentiation with query  | `/power/2?exp=8`                |
| GET    | `/colors`           | List of colors             | N/A                             |

## Running the Tests
1. Ensure the server is running
2. Run the test file:
```bash
cd "Lab 1"
python test.py
```
Test Output:
- Each test’s printout is clearly labeled with a unique identifier, so results remain easy to read and debug, even if test execution order changes

## Technologies Used

- **FastAPI** – API framework
- **Uvicorn** – ASGI server for local development
- **Pydantic** – Data validation and parsing
- **unittest** – Automated testing
- **requests** – HTTP client for test scripts