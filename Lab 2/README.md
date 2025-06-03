# COMP3480 Lab 2 - Advanced FastAPI Service

This is an advanced FastAPI service created as a programming lab assignment. The main goal is to learn advanced API features including headers, cookies, and build an interactive CLI testing tool.

## Learning Goals

- Learn advanced FastAPI features like headers and cookies
- Practice API authentication using custom headers
- Understand session management through cookies
- Build interactive CLI tools for testing APIs
- Handle different types of HTTP requests with advanced features

## Features

- **12 API routes**: Path, query, POST, header authentication, and cookie usage
- **Authentication**: Protected endpoints requiring API key headers
- **Session management**: Cookie-based personalized greetings
- **Interactive CLI Driver**: Command-line interface for testing all endpoints
- **Advanced mathematical operations**: Enhanced with power calculations
- **User data handling**: JSON inputs and validation

## How To Use

### Prerequisites
- Python 3.8 or newer
- `pip` package manager

### Installation

1. **Install FastAPI and Uvicorn:**
```bash
pip install fastapi uvicorn
```

2. **Install requests for CLI and testing:**
```bash
pip install requests
```

### Running the API Server
```bash
cd "Lab 2"
uvicorn main:app --port 8080 --reload
```

### Using the Interactive CLI Driver
```bash
cd "Lab 2"
python cli_driver.py
```

### API Documentation
Interactive documentation is automatically available at:
- http://localhost:8080/docs (Swagger UI)
- http://localhost:8080/redoc (ReDoc)

## API Endpoints

| Method | Endpoint            | Description                    | Authentication | Example Input                   |
| ------ | ------------------- | ------------------------------ | -------------- | ------------------------------- |
| GET    | `/`                 | Welcome message                | None           | N/A                             |
| GET    | `/greet`            | Greet by name (query)          | None           | `/greet?name=Aniket`            |
| GET    | `/cube/{number}`    | Cube a number (path)           | None           | `/cube/3`                       |
| GET    | `/add`              | Add two numbers (query)        | None           | `/add?a=5&b=7`                  |
| GET    | `/factorial/{n}`    | Calculate factorial (path)     | None           | `/factorial/5`                  |
| POST   | `/person`           | Person info (JSON)             | None           | `{"name": "Alex", "age": 17}`   |
| GET    | `/city/{city_name}` | Get info on a city (path)      | None           | `/city/Boston`                  |
| POST   | `/area/rectangle`   | Rectangle area (JSON)          | None           | `{"width": 4.0, "height": 5.0}` |
| GET    | `/power/{base}`     | Power calculation with query   | None           | `/power/2?exp=8`                |
| GET    | `/colors`           | List of colors                 | None           | N/A                             |
| GET    | `/protected-data`   | Protected data access          | **API Key**    | Header: `api-key: mysecretkey`  |
| GET    | `/cookie-greet`     | Personal cookie greeting       | **Cookie**     | Cookie: `username=JohnDoe`      |

## Running the Tests

### Unit Tests
1. Make sure the server is running
2. Run the test file:
```bash
python test.py
```

### CLI Testing
1. Start the CLI driver:
```bash
python cli_driver.py
```
2. Follow the interactive menu to test individual endpoints or run all tests automatically

## Technologies Used

- **FastAPI** – API framework with automatic documentation
- **Uvicorn** – ASGI server for local development
- **Pydantic** – Data validation and parsing
- **unittest** – Automated testing
- **requests** – HTTP client for CLI and test scripts 