# COMP3480 Lab 4 - Docker Containerization

This project demonstrates containerization of a FastAPI service using Docker. The main goal is to learn how to containerize applications and deploy them using Docker, while also understanding container networking and remote access.

## Learning Goals

- Learn Docker containerization concepts and best practices
- Practice building and running Docker containers
- Deploy and access containerized applications

## Features

- **Dockerized FastAPI Service**: Complete containerization of the API service
- **Port Mapping**: Exposed container port for external access
- **Dependency Management**: Isolated Python environment in container

## How To Use

### Prerequisites
- Docker installed on your system

### Building the Container

1. **Build the Docker image:**
```bash
cd "Lab 4"
docker build -t lab4-cloudcomputing .
```

2. **Run the container:**
```bash
docker run -p 8080:8080 lab4-cloudcomputing
```

### Accessing the API

The API will be available at:
- http://localhost:8080

### API Documentation
Interactive documentation is available at:
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
| GET    | `/protected-data`   | Protected data access      | Header: `api-key: mysecretkey`  |
| GET    | `/cookie-greet`     | Personal cookie greeting   | Cookie: `username=JohnDoe`      |

## Docker Configuration

### Dockerfile Structure
```dockerfile
# Use the official Python 3.11.5 image
FROM python:3.11.5-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### Dependencies
The container uses the following Python packages:
- FastAPI
- Uvicorn
- Pydantic
- Typing

## Technologies Used

- **Docker** – Container platform
- **FastAPI** – API framework
- **Python** – Programming language
- **Uvicorn** – ASGI server
- **Pydantic** – Data validation 