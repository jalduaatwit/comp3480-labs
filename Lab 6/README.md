# COMP3480 Lab 6 - Containerized MySQL Database

This project demonstrates containerized SQL database operations using Docker Compose and MySQL. The main goal is to learn how to deploy and manage a MySQL database in a containerized environment while executing various SQL queries using DBeaver as the database management tool.

## Learning Goals

- Practice containerized database deployment and management
- Execute SQL queries in a containerized MySQL environment

## Features

- **Containerized MySQL Database**: Complete MySQL deployment using Docker Compose
- **Persistent Data Storage**: Docker volumes for data persistence across container restarts
- **13 SQL Queries**: Comprehensive query set covering different SQL concepts
- **Simple Queries**: 3 basic single-table queries for data retrieval
- **Inner Join Queries**: 5 queries demonstrating table relationships
- **Aggregation Queries**: 5 queries using GROUP BY and functions
- **DBeaver Integration**: Complete setup and execution instructions for containerized database

## How To Use

### Prerequisites
- Docker and Docker Compose installed on your system
- DBeaver Community Edition (free database tool)
- Basic knowledge of SQL syntax and Docker concepts

### Database Setup with Docker Compose

1. **Start the MySQL container:**
```bash
cd "Lab 6"
docker-compose up
```

### Connecting DBeaver to Containerized MySQL

1. **Open DBeaver** and create a new MySQL connection
2. **Configure connection settings:**
   - **Host**: `localhost`
   - **Port**: `3307` (mapped from container's 3306)
   - **Database**: Leave empty initially
   - **Username**: `root`
   - **Password**: `secret_password`
3. **Test the connection** to ensure it works

### Database Initialization

1. **Open the `createguitar.sql` file** in DBeaver:
   - Go to File → Open File
   - Navigate to the Lab 6 folder and select `createguitar.sql`
2. **Execute the script**:
   - Click the "Execute SQL Script" button (▶️) or press Ctrl+Alt+X
   - This will create the database, tables, and insert sample data

### Running Queries

#### Method 1: Using SQL Editor
1. **Open a new SQL Editor**:
   - Click the "SQL Editor" button or press Ctrl+]
2. **Select your datasource**:
   - Press **Ctrl+9** to open the datasource selection dialog
   - Choose your MySQL connection (localhost:3307)
3. **Select the database**:
   - Press **Ctrl+0** to open the database selection dialog
   - Choose `my_guitar_shop` database
4. **Open a query file**:
   - Go to File → Open File
   - Select any `.sql` file from the Lab 6 folder
5. **Execute the query**:
   - Click the "Execute SQL Statement" button (▶️) or press Ctrl+Enter
6. **View results** in the data tab below the editor

#### Method 2: Direct File Execution
1. **Right-click on any `.sql` file** in DBeaver's file explorer
2. **Select "Open With" → "SQL Editor"**
3. **Select datasource and database**:
   - Press **Ctrl+9** to select your MySQL datasource
   - Press **Ctrl+0** to select the `my_guitar_shop` database
4. **Execute the query** using Ctrl+Enter

#### Method 3: Copy and Paste
1. **Open a new SQL Editor**
2. **Select datasource and database**:
   - Press **Ctrl+9** to select your MySQL datasource
   - Press **Ctrl+0** to select the `my_guitar_shop` database
3. **Copy the contents** of any query file
4. **Paste into the editor**
5. **Execute the query**

## Docker Configuration

### Docker Compose Structure
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:9.3
    container_name: mysql-db
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: secret_password
    ports:
      - "3307:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### Key Configuration Details
- **MySQL Version**: 9.3 (latest stable)
- **Port Mapping**: Host port 3307 → Container port 3306
- **Root Password**: `secret_password`
- **Data Persistence**: `mysql_data` volume for database files
- **Restart Policy**: `unless-stopped` for automatic recovery

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

| Query File | Description | SQL Concept |
|------------|-------------|-------------|
| **SimpleQuery1.sql** | List all product names and prices | Basic SELECT |
| **SimpleQuery2.sql** | List all customers with the last name Brown | WHERE clause filtering |
| **SimpleQuery3.sql** | Products with a discount over 25% | WHERE clause with comparison |

### Inner Join Queries (5 queries)

| Query File | Description | SQL Concept |
|------------|-------------|-------------|
| **InnerJoinQuery1.sql** | Products with their category names | Basic INNER JOIN |
| **InnerJoinQuery2.sql** | Orders with customer information | Multi-table join |
| **InnerJoinQuery3.sql** | Order items with product details | Complex joins |
| **InnerJoinQuery4.sql** | Shipping address for each order | Join with address data |
| **InnerJoinQuery5.sql** | Customer's addresses | Customer-address relationship |

### Group By and Function Queries (5 queries)

| Query File | Description | SQL Concept |
|------------|-------------|-------------|
| **GroupByQuery1.sql** | Count customers per state | COUNT with GROUP BY |
| **GroupByQuery2.sql** | Average discount by category | AVG with GROUP BY |
| **GroupByQuery3.sql** | Total number of orders per customer | COUNT with GROUP BY |
| **GroupByQuery4.sql** | Most expensive product per category | MAX with GROUP BY |
| **GroupByQuery5.sql** | Total order value per order | SUM with calculations |

## Example Query Results

### Simple Query Example
```sql
-- SimpleQuery1.sql
SELECT product_name, list_price
FROM products;
```
**Result**: Shows all products with their prices

### Inner Join Example
```sql
-- InnerJoinQuery1.sql
SELECT p.product_name, c.category_name
FROM products p
INNER JOIN categories c 
ON p.category_id = c.category_id;
```
**Result**: Products displayed with their category names

### Group By Example
```sql
-- GroupByQuery1.sql
SELECT state, COUNT(*) AS num_customers
FROM addresses
GROUP BY state;
```
**Result**: Customer count grouped by state

## Container Management

### Useful Docker Commands

**Start the database (in the background):**
```bash
docker-compose up -d
```

**Stop the database (stops the container):**
```bash
docker-compose down
```

**View container status:**
```bash
docker-compose ps
```

**View container logs:**
```bash
docker-compose logs mysql
```

### Data Persistence
- Database data is stored in the `mysql_data` Docker volume
- Data persists across container restarts and system reboots
- To completely reset the database, use `docker-compose down -v`

## Troubleshooting

### Common Issues:
- **"Database not found"**: Make sure you executed the `createguitar.sql` script first
- **"Table doesn't exist"**: Verify the database was created successfully
- **"Wrong port"**: Use port 3307 (not 3306) for the host connection
- **"Wrong database selected"**: Use Ctrl+0 to select the `my_guitar_shop` database

### Container-Specific Issues:
- **"Port already in use"**: Change the port mapping in docker-compose.yaml

## Key Differences from Lab 5

- **Deployment**: Containerized MySQL vs local MySQL installation
- **Port**: 3307 (mapped) vs 3306 (direct)
- **Management**: Docker Compose vs system service management
- **Isolation**: Containerized environment vs system-wide installation
- **Persistence**: Docker volumes vs system file storage

## Technologies Used

- **Docker** – Container platform for application isolation
- **Docker Compose** – Multi-container application orchestration
- **MySQL 9.3** – Relational database management system
- **DBeaver** – Universal database management tool
- **SQL** – Structured Query Language
