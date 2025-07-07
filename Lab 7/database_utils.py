"""
Database Utilities for Lab 7
============================

This module provides database connectivity and query execution functions
for the MySQL database used in Lab 7.
"""

import mysql.connector
from typing import List, Tuple, Dict, Any, Optional


def ensure_database_exists(host: str = "localhost", port: int = 3307, 
                           user: str = "root", password: str = "secret_password", 
                           database_file: str = "createguitar.sql") -> None:
    """
    Ensure the specified database exists. If not, create it.
    """
    try:
        # Connect to MySQL server (no database specified)
        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            connection_timeout=10,
            autocommit=True
        )
        with open(database_file, 'r') as f:
            sql_script = f.read()
        sql_commands = sql_script.split(';')
            
        mycursor = mydb.cursor()
        for command in sql_commands:
            mycursor.execute(command)
        mycursor.close()
        mydb.close()
    except mysql.connector.Error as err:
        print(f"Error ensuring database exists: {err}")
        raise


def connect_to_db(host: str = "localhost", port: int = 3307, 
                  user: str = "root", password: str = "secret_password",
                  database: str = "my_guitar_shop",
                  database_file: str = "createguitar.sql") -> Optional[mysql.connector.MySQLConnection]:
    """
    Connect to the MySQL database, ensuring it exists first.
    """
    try:
        ensure_database_exists(host, port, user, password, database_file)
        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            connection_timeout=10,
            autocommit=True
        )
        print("Successfully connected to MySQL database!")
        return mydb
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None


def execute_query_with_headers(mydb: mysql.connector.MySQLConnection, sql_query: str) -> Optional[Dict[str, Any]]:
    """
    Execute a SQL query and return results with column headers.
    
    Args:
        mydb: MySQL connection object
        sql_query: SQL query to execute
    
    Returns:
        Dictionary with 'headers' and 'data' keys, or None if query fails
    """
    try:
        # Reconnect if connection is lost
        if mydb is None or not mydb.is_connected():
            print("Reconnection to db required")
            mydb = connect_to_db()
            if mydb is None:
                return None

        # Create a cursor object to execute SQL queries
        mycursor = mydb.cursor()

        # Execute the query
        mycursor.execute(sql_query)

        # Get column headers
        headers = [desc[0] for desc in mycursor.description]

        # Fetch all the results
        data = mycursor.fetchall()
        
        return {
            'headers': headers,
            'data': data
        }

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        return None


def format_query_results_as_table(headers: List[str], data: List[Tuple]) -> str:
    """
    Format query results as a nicely formatted table.
    
    Args:
        headers: List of column headers
        data: List of data rows
    
    Returns:
        Formatted table string
    """
    if not data:
        return "No data returned."
    
    # Calculate column widths
    col_widths = []
    for i, header in enumerate(headers):
        # Start with header width
        max_width = len(str(header))
        # Check data column widths
        for row in data:
            if i < len(row):
                max_width = max(max_width, len(str(row[i])))
        col_widths.append(max_width)
    
    # Create separator line
    separator = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+"
    
    # Build table
    table_lines = []
    table_lines.append(separator)
    
    # Header row
    header_row = "|"
    for i, header in enumerate(headers):
        header_row += f" {str(header):<{col_widths[i]}} |"
    table_lines.append(header_row)
    table_lines.append(separator)
    
    # Data rows
    for row in data:
        data_row = "|"
        for i, cell in enumerate(row):
            data_row += f" {str(cell):<{col_widths[i]}} |"
        table_lines.append(data_row)
    
    table_lines.append(separator)
    
    return "\n".join(table_lines)


def execute_query_with_table_format(mydb: mysql.connector.MySQLConnection, sql_query: str) -> Optional[str]:
    """
    Execute a SQL query and return results formatted as a table string.
    
    Args:
        mydb: MySQL connection object
        sql_query: SQL query to execute
    
    Returns:
        Formatted table string or None if query fails
    """
    result = execute_query_with_headers(mydb, sql_query)
    if result:
        return format_query_results_as_table(result['headers'], result['data'])
    return None


