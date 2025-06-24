# COMP3480 Lab 5 - SQL Database Queries

This project focuses on creating and executing various SQL queries using a guitar shop database. The main goal is to learn SQL query development with different types of joins, aggregations, and database operations using DBeaver as the database management tool.

## Learning Goals

- Learn to create and execute SQL queries in a database management tool
- Practice simple single-table queries for basic data retrieval
- Understand and implement inner joins to combine data from multiple tables
- Master aggregation functions and GROUP BY clauses for data analysis
- Develop proficiency with DBeaver database management interface
- Analyze real-world data relationships in a business context

## Features

- **13 SQL Queries**: Comprehensive query set covering different SQL concepts
- **Simple Queries**: 3 basic single-table queries for data retrieval
- **Inner Join Queries**: 5 queries demonstrating table relationships
- **Aggregation Queries**: 5 queries using GROUP BY and functions
- **Real Business Data**: Guitar shop database with products, customers, and orders
- **DBeaver Integration**: Complete setup and execution instructions

## How To Use

### Prerequisites
- DBeaver Community Edition (free database tool)
- MySQL Server installed and running
- Basic knowledge of SQL syntax

### Database Setup

1. **Open DBeaver** and connect to your MySQL server
2. **Open the `createguitar.sql` file** in DBeaver:
   - Go to File → Open File
   - Navigate to the Lab 5 folder and select `createguitar.sql`
3. **Execute the script**:
   - Click the "Execute SQL Script" button (▶️) or press Ctrl+Alt+X
   - This will create the database, tables, and insert sample data

### Running Queries

#### Method 1: Using SQL Editor
1. **Open a new SQL Editor**:
   - Click the "SQL Editor" button or press Ctrl+]
2. **Select your datasource**:
   - Press **Ctrl+9** to open the datasource selection dialog
   - Choose your MySQL connection
3. **Select the database**:
   - Press **Ctrl+0** to open the database selection dialog
   - Choose `my_guitar_shop` database
4. **Open a query file**:
   - Go to File → Open File
   - Select any `.sql` file from the Lab 5 folder
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

## Troubleshooting

### Common Issues:
- **"Database not found"**: Make sure you executed the `createguitar.sql` script first
- **"Table doesn't exist"**: Verify the database was created successfully
- **"Connection failed"**: Check your MySQL server is running and credentials are correct
- **"Wrong database selected"**: Use Ctrl+0 to select the `my_guitar_shop` database
- **"Wrong datasource"**: Use Ctrl+9 to select your MySQL connection

## Technologies Used

- **MySQL** – Relational database management system
- **DBeaver** – Universal database management tool
- **SQL** – Structured Query Language