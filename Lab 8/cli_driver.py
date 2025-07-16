"""
Python Command Line Driver Program for Lab 7 FastAPI Services and Database
==========================================================================

This program provides an interactive command-line interface to access
all route services available in the Lab 2 FastAPI application and
execute database queries.

Usage: python cli_driver.py
"""

import requests
import json
import sys
import os
import redis
import smtplib
import io
from typing import Optional, Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from minio import Minio
from minio.error import S3Error
from database_utils import (
    connect_to_db, close_connection,
    get_query_by_key, list_all_queries
)


def clear_terminal():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


class FastAPIDriver:
    """Driver class to interact with FastAPI Lab 2 services."""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        """Initialize the driver with base URL."""
        self.base_url = base_url.rstrip('/')
        self.db_connection = None
        
    def check_server_status(self) -> bool:
        """Check if the FastAPI server is running."""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                    json_data: Optional[Dict] = None, headers: Optional[Dict] = None,
                    cookies: Optional[Dict] = None) -> Optional[Dict[Any, Any]]:
        """Make HTTP request and handle response."""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == 'GET':
                response = requests.get(url, params=params, headers=headers, cookies=cookies)
            elif method.upper() == 'POST':
                response = requests.post(url, json=json_data, params=params, headers=headers, cookies=cookies)
            else:
                print(f"ERROR: Unsupported HTTP method: {method}")
                return None
            
            print(f"REQUEST: {method.upper()} {url}")
            if params:
                print(f"Query Parameters: {params}")
            if json_data:
                print(f"Request Body: {json.dumps(json_data, indent=2)}")
            if headers:
                print(f"Headers: {headers}")
            if cookies:
                print(f"Cookies: {cookies}")
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
                return result
            else:
                print(f"ERROR: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Request failed: {e}")
            return None

    # Database methods
    def execute_predefined_query(self, query_key: str):
        """Execute a predefined query by key."""
        clear_terminal()
        print("="*60)
        print("Executing Predefined Query")
        print("="*60)
        
        query_info = get_query_by_key(query_key)
        if not query_info:
            print(f"ERROR: Query key '{query_key}' not found.")
            return
        
        print(f"Query: {query_info['name']}")
        print(f"SQL: {query_info['query']}")
        print("-" * 60)
        
        # Connect to database if not already connected
        if not self.db_connection:
            self.db_connection = connect_to_db()
            if not self.db_connection:
                print("Failed to connect to database. Please ensure MySQL container is running.")
                return
        
        from database_utils import execute_query_with_table_format, execute_query_with_headers
        result = execute_query_with_table_format(self.db_connection, query_info['query'])
        
        if result:
            print(result)
            # Get actual row count from the data
            data_result = execute_query_with_headers(self.db_connection, query_info['query'])
            if data_result and data_result['data']:
                print(f"\nTotal rows: {len(data_result['data'])}")
            else:
                print("\nTotal rows: 0")
        else:
            print("Failed to execute query.")
    
    def execute_custom_query(self):
        """Execute a custom SQL query."""
        clear_terminal()
        print("="*60)
        print("Execute Custom SQL Query")
        print("="*60)
        
        # Connect to database if not already connected
        if not self.db_connection:
            self.db_connection = connect_to_db()
            if not self.db_connection:
                print("Failed to connect to database. Please ensure MySQL container is running.")
                return
        
        print("Enter your SQL query (type 'exit' to cancel):")
        print("Example: SELECT * FROM products LIMIT 5;")
        print("-" * 60)
        
        sql_query = input("SQL Query: ").strip()
        
        if sql_query.lower() == 'exit':
            print("Query cancelled.")
            return
        
        if not sql_query:
            print("No query entered.")
            return
        
        print(f"\nExecuting: {sql_query}")
        print("-" * 60)
        
        from database_utils import execute_query_with_table_format, execute_query_with_headers
        result = execute_query_with_table_format(self.db_connection, sql_query)
        
        if result:
            print(result)
            # Get actual row count from the data
            data_result = execute_query_with_headers(self.db_connection, sql_query)
            if data_result and data_result['data']:
                print(f"\nTotal rows: {len(data_result['data'])}")
            else:
                print("\nTotal rows: 0")
        else:
            print("Failed to execute query.")
    
    def test_root(self):
        """Test the root endpoint."""
        clear_terminal()
        print("="*60)
        print("Testing Root Endpoint")
        print("="*60)
        self.make_request('GET', '/')
    
    def test_greet(self):
        """Test the greet endpoint with default and custom names."""
        clear_terminal()
        print("="*60)
        print("Testing Greet Endpoint")
        print("="*60)
        
        # Default greeting
        print("\nTesting default greeting:")
        self.make_request('GET', '/greet')
        
        # Custom name
        print("\nTesting custom name:")
        name = input("Enter a name (or press Enter for 'Aniket'): ").strip()
        if not name:
            name = "Aniket"
        self.make_request('GET', '/greet', params={'name': name})
    
    def test_cube(self):
        """Test the cube calculation endpoint."""
        clear_terminal()
        print("="*60)
        print("Testing Cube Calculation")
        print("="*60)
        
        try:
            number = input("Enter a number to cube (or press Enter for 3): ").strip()
            if not number:
                number = "3"
            number = int(number)
            self.make_request('GET', f'/cube/{number}')
        except ValueError:
            print("ERROR: Invalid number. Using default value 3.")
            self.make_request('GET', '/cube/3')
    
    def test_add(self):
        """Test the addition endpoint."""
        clear_terminal()
        print("="*60)
        print("Testing Addition")
        print("="*60)
        
        try:
            a = input("Enter first number (or press Enter for 5): ").strip()
            if not a:
                a = "5"
            a = int(a)
            
            b = input("Enter second number (or press Enter for 7): ").strip()
            if not b:
                b = "7"
            b = int(b)
            
            self.make_request('GET', '/add', params={'a': a, 'b': b})
        except ValueError:
            print("ERROR: Invalid numbers. Using default values 5 and 7.")
            self.make_request('GET', '/add', params={'a': 5, 'b': 7})
    
    def test_factorial(self):
        """Test the factorial calculation endpoint."""
        clear_terminal()
        print("="*60)
        print("Testing Factorial Calculation")
        print("="*60)
        
        try:
            n = input("Enter a number for factorial (or press Enter for 5): ").strip()
            if not n:
                n = "5"
            n = int(n)
            if n < 0:
                print("ERROR: Factorial is not defined for negative numbers. Using 5.")
                n = 5
            self.make_request('GET', f'/factorial/{n}')
        except ValueError:
            print("ERROR: Invalid number. Using default value 5.")
            self.make_request('GET', '/factorial/5')
    
    def test_person(self):
        """Test the person info POST endpoint."""
        clear_terminal()
        print("="*60)
        print("Testing Person Info")
        print("="*60)
        
        name = input("Enter person's name (or press Enter for 'Alex'): ").strip()
        if not name:
            name = "Alex"
        
        try:
            age_input = input("Enter person's age (or press Enter for 17): ").strip()
            if not age_input:
                age = 17
            else:
                age = int(age_input)
            
            person_data = {"name": name, "age": age}
            self.make_request('POST', '/person', json_data=person_data)
        except ValueError:
            print("ERROR: Invalid age. Using default values.")
            self.make_request('POST', '/person', json_data={"name": "Alex", "age": 17})
    
    def test_city_info(self):
        """Test the city info endpoint."""
        clear_terminal()
        print("="*60)
        print("Testing City Information")
        print("="*60)
        
        print("Available cities with info: Boston, NewYork, Seattle, Miami, Dallas")
        city = input("Enter a city name (or press Enter for 'Boston'): ").strip()
        if not city:
            city = "Boston"
        
        self.make_request('GET', f'/city/{city}')
    
    def test_rectangle_area(self):
        """Test the rectangle area calculation endpoint."""
        clear_terminal()
        print("="*60)
        print("Testing Rectangle Area Calculation")
        print("="*60)
        
        try:
            width = input("Enter rectangle width (or press Enter for 4.0): ").strip()
            if not width:
                width = 4.0
            else:
                width = float(width)
            
            height = input("Enter rectangle height (or press Enter for 5.0): ").strip()
            if not height:
                height = 5.0
            else:
                height = float(height)
            
            rect_data = {"width": width, "height": height}
            self.make_request('POST', '/area/rectangle', json_data=rect_data)
        except ValueError:
            print("ERROR: Invalid dimensions. Using default values.")
            self.make_request('POST', '/area/rectangle', json_data={"width": 4.0, "height": 5.0})
    
    def test_power(self):
        """Test the power calculation endpoint."""
        clear_terminal()
        print("="*60)
        print("Testing Power Calculation")
        print("="*60)
        
        try:
            base = input("Enter base number (or press Enter for 2): ").strip()
            if not base:
                base = 2
            else:
                base = int(base)
            
            exp = input("Enter exponent (or press Enter for default 2): ").strip()
            if exp:
                exp = int(exp)
                self.make_request('GET', f'/power/{base}', params={'exp': exp})
            else:
                print("Using default exponent (2)")
                self.make_request('GET', f'/power/{base}')
        except ValueError:
            print("ERROR: Invalid numbers. Using default values.")
            self.make_request('GET', '/power/2')
    
    def test_colors(self):
        """Test the colors list endpoint."""
        clear_terminal()
        print("="*60)
        print("Testing Colors List")
        print("="*60)
        self.make_request('GET', '/colors')
    
    def test_protected_data(self):
        """Test the protected data endpoint with header authentication."""
        clear_terminal()
        print("="*60)
        print("Testing Protected Data (Header Authentication)")
        print("="*60)
        
        print("This endpoint requires an API key in the header.")
        print("Valid API key: mysecretkey")
        
        # Test without API key first
        print("\nTesting without API key:")
        self.make_request('GET', '/protected-data')
        
        # Test with API key
        print("\nTesting with API key:")
        api_key = input("Enter API key (or press Enter for 'mysecretkey'): ").strip()
        if not api_key:
            api_key = "mysecretkey"
        
        headers = {"api-key": api_key}
        self.make_request('GET', '/protected-data', headers=headers)
    
    def test_cookie_greet(self):
        """Test the cookie-based personal greeting endpoint."""
        clear_terminal()
        print("="*60)
        print("Testing Cookie-Based Personal Greeting")
        print("="*60)
        
        print("This endpoint uses cookies to personalize greetings.")
        
        # Test without cookie first
        print("\nTesting without cookie:")
        self.make_request('GET', '/cookie-greet')
        
        # Test with cookie
        print("\nTesting with username cookie:")
        username = input("Enter username for cookie (or press Enter for 'JohnDoe'): ").strip()
        if not username:
            username = "JohnDoe"
        
        cookies = {"username": username}
        self.make_request('GET', '/cookie-greet', cookies=cookies)
    
    def test_redis_service(self):
        """Test Redis shared memory functionality."""
        clear_terminal()
        print("="*60)
        print("Testing Redis Shared Memory Service")
        print("="*60)
        
        try:
            # Connect to Redis
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)
            
            # Test connection
            print("Testing Redis connection...")
            r.ping()
            print("SUCCESS: Connected to Redis successfully!")
            
            # Set a key-value pair
            key = input("Enter a key to store (or press Enter for 'test_key'): ").strip()
            if not key:
                key = "test_key"
            
            value = input("Enter a value to store (or press Enter for 'test_value'): ").strip()
            if not value:
                value = "test_value"
            
            r.set(key, value)
            print(f"SUCCESS: Stored: {key} = {value}")
            
            # Retrieve the value
            retrieved = r.get(key)
            print(f"SUCCESS: Retrieved: {key} = {retrieved}")
            
            # List all keys
            keys = r.keys('*')
            print(f"SUCCESS: All keys in Redis: {keys}")
            
            # Test with expiration
            exp_key = "temp_key"
            r.setex(exp_key, 30, "This expires in 30 seconds")
            ttl = r.ttl(exp_key)
            print(f"SUCCESS: Set temporary key '{exp_key}' with TTL: {ttl} seconds")
            
        except redis.ConnectionError:
            print("ERROR: Could not connect to Redis. Make sure Redis container is running.")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_minio_service(self):
        """Test MinIO shared file system functionality."""
        clear_terminal()
        print("="*60)
        print("Testing MinIO Shared File System Service")
        print("="*60)
        
        try:
            # Connect to MinIO
            client = Minio(
                "localhost:9000",
                access_key="minioadmin",
                secret_key="minioadmin123",
                secure=False
            )
            
            print("Testing MinIO connection...")
            
            # Create bucket if it doesn't exist
            bucket_name = "lab8-bucket"
            if not client.bucket_exists(bucket_name):
                client.make_bucket(bucket_name)
                print(f"SUCCESS: Created bucket: {bucket_name}")
            else:
                print(f"SUCCESS: Bucket already exists: {bucket_name}")
            
            # Upload a file
            file_name = input("Enter filename to create (or press Enter for 'test.txt'): ").strip()
            if not file_name:
                file_name = "test.txt"
            
            content = input("Enter file content (or press Enter for 'Hello from Lab 8!'): ").strip()
            if not content:
                content = "Hello from Lab 8!"
            
            # Create a file-like object from string
            data = io.BytesIO(content.encode('utf-8'))
            
            client.put_object(
                bucket_name,
                file_name,
                data,
                len(content.encode('utf-8')),
                content_type='text/plain'
            )
            print(f"SUCCESS: Uploaded file: {file_name}")
            
            # List files in bucket
            objects = client.list_objects(bucket_name)
            print("SUCCESS: Files in bucket:")
            for obj in objects:
                print(f"  - {obj.object_name} (Size: {obj.size} bytes)")
            
            # Download and display file content
            response = client.get_object(bucket_name, file_name)
            downloaded_content = response.read().decode('utf-8')
            print(f"SUCCESS: Downloaded content: {downloaded_content}")
            response.close()
            response.release_conn()
            
        except S3Error as e:
            print(f"ERROR: MinIO Error: {e}")
        except Exception as e:
            print(f"ERROR: {e}")
    
    def test_postfix_service(self):
        """Test Postfix email server functionality."""
        clear_terminal()
        print("="*60)
        print("Testing Postfix Email Server Service")
        print("="*60)
        
        print("   IMPORTANT: This will attempt to send a REAL email!")
        print("   The email will likely be rejected by most recipient servers as spam.")
        print("   This demonstrates real email sending behavior.")
        print("="*60)
        
        try:
            # Connect to SMTP server
            print("Testing SMTP connection...")
            
            sender_email = "test@wit.edu"
            recipient_email = input("Enter recipient email (or press Enter for 'jaldua@wit.edu'): ").strip()
            if not recipient_email:
                recipient_email = "jaldua@wit.edu"
            
            subject = input("Enter email subject (or press Enter for 'Lab 8 Test Email'): ").strip()
            if not subject:
                subject = "Lab 8 Test Email"
            
            body = input("Enter email body (or press Enter for default message): ").strip()
            if not body:
                body = """
Hello!

This is a test email from Lab 8 Postfix service.
This email was sent from a local Postfix server without proper authentication.
It will likely be flagged as spam by the recipient's email server.

This demonstrates real email sending behavior in a lab environment.

Best regards,
Lab 8 CLI Driver
"""
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server
            server = smtplib.SMTP('localhost', 1587)
            server.set_debuglevel(1)  # Enable debug output
            
            text = msg.as_string()
            
            print(f"\nAttempting to send REAL email from {sender_email} to {recipient_email}...")
            print("   This will attempt to send via the internet (not just local queue)")
            print("   Expected result: Rejection by recipient server due to spam filters")
            print("="*60)
            
            try:
                server.sendmail(sender_email, recipient_email, text)
                print("SUCCESS: Email was accepted by local Postfix server!")
                print("   Note: Email may still be rejected by recipient server")
                print("   Check the debug output above for delivery status")
            except Exception as send_error:
                print(f"ERROR: Email sending failed: {send_error}")
                print("   This is expected behavior - the email server rejected the message")
                print("   Common reasons: spam filters, authentication requirements, etc.")
            
            server.quit()
            
            print("\n" + "="*60)
            print("Email Test Summary:")
            print("   SUCCESS: SMTP connection established")
            print("   SUCCESS: Email message created and sent to Postfix")
            print("   SUCCESS: Real email delivery attempted")
            print("   SUCCESS: Expected failure demonstrates spam filter behavior")
            print("="*60)
            
        except Exception as e:
            print(f"ERROR: Error connecting to SMTP server: {e}")
            print("Make sure Postfix container is running on localhost:1587")