def close_connection(mydb: mysql.connector.MySQLConnection) -> None:
    """
    Close the MySQL database connection.
    
    Args:
        mydb: MySQL connection object
    """
    try:
        if mydb and mydb.is_connected():
            mydb.close()
            print("MySQL connection closed.")
    except mysql.connector.Error as err:
        print(f"Error closing connection: {err}")


# Predefined queries
QUERIES = {
    # Simple queries
    "simple_1": {
        "name": "List all product names and prices",
        "query": "SELECT product_name, list_price FROM products;"
    },
    "simple_2": {
        "name": "List all customers with the last name Brown",
        "query": "SELECT first_name, last_name, email_address FROM customers WHERE last_name = 'Brown';"
    },
    "simple_3": {
        "name": "Products with a discount over 25%",
        "query": "SELECT product_name, list_price, discount_percent FROM products WHERE discount_percent > 25;"
    },
    
    # Inner join queries
    "join_1": {
        "name": "Products with their category names",
        "query": "SELECT p.product_name, c.category_name FROM products p INNER JOIN categories c ON p.category_id = c.category_id;"
    },
    "join_2": {
        "name": "Orders with customer information",
        "query": "SELECT o.order_id, o.order_date, c.first_name, c.last_name FROM orders o INNER JOIN customers c ON o.customer_id = c.customer_id;"
    },
    "join_3": {
        "name": "Order items with product details",
        "query": "SELECT oi.item_id, p.product_name, oi.quantity, oi.item_price FROM order_items oi INNER JOIN products p ON oi.product_id = p.product_id;"
    },
    "join_4": {
        "name": "Shipping address for each order",
        "query": "SELECT o.order_id, a.line1, a.city, a.state FROM orders o INNER JOIN addresses a ON o.ship_address_id = a.address_id;"
    },
    "join_5": {
        "name": "Customer's addresses",
        "query": "SELECT c.first_name, c.last_name, a.line1, a.city, a.state FROM customers c INNER JOIN addresses a ON c.customer_id = a.customer_id;"
    },
    
    # Group by queries
    "group_1": {
        "name": "Count customers per state",
        "query": "SELECT state, COUNT(*) AS num_customers FROM addresses GROUP BY state;"
    },
    "group_2": {
        "name": "Average discount by category",
        "query": "SELECT c.category_name, AVG(p.discount_percent) AS avg_discount FROM products p INNER JOIN categories c ON p.category_id = c.category_id GROUP BY c.category_name;"
    },
    "group_3": {
        "name": "Total number of orders per customer",
        "query": "SELECT c.first_name, c.last_name, COUNT(o.order_id) AS total_orders FROM customers c INNER JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.first_name, c.last_name;"
    },
    "group_4": {
        "name": "Most expensive product per category",
        "query": "SELECT c.category_name, MAX(p.list_price) AS max_price FROM products p INNER JOIN categories c ON p.category_id = c.category_id GROUP BY c.category_name;"
    },
    "group_5": {
        "name": "Total order value per order",
        "query": "SELECT o.order_id, SUM(oi.quantity * oi.item_price) AS total_value FROM orders o INNER JOIN order_items oi ON o.order_id = oi.order_id GROUP BY o.order_id;"
    }
}


def get_query_by_key(key: str) -> Optional[Dict[str, str]]:
    """
    Get a query by its key.
    
    Args:
        key: Query key from QUERIES dictionary
    
    Returns:
        Query dictionary with 'name' and 'query' keys, or None if key not found
    """
    return QUERIES.get(key)


def list_all_queries() -> Dict[str, str]:
    """
    Get a list of all available queries with their names.
    
    Returns:
        Dictionary mapping query keys to their names
    """
    return {key: query["name"] for key, query in QUERIES.items()} 