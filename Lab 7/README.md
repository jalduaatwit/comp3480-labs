# COMP3480 Lab 7 - Integrated FastAPI and Database CLI

This project demonstrates a unified Python application that combines FastAPI service testing with MySQL database operations through a comprehensive command-line interface. The main goal is to create an integrated CLI driver that can test both API endpoints and execute database queries, along with comprehensive unit tests for all functionality.

## Learning Goals

- Learn to integrate FastAPI service testing with MySQL database operations in a single Python application
- Practice implementing SQL queries in Python with proper error handling and connection management
- Build a unified interactive command-line interface for both API and database testing
- Develop comprehensive unit tests for both FastAPI endpoints and database functionality
- Understand containerized deployment with both FastAPI and MySQL services
- Master database query execution with formatted output display and API response testing

## Features

- **Unified CLI Interface**: Single command-line application for both FastAPI service testing and database operations
- **FastAPI Service Testing**: Interactive testing of all 12 API endpoints with real-time request/response display
- **Database Query Execution**: 13 predefined SQL queries plus custom query support with formatted table output
- **Integrated Architecture**: Seamless integration between API testing and database operations
- **Comprehensive Unit Tests**: Automated testing for both FastAPI endpoints and database functionality
- **Containerized Services**: Both FastAPI and MySQL services running in Docker containers
- **Error Handling**: Robust connection management for both API and database operations
- **Server Status Monitoring**: Real-time checking of FastAPI service availability

## How To Use

### Prerequisites
- Python 3.8 or newer
- Docker and Docker Compose installed
- `pip` package manager

### Installation

1. **Install Python dependencies:**
```bash
cd "Lab 7"
pip install -r requirements.txt
```

2. **Start up the containers:**
```bash
docker-compose up -d
```

### Using the Integrated CLI Driver

The CLI driver provides a unified interface for both FastAPI service testing and database operations:

```bash
python cli_driver.py
```

#### Main Menu Options:

**FastAPI Service Testing (Options 1-12):**
- Test individual API endpoints with interactive parameter input
- Real-time request/response display with detailed logging
- Support for all HTTP methods (GET, POST) with headers and cookies
- Server status monitoring and connection validation

**Database Operations (Option 13):**
- Execute 13 predefined SQL queries organized by category
- Run custom SQL queries with immediate execution
- View formatted table results with row counts
- Automatic database connection management

**Additional Features:**
- Run all tests automatically (API + Database)
- Check server status and connectivity
- Integrated error handling and recovery

### Running the Tests

#### Unit Tests
```bash
python test.py
```

The test suite covers:
- **FastAPI Endpoints**: All 12 API routes with various scenarios including authentication and error conditions
- **Database Operations**: All 13 predefined queries with result validation and connection testing
- **Integrated Testing**: Combined API and database functionality testing
- **Connection Management**: Both API and database connectivity with error handling

## Database Schema

The `my_guitar_shop` database contains the following tables:

| Table | Description | Key Fields |
|-------|-------------|------------|
| **categories** | Product categories | category_id, category_name |
| **products** | Product information | product_id, category_id, product_name, list_price |
| **customers** | Customer accounts | customer_id, email_address, first_name, last_name |
| **addresses** | Customer addresses | address_id, customer_id, city, state |
| **orders** | Order details | order_id, customer_id, order_date, ship_amount |
| **order_items** | Order line items | item_id, order_id, product_id, quantity |
| **administrators** | Admin accounts | admin_id, email_address |

## Query Categories

### Simple Single Table Queries (3 queries)

| Query Key | Description | SQL Concept |
|-----------|-------------|-------------|
| **simple_1** | List all product names and prices | Basic SELECT |
| **simple_2** | List all customers with the last name Brown | WHERE clause filtering |
| **simple_3** | Products with a discount over 25% | WHERE clause with comparison |

### Inner Join Queries (5 queries)

| Query Key | Description | SQL Concept |
|-----------|-------------|-------------|
| **join_1** | Products with their category names | Basic INNER JOIN |
| **join_2** | Orders with customer information | Multi-table join |
| **join_3** | Order items with product details | Complex joins |
| **join_4** | Shipping address for each order | Join with address data |
| **join_5** | Customer's addresses | Customer-address relationship |

### Group By and Function Queries (5 queries)

| Query Key | Description | SQL Concept |
|-----------|-------------|-------------|
| **group_1** | Count customers per state | COUNT with GROUP BY |
| **group_2** | Average discount by category | AVG with GROUP BY |
| **group_3** | Total number of orders per customer | COUNT with GROUP BY |
| **group_4** | Most expensive product per category | MAX with GROUP BY |
| **group_5** | Total order value per order | SUM with calculations |

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

## Example Usage

### Integrated CLI Driver Example

**Starting the CLI driver:**
```bash
python cli_driver.py
# Enter server URL (or press Enter for default)
# Server status check and validation
```

**Main Menu Options:**
```
AVAILABLE ROUTE SERVICES:
============================================================
1.  Root Endpoint                (/)
2.  Greet Service                (/greet)
3.  Cube Calculator              (/cube/{number})
4.  Addition Service             (/add)
5.  Factorial Calculator         (/factorial/{n})
6.  Person Info                  (/person)
7.  City Information             (/city/{city_name})
8.  Rectangle Area Calculator    (/area/rectangle)
9.  Power Calculator             (/power/{base})
10. Colors List                  (/colors)
11. Protected Data               (/protected-data)
12. Cookie Personal Greeting     (/cookie-greet)
============================================================
13. Database Operations
14. Run All Tests (Auto)
15. Check Server Status
0.  Exit
============================================================
```