def print_banner():
    """Print application banner."""
    print("="*60)
    print("FastAPI Lab 8 - Command Line Driver")
    print("Multi-Service System: API, Database, File Storage, Cache & Email")
    print("="*60)


def print_menu():
    """Print the main menu."""
    print("\n" + "="*60)
    print("LAB 8 SERVICES:")
    print("="*60)
    print("API SERVICES:")
    print("1.  FastAPI Services Menu")
    print("\nNEW LAB 8 SERVICES:")
    print("2.  Redis Cache Service (Shared Memory)")
    print("3.  MinIO File Service (Object Storage)")
    print("4.  Postfix Email Service (SMTP Server)")
    print("\nSYSTEM OPERATIONS:")
    print("5.  Database Operations")
    print("6.  Run All Tests (Auto)")
    print("7.  Check All Services Status")
    print("0.  Exit")
    print("="*60)


def print_api_menu():
    """Print the FastAPI services submenu."""
    print("\n" + "="*60)
    print("FASTAPI ROUTE SERVICES:")
    print("="*60)
    print("1.  Root Endpoint                (/)")
    print("2.  Greet Service                (/greet)")
    print("3.  Cube Calculator              (/cube/{number})")
    print("4.  Addition Service             (/add)")
    print("5.  Factorial Calculator         (/factorial/{n})")
    print("6.  Person Info                  (/person)")
    print("7.  City Information             (/city/{city_name})")
    print("8.  Rectangle Area Calculator    (/area/rectangle)")
    print("9.  Power Calculator             (/power/{base})")
    print("10. Colors List                  (/colors)")
    print("11. Protected Data               (/protected-data)")
    print("12. Cookie Personal Greeting     (/cookie-greet)")
    print("0.  Back to Main Menu")
    print("="*60)


