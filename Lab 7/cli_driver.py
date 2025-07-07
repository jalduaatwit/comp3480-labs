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
from typing import Optional, Dict, Any
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


def print_banner():
    """Print application banner."""
    print("="*60)
    print("FastAPI Lab 7 - Command Line Driver")
    print("Interactive Route Service Tester & Database Query Executor")
    print("="*60)


def print_menu():
    """Print the main menu."""
    print("\n" + "="*60)
    print("AVAILABLE ROUTE SERVICES:")
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
    print("="*60)
    print("13. Database Operations")
    print("14. Run All Tests (Auto)")
    print("15. Check Server Status")
    print("0.  Exit")
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
            choice = input("\nSelect an option (0-15): ").strip()
            
            if choice == '0':
                if driver.db_connection:
                    close_connection(driver.db_connection)
                clear_terminal()
                print("="*60)
                print("Thank you for using FastAPI Lab 7 Driver!")
                print("Goodbye!")
                print("="*60)
                break
            elif choice == '1':
                driver.test_root()
            elif choice == '2':
                driver.test_greet()
            elif choice == '3':
                driver.test_cube()
            elif choice == '4':
                driver.test_add()
            elif choice == '5':
                driver.test_factorial()
            elif choice == '6':
                driver.test_person()
            elif choice == '7':
                driver.test_city_info()
            elif choice == '8':
                driver.test_rectangle_area()
            elif choice == '9':
                driver.test_power()
            elif choice == '10':
                driver.test_colors()
            elif choice == '11':
                driver.test_protected_data()
            elif choice == '12':
                driver.test_cookie_greet()
            elif choice == '13':
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
            elif choice == '14':
                # Run all tests (API + DB)
                import subprocess
                clear_terminal()
                print("="*60)
                print("RUNNING ALL TESTS (API + DATABASE)")
                print("="*60)
                subprocess.run(["python", "test.py"])
            elif choice == '15':
                clear_terminal()
                print("="*60)
                print("Server Status Check")
                print("="*60)
                print(f"Checking server status at {server_url}...")
                if driver.check_server_status():
                    print("Server is running and accessible!")
                else:
                    print(f"ERROR: Server is not responding at {server_url}")
            else:
                clear_terminal()
                print("="*60)
                print("ERROR: Invalid choice. Please select 0-15.")
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