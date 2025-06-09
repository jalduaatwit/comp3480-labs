# COMP3480 Lab 3 - Express.js Service

This is an Express.js web service created as a programming lab assignment. The main goal is to transition from FastAPI (Python) to Express.js (Node.js) while implementing similar API functionality with enhanced features.

## Learning Goals

- Learn Express.js framework and Node.js ecosystem
- Practice building REST APIs with JavaScript/Node.js
- Understand middleware usage and request handling in Express
- Implement header authentication and query parameter validation
- Handle different content types (HTML and JSON responses)
- Compare and contrast Express.js with FastAPI implementation patterns

## Features

- **11 API routes**: Path parameters, query strings, POST requests, and header authentication
- **Mixed response formats**: 7 HTML routes and 4 JSON routes
- **Query parameter support**: 5 routes with comprehensive query handling
- **Authentication**: Protected endpoint requiring API key headers
- **Mathematical operations**: Add, cube, factorial, and power calculations
- **User data handling**: JSON inputs through POST requests
- **City information**: Dynamic city facts with optional detailed view

## How To Use

### Prerequisites
- Node.js 14+ or newer
- npm package manager

### Installation

1. **Initialize and install Express:**
```bash
cd "Lab 3"
npm init -y
npm install express
```

### Running the Express Server
```bash
cd "Lab 3"
node main.js
```

The server will start on http://localhost:8080

### Testing the API
You can test the endpoints using:
- **Browser**: For GET requests returning HTML
- **curl**: For command-line testing
- **Postman**: For comprehensive API testing
- **Thunder Client** (VS Code extension): For integrated testing

## API Endpoints

| Method | Endpoint                    | Response | Authentication | Description                    | Example Input                   |
| ------ | --------------------------- | -------- | -------------- | ------------------------------ | ------------------------------- |
| GET    | `/`                         | HTML     | None           | Welcome message                | N/A                             |
| GET    | `/greet?name=Aniket`        | HTML     | None           | Greet by name (query)          | `/greet?name=Aniket`            |
| GET    | `/cube/{number}`            | HTML     | None           | Cube a number (path)           | `/cube/3`                       |
| GET    | `/add?a=5&b=7`              | JSON     | None           | Add two numbers (query)        | `/add?a=5&b=7`                  |
| GET    | `/factorial/{n}?format=html`| HTML/JSON| None           | Calculate factorial            | `/factorial/5?format=html`      |
| POST   | `/person`                   | JSON     | None           | Person info (JSON body)        | `{"name": "Alex", "age": 17}`   |
| GET    | `/city/{name}?details=true` | HTML     | None           | City info with optional details| `/city/Boston?details=true`     |
| POST   | `/area/rectangle`           | JSON     | None           | Rectangle area (JSON body)     | `{"width": 4.0, "height": 5.0}` |
| GET    | `/power/{base}?exp=8`       | HTML     | None           | Power calculation with query   | `/power/2?exp=8`                |
| GET    | `/colors`                   | JSON     | None           | List of colors                 | N/A                             |
| GET    | `/protected-data`           | JSON     | **API Key**    | Protected data access          | Header: `api-key: mysecretkey`  |

## Assignment Requirements Met

✅ **Minimum 5 HTML Routes**: 7 routes return HTML content  
✅ **Minimum 5 Query Parameters**: 5 routes accept query parameters  
✅ **Minimum 1 Header Parameter**: `/protected-data` requires API key header  
✅ **Minimum 1 Body Input**: `/person` and `/area/rectangle` accept JSON bodies  

## Example Usage

### Testing with curl

**HTML Response:**
```bash
curl "http://localhost:8080/greet?name=Alice"
# Returns: <h2>Hello, Alice!</h2>
```

**JSON Response:**
```bash
curl "http://localhost:8080/add?a=10&b=20"
# Returns: {"sum": 30}
```

**POST Request:**
```bash
curl -X POST http://localhost:8080/person \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "age": 25}'
# Returns: {"message": "John is 25 years old and is an adult."}
```

**Header Authentication:**
```bash
curl -H "api-key: mysecretkey" http://localhost:8080/protected-data
# Returns: {"data": "This is protected data."}
```

## Key Differences from FastAPI (Lab 2)

- **Framework**: Express.js (Node.js) vs FastAPI (Python)
- **Response Types**: Mixed HTML/JSON responses vs pure JSON
- **Middleware**: Express middleware vs FastAPI dependency injection
- **Documentation**: Manual documentation vs automatic OpenAPI/Swagger
- **Type Safety**: JavaScript vs Python with Pydantic validation

## Technologies Used

- **Express.js** – Web application framework for Node.js
- **Node.js** – JavaScript runtime environment
- **JavaScript ES6+** – Modern JavaScript features
- **JSON** – Data interchange format
- **HTML** – Markup for web responses 