def print_db_menu():
    """Print the database operations submenu."""
    from database_utils import list_all_queries
    queries = list_all_queries()
    
    # Categorize queries
    simple = [(k, v) for k, v in queries.items() if k.startswith('simple_')]
    join = [(k, v) for k, v in queries.items() if k.startswith('join_')]
    group = [(k, v) for k, v in queries.items() if k.startswith('group_')]
    
    print("\n" + "="*60)
    print("DATABASE OPERATIONS:")
    print("="*60)
    
    # Simple queries (1-3)
    print("Simple Queries:")
    for i, (k, v) in enumerate(simple, 1):
        print(f"{i}. {v}")
    
    # Join queries (4-8)
    print("\nJoin Queries:")
    for i, (k, v) in enumerate(join, len(simple) + 1):
        print(f"{i}. {v}")
    
    # Group by queries (9-13)
    print("\nGroup By Queries:")
    for i, (k, v) in enumerate(group, len(simple) + len(join) + 1):
        print(f"{i}. {v}")
    
    # Custom query (14)
    custom_option = len(simple) + len(join) + len(group) + 1
    print(f"\n{custom_option}. Execute Custom SQL Query")
    print(f"0. Back to Main Menu")
    print("="*60)


def main():
    """Main function to run the CLI driver."""
    clear_terminal()
    print_banner()
    
    # Get server URL
    server_url = input("\nEnter FastAPI server URL (or press Enter for http://localhost:8080): ").strip()
    if not server_url:
        server_url = "http://localhost:8080"
    
    driver = FastAPIDriver(server_url)
    
    # Check server status
    print(f"\nChecking server status at {server_url}...")
    if not driver.check_server_status():
        print(f"ERROR: Server is not responding at {server_url}")
        print("Make sure the FastAPI server is running in a Docker container.")
        
        continue_anyway = input("\nContinue anyway? (y/N): ").strip().lower()
        if continue_anyway != 'y':
            print("Goodbye!")
            sys.exit(1)
    else:
        print("Server is running and accessible!")
    
    input("\nPress Enter to continue to main menu...")
    
    # Main loop
    while True:
        clear_terminal()
        print_banner()
        print_menu()
        
        try:
            choice = input("\nSelect an option (0-7): ").strip()
            
            if choice == '0':
                if driver.db_connection:
                    close_connection(driver.db_connection)
                clear_terminal()
                print("="*60)
                print("Thank you for using FastAPI Lab 8 Driver!")
                print("Goodbye!")
                print("="*60)
                break
            elif choice == '1':
                # FastAPI Services Submenu
                while True:
                    clear_terminal()
                    print_banner()
                    print_api_menu()
                    api_choice = input("\nSelect an API service (0 to return): ").strip()
                    
                    if api_choice == '0':
                        break
                    elif api_choice == '1':
                        driver.test_root()
                    elif api_choice == '2':
                        driver.test_greet()
                    elif api_choice == '3':
                        driver.test_cube()
                    elif api_choice == '4':
                        driver.test_add()
                    elif api_choice == '5':
                        driver.test_factorial()
                    elif api_choice == '6':
                        driver.test_person()
                    elif api_choice == '7':
                        driver.test_city_info()
                    elif api_choice == '8':
                        driver.test_rectangle_area()
                    elif api_choice == '9':
                        driver.test_power()
                    elif api_choice == '10':
                        driver.test_colors()
                    elif api_choice == '11':
                        driver.test_protected_data()
                    elif api_choice == '12':
                        driver.test_cookie_greet()
                    else:
                        print("Invalid API service option.")
                    
                    if api_choice != '0':
                        input("\nPress Enter to continue...")
            elif choice == '2':
                # Redis Service
                driver.test_redis_service()
            elif choice == '3':
                # MinIO Service
                driver.test_minio_service()
            elif choice == '4':
                # Postfix Service
                driver.test_postfix_service()
            elif choice == '5':
                # Database Operations Submenu
                while True:
                    clear_terminal()
                    print_banner()
                    print_db_menu()
                    db_choice = input("\nSelect a database option (0 to return): ").strip()
                    
                    from database_utils import list_all_queries, get_query_by_key
                    queries = list_all_queries()
                    simple = [k for k in queries if k.startswith('simple_')]
                    join = [k for k in queries if k.startswith('join_')]
                    group = [k for k in queries if k.startswith('group_')]
                    
                    if db_choice == '0':
                        break
                    elif db_choice.isdigit():
                        choice_num = int(db_choice)
                        
                        # Simple queries (1-3)
                        if 1 <= choice_num <= len(simple):
                            driver.execute_predefined_query(simple[choice_num - 1])
                        
                        # Join queries (4-8)
                        elif len(simple) + 1 <= choice_num <= len(simple) + len(join):
                            join_index = choice_num - len(simple) - 1
                            driver.execute_predefined_query(join[join_index])
                        
                        # Group by queries (9-13)
                        elif len(simple) + len(join) + 1 <= choice_num <= len(simple) + len(join) + len(group):
                            group_index = choice_num - len(simple) - len(join) - 1
                            driver.execute_predefined_query(group[group_index])
                        
                        # Custom query (14)
                        elif choice_num == len(simple) + len(join) + len(group) + 1:
                            driver.execute_custom_query()
                        
                        else:
                            print("Invalid database option.")
                    else:
                        print("Invalid database option.")
                    
                    input("\nPress Enter to continue...")
            elif choice == '6':
                # Run all tests (API + DB + New Services)
                import subprocess
                clear_terminal()
                print("="*60)
                print("RUNNING ALL TESTS (API + DATABASE + NEW SERVICES)")
                print("="*60)
                subprocess.run(["python", "test.py"])
            elif choice == '7':
                # Check all services status
                clear_terminal()
                print("="*60)
                print("ALL SERVICES STATUS CHECK")
                print("="*60)
                
                # FastAPI Server
                print(f"1. FastAPI Server ({server_url})...")
                if driver.check_server_status():
                    print("FastAPI Server is running!")
                else:
                    print(f"FastAPI Server is not responding")
                
                # Redis
                print("2. Redis Cache Service...")
                try:
                    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
                    r.ping()
                    print("Redis is running!")
                except:
                    print("Redis is not responding")
                
                # MinIO
                print("3. MinIO File Storage...")
                try:
                    client = Minio("localhost:9000", access_key="minioadmin", secret_key="minioadmin123", secure=False)
                    client.list_buckets()
                    print("MinIO is running!")
                except:
                    print("MinIO is not responding")
                
                # Postfix
                print("4. Postfix Email Server...")
                try:
                    server = smtplib.SMTP('localhost', 1587, timeout=5)
                    server.quit()
                    print("Postfix is running!")
                except:
                    print("Postfix is not responding")
                
                # Database
                print("5. MySQL Database...")
                try:
                    conn = connect_to_db()
                    if conn:
                        print("MySQL Database is running!")
                        close_connection(conn)
                    else:
                        print("MySQL Database connection failed")
                except:
                    print("MySQL Database is not responding")
            else:
                clear_terminal()
                print("="*60)
                print("ERROR: Invalid choice. Please select 0-7.")
                print("="*60)
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            if driver.db_connection:
                close_connection(driver.db_connection)
            clear_terminal()
            print("="*60)
            print("Interrupted by user.")
            print("Goodbye!")
            print("="*60)
            break
        except Exception as e:
            clear_terminal()
            print("="*60)
            print(f"ERROR: An error occurred: {e}")
            print("="*60)
            input("Press Enter to continue...")


if __name__ == "__main__":
    main() 