### FastAPI Service Testing Example

**Test API endpoint with interactive input:**
```bash
# Select option 2 (Greet Service)
# Enter name: Aniket
```

**Output:**
```
REQUEST: GET http://localhost:8080/greet
Query Parameters: {'name': 'Aniket'}
Status Code: 200
Response: {
  "greeting": "Hello, Aniket!"
}
```

### Database Operations Example

**Execute a predefined query:**
```bash
# Select option 13 (Database Operations)
# Choose from categorized queries:
# - Simple Queries (1-3)
# - Join Queries (4-8) 
# - Group By Queries (9-13)
# - Custom SQL Query (14)
```

**Query Output:**
```
+----------------+------------+
| product_name   | list_price |
+----------------+------------+
| Gibson Les Paul| 2517.00    |
| Fender Strat   | 699.00     |
| Yamaha FG800   | 179.99     |
+----------------+------------+
Total rows: 3
```

### Automated Testing Example

**Run all tests:**
```bash
# Select option 14 (Run All Tests)
# Executes both API and database tests automatically
```

## Docker Configuration

### Docker Compose Structure
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:9.3
    container_name: mysql-db-lab7
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: secret_password
    ports:
      - "3307:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  fastapi:
    image: fastapi:latest
    container_name: fastapi-server
    restart: always
    ports:
      - "8080:8080"

volumes:
  mysql_data:
```

### Key Configuration Details
- **MySQL Version**: 9.3 (latest stable)
- **Port Mapping**: Host port 3307 → Container port 3306
- **Root Password**: `secret_password`
- **Data Persistence**: `mysql_data` volume for database files
- **FastAPI Server**: Containerized API service

## Python Database Integration

### Database Utilities (`database_utils.py`)

**Key Functions:**
- `connect_to_db()`: Establish MySQL connection with automatic database creation
- `execute_query_with_headers()`: Execute queries and return structured results
- `format_query_results_as_table()`: Format results as readable tables
- `execute_query_with_table_format()`: Combined query execution and formatting

**Connection Management:**
- Automatic reconnection on connection loss
- Proper connection cleanup
- Error handling for database operations

### CLI Driver Features (`cli_driver.py`)

**Unified Interface:**
- Single application for both API and database testing
- Server status monitoring and validation
- Integrated error handling and recovery

**FastAPI Service Testing:**
- Interactive endpoint testing with parameter input
- Real-time request/response display with detailed logging
- Support for all HTTP methods (GET, POST) with headers and cookies
- Authentication testing (API keys, cookies)

**Database Operations:**
- Predefined query execution with categorized menu
- Custom SQL query input with immediate execution
- Formatted table result display with row counts
- Automatic database connection management
- Connection recovery and error handling

**Additional Features:**
- Automated test execution (API + Database)
- Server connectivity checking
- Graceful exit with connection cleanup

## Unit Testing

### Test Coverage (`test.py`)

**FastAPI Tests:**
- All 12 API endpoints
- Various input scenarios
- Error condition testing
- Authentication testing

**Database Tests:**
- All 13 predefined queries
- Result validation
- Connection testing
- Error handling verification

### Running Tests
```bash
# Run all tests
python test.py

# Run specific test class
python -m unittest test.FastAPILab1Test
python -m unittest test.DatabaseLab7Test
```

## Key Differences from Lab 6

- **Unified Application**: Single CLI application vs separate DBeaver and API testing tools
- **Implementation Language**: Python integration vs SQL-only execution
- **Query Execution**: Programmatic execution with formatted output vs manual DBeaver execution
- **Service Integration**: Combined FastAPI and database testing vs isolated database operations
- **User Interface**: Interactive CLI with categorized menus vs separate database management tool
- **Testing**: Automated unit tests for both API and database vs manual verification
- **Error Handling**: Integrated error handling for both services vs separate error management
- **Server Monitoring**: Real-time service status checking vs manual service verification

## Troubleshooting

### Common Issues:
- **"Server not responding"**: Ensure FastAPI server is running with `docker-compose ps`
- **"Database connection failed"**: Ensure MySQL container is running with `docker-compose ps`
- **"Module not found"**: Install dependencies with `pip install -r requirements.txt`
- **"Port already in use"**: Check if services are running on ports 8080 and 3307
- **"Query execution failed"**: Verify database schema with `docker-compose logs mysql`
- **"CLI driver errors"**: Ensure both FastAPI and MySQL services are running before using CLI

### Container Management:
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs

# Stop services
docker-compose down

# Reset database
docker-compose down -v
docker-compose up -d
```

## Technologies Used

- **Python 3.8+** – Programming language for database integration
- **mysql-connector-python** – MySQL database connector for Python
- **FastAPI** – API framework for web service endpoints
- **Docker Compose** – Multi-container application orchestration
- **MySQL 9.3** – Relational database management system
- **unittest** – Automated testing framework
- **requests** – HTTP client for API testing 