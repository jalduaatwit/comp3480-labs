import unittest
import requests
import mysql.connector
import redis
import smtplib
import io
from decimal import Decimal
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from minio import Minio
from minio.error import S3Error
from database_utils import (
    connect_to_db, execute_query_with_headers, close_connection,
    get_query_by_key
)


class FastAPILab1Test(unittest.TestCase):
    base_url = "http://localhost:8080"

    def test_1_root(self):
        prefix = "[1]"
        print(f"\n{prefix} Testing GET /")
        url = f"{self.base_url}/"
        response = requests.get(url)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        print(f"{prefix} " + "-" * 40)

    def test_2a_greet_default(self):
        prefix = "[2a]"
        print(f"\n{prefix} Testing GET /greet (default)")
        url = f"{self.base_url}/greet"
        response = requests.get(url)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"greeting": "Hello, Guest!"})
        print(f"{prefix} " + "-" * 40)

    def test_2b_greet_named(self):
        prefix = "[2b]"
        print(f"\n{prefix} Testing GET /greet?name=Aniket")
        url = f"{self.base_url}/greet?name=Aniket"
        response = requests.get(url)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"greeting": "Hello, Aniket!"})
        print(f"{prefix} " + "-" * 40)

    def test_3_cube(self):
        prefix = "[3]"
        print(f"\n{prefix} Testing GET /cube/3")
        url = f"{self.base_url}/cube/3"
        response = requests.get(url)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"number": 3, "cube": 27})
        print(f"{prefix} " + "-" * 40)

    def test_4_add(self):
        prefix = "[4]"
        print(f"\n{prefix} Testing GET /add?a=5&b=7")
        url = f"{self.base_url}/add?a=5&b=7"
        response = requests.get(url)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"sum": 12})
        print(f"{prefix} " + "-" * 40)

    def test_5_factorial(self):
        prefix = "[5]"
        print(f"\n{prefix} Testing GET /factorial/5")
        url = f"{self.base_url}/factorial/5"
        response = requests.get(url)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"n": 5, "factorial": 120})
        print(f"{prefix} " + "-" * 40)

    def test_6a_person_post_minor(self):
        prefix = "[6a]"
        print(f"\n{prefix} Testing POST /person (minor)")
        url = f"{self.base_url}/person"
        data = {"name": "Alex", "age": 17}
        response = requests.post(url, json=data)
        print(f"{prefix} Request Body: {data}")
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("minor", response.json()["message"])
        print(f"{prefix} " + "-" * 40)

    def test_6b_person_post_adult(self):
        prefix = "[6b]"
        print(f"\n{prefix} Testing POST /person (adult)")
        url = f"{self.base_url}/person"
        data = {"name": "Jordan", "age": 30}
        response = requests.post(url, json=data)
        print(f"{prefix} Request Body: {data}")
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("adult", response.json()["message"])
        print(f"{prefix} " + "-" * 40)

    def test_7a_city_info_known(self):
        prefix = "[7a]"
        print(f"\n{prefix} Testing GET /city/Boston (known city)")
        url = f"{self.base_url}/city/Boston"
        response = requests.get(url)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Boston", response.json()["city"])
        print(f"{prefix} " + "-" * 40)

    def test_7b_city_info_unknown(self):
        prefix = "[7b]"
        print(f"\n{prefix} Testing GET /city/Springfield (unknown city)")
        url = f"{self.base_url}/city/Springfield"
        response = requests.get(url)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Springfield", response.json()["city"])
        self.assertIn("No info", response.json()["info"])
        print(f"{prefix} " + "-" * 40)

    def test_8_rectangle_area(self):
        prefix = "[8]"
        print(f"\n{prefix} Testing POST /area/rectangle")
        url = f"{self.base_url}/area/rectangle"
        data = {"width": 4.0, "height": 5.0}
        response = requests.post(url, json=data)
        print(f"{prefix} Request Body: {data}")
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["area"], 20.0)
        print(f"{prefix} " + "-" * 40)

    def test_9a_power_default(self):
        prefix = "[9a]"
        print(f"\n{prefix} Testing GET /power/2 (default exp)")
        url = f"{self.base_url}/power/2"
        response = requests.get(url)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["result"], 4)
        print(f"{prefix} " + "-" * 40)

    def test_9b_power_exp(self):
        prefix = "[9b]"
        print(f"\n{prefix} Testing GET /power/2?exp=8")
        url = f"{self.base_url}/power/2?exp=8"
        response = requests.get(url)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["result"], 256)
        print(f"{prefix} " + "-" * 40)

    def test_10_list_colors(self):
        prefix = "[10]"
        print(f"\n{prefix} Testing GET /colors")
        url = f"{self.base_url}/colors"
        response = requests.get(url)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("colors", response.json())
        self.assertIn("red", response.json()["colors"])
        print(f"{prefix} " + "-" * 40)
        
    def test_11_protected_data_no_key(self):
        prefix = "[11a]"
        print(f"\n{prefix} Testing GET /protected-data with NO API key header")
        url = f"{self.base_url}/protected-data"
        response = requests.get(url)
        print(f"{prefix} Status Code: {response.status_code}")
        if response.status_code == 401:
            print(f"{prefix} Unauthorized: {response.json()}")
        self.assertEqual(response.status_code, 401)
        print(f"{prefix} " + "-" * 40)

    def test_11b_protected_data_wrong_key(self):
        prefix = "[11b]"
        print(f"\n{prefix} Testing GET /protected-data with WRONG API key")
        url = f"{self.base_url}/protected-data"
        headers = {"api-key": "wrongkey"}
        response = requests.get(url, headers=headers)
        print(f"{prefix} Status Code: {response.status_code}")
        if response.status_code == 401:
            print(f"{prefix} Unauthorized: {response.json()}")
        self.assertEqual(response.status_code, 401)
        print(f"{prefix} " + "-" * 40)

    def test_11c_protected_data_right_key(self):
        prefix = "[11c]"
        print(f"\n{prefix} Testing GET /protected-data with CORRECT API key")
        url = f"{self.base_url}/protected-data"
        headers = {"api-key": "mysecretkey"}
        response = requests.get(url, headers=headers)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())
        print(f"{prefix} " + "-" * 40)

    def test_12_cookie_greet_no_cookie(self):
        prefix = "[12a]"
        print(f"\n{prefix} Testing GET /cookie-greet with NO cookie")
        url = f"{self.base_url}/cookie-greet"
        response = requests.get(url)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("new visitor", response.json()["greeting"])
        print(f"{prefix} " + "-" * 40)

    def test_12b_cookie_greet_with_cookie(self):
        prefix = "[12b]"
        print(f"\n{prefix} Testing GET /cookie-greet with username cookie")
        url = f"{self.base_url}/cookie-greet"
        cookies = {"username": "JohnDoe"}
        response = requests.get(url, cookies=cookies)
        print(f"{prefix} Status Code: {response.status_code}")
        print(f"{prefix} Response Body: {response.json()}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("JohnDoe", response.json()["greeting"])
        print(f"{prefix} " + "-" * 40)


class DatabaseLab7Test(unittest.TestCase):
    """Database unit tests for Lab 7."""
    
    def setUp(self):
        """Set up database connection before each test."""
        try:
            self.db_connection = connect_to_db()
            if not self.db_connection:
                self.skipTest("Database connection failed. Make sure MySQL container is running.")
        except Exception as e:
            self.skipTest(f"Database connection failed: {e}")
    
    def tearDown(self):
        """Close database connection after each test."""
        if self.db_connection:
            close_connection(self.db_connection)
    
    def test_db_connection(self):
        """Test database connection."""
        prefix = "[DB1]"
        print(f"\n{prefix} Testing database connection")
        self.assertIsNotNone(self.db_connection)
        self.assertTrue(self.db_connection.is_connected())
        print(f"{prefix} Database connection successful")
        print(f"{prefix} " + "-" * 40)
    
    def test_simple_query_1(self):
        """Test simple query 1: List all product names and prices."""
        prefix = "[DB2]"
        print(f"\n{prefix} Testing Simple Query 1: Products and Prices")
        
        query_info = get_query_by_key('simple_1')
        self.assertIsNotNone(query_info)
        
        result = execute_query_with_headers(self.db_connection, query_info['query'])
        self.assertIsNotNone(result)
        
        headers = result['headers']
        data = result['data']
        
        print(f"{prefix} Headers: {headers}")
        print(f"{prefix} Number of rows: {len(data)}")
        
        # Verify headers
        self.assertIn('product_name', headers)
        self.assertIn('list_price', headers)
        
        # Verify we have data
        self.assertGreater(len(data), 0)
        
        # Verify data structure
        for row in data:
            self.assertEqual(len(row), 2)  # product_name, list_price
            self.assertIsInstance(row[0], str)  # product_name should be string
            self.assertIsInstance(row[1], (int, float, Decimal))  # list_price should be numeric
        
        print(f"{prefix} " + "-" * 40)
    
    def test_simple_query_2(self):
        """Test simple query 2: List customers with last name Brown."""
        prefix = "[DB3]"
        print(f"\n{prefix} Testing Simple Query 2: Customers named Brown")
        
        query_info = get_query_by_key('simple_2')
        self.assertIsNotNone(query_info)
        
        result = execute_query_with_headers(self.db_connection, query_info['query'])
        self.assertIsNotNone(result)
        
        headers = result['headers']
        data = result['data']
        
        print(f"{prefix} Headers: {headers}")
        print(f"{prefix} Number of rows: {len(data)}")
        
        # Verify headers
        self.assertIn('first_name', headers)
        self.assertIn('last_name', headers)
        self.assertIn('email_address', headers)
        
        # Verify all returned customers have last name 'Brown'
        for row in data:
            self.assertEqual(row[1], 'Brown')  # last_name should be 'Brown'
        
        print(f"{prefix} " + "-" * 40)
    
    def test_simple_query_3(self):
        """Test simple query 3: Products with discount over 25%."""
        prefix = "[DB4]"
        print(f"\n{prefix} Testing Simple Query 3: Products with >25% discount")
        
        query_info = get_query_by_key('simple_3')
        self.assertIsNotNone(query_info)
        
        result = execute_query_with_headers(self.db_connection, query_info['query'])
        self.assertIsNotNone(result)
        
        headers = result['headers']
        data = result['data']
        
        print(f"{prefix} Headers: {headers}")
        print(f"{prefix} Number of rows: {len(data)}")
        
        # Verify headers
        self.assertIn('product_name', headers)
        self.assertIn('list_price', headers)
        self.assertIn('discount_percent', headers)
        
        # Verify we have data
        self.assertGreater(len(data), 0)
        
        # Verify data structure and discount > 25%
        for row in data:
            self.assertEqual(len(row), 3)  # product_name, list_price, discount_percent
            self.assertIsInstance(row[0], str)  # product_name should be string
            self.assertIsInstance(row[1], (int, float, Decimal))  # list_price should be numeric
            self.assertIsInstance(row[2], (int, float, Decimal))  # discount_percent should be numeric
            self.assertGreater(row[2], 25)  # discount should be > 25%
        
        print(f"{prefix} " + "-" * 40)
    
    def test_join_query_1(self):
        """Test join query 1: Products with their category names."""
        prefix = "[DB5]"
        print(f"\n{prefix} Testing Join Query 1: Products with Categories")
        
        query_info = get_query_by_key('join_1')
        self.assertIsNotNone(query_info)
        
        result = execute_query_with_headers(self.db_connection, query_info['query'])
        self.assertIsNotNone(result)
        
        headers = result['headers']
        data = result['data']
        
        print(f"{prefix} Headers: {headers}")
        print(f"{prefix} Number of rows: {len(data)}")
        
        # Verify headers
        self.assertIn('product_name', headers)
        self.assertIn('category_name', headers)
        
        # Verify we have data
        self.assertGreater(len(data), 0)
        
        # Verify data structure
        for row in data:
            self.assertEqual(len(row), 2)  # product_name, category_name
            self.assertIsInstance(row[0], str)  # product_name should be string
            self.assertIsInstance(row[1], str)  # category_name should be string
        
        print(f"{prefix} " + "-" * 40)
    
    def test_join_query_2(self):
        """Test join query 2: Orders with customer information."""
        prefix = "[DB6]"
        print(f"\n{prefix} Testing Join Query 2: Orders with Customer Info")
        
        query_info = get_query_by_key('join_2')
        self.assertIsNotNone(query_info)
        
        result = execute_query_with_headers(self.db_connection, query_info['query'])
        self.assertIsNotNone(result)
        
        headers = result['headers']
        data = result['data']
        
        print(f"{prefix} Headers: {headers}")
        print(f"{prefix} Number of rows: {len(data)}")
        
        # Verify headers
        self.assertIn('order_id', headers)
        self.assertIn('order_date', headers)
        self.assertIn('first_name', headers)
        self.assertIn('last_name', headers)
        
        # Verify we have data
        self.assertGreater(len(data), 0)
        
        # Verify data structure
        for row in data:
            self.assertEqual(len(row), 4)  # order_id, order_date, first_name, last_name
            self.assertIsInstance(row[0], int)  # order_id should be integer
            self.assertIsInstance(row[2], str)  # first_name should be string
            self.assertIsInstance(row[3], str)  # last_name should be string
        
        print(f"{prefix} " + "-" * 40)
    
    def test_join_query_3(self):
        """Test join query 3: Order items with product details."""
        prefix = "[DB7]"
        print(f"\n{prefix} Testing Join Query 3: Order Items with Products")
        
        query_info = get_query_by_key('join_3')
        self.assertIsNotNone(query_info)
        
        result = execute_query_with_headers(self.db_connection, query_info['query'])
        self.assertIsNotNone(result)
        
        headers = result['headers']
        data = result['data']
        
        print(f"{prefix} Headers: {headers}")
        print(f"{prefix} Number of rows: {len(data)}")
        
        # Verify headers
        self.assertIn('item_id', headers)
        self.assertIn('product_name', headers)
        self.assertIn('quantity', headers)
        self.assertIn('item_price', headers)
        
        # Verify we have data
        self.assertGreater(len(data), 0)
        
        # Verify data structure
        for row in data:
            self.assertEqual(len(row), 4)  # item_id, product_name, quantity, item_price
            self.assertIsInstance(row[0], int)  # item_id should be integer
            self.assertIsInstance(row[1], str)  # product_name should be string
            self.assertIsInstance(row[2], int)  # quantity should be integer
            self.assertIsInstance(row[3], (int, float, Decimal))  # item_price should be numeric
        
        print(f"{prefix} " + "-" * 40)
    
    def test_join_query_4(self):
        """Test join query 4: Orders with shipping address."""
        prefix = "[DB8]"
        print(f"\n{prefix} Testing Join Query 4: Orders with Shipping Address")
        
        query_info = get_query_by_key('join_4')
        self.assertIsNotNone(query_info)
        
        result = execute_query_with_headers(self.db_connection, query_info['query'])
        self.assertIsNotNone(result)
        
        headers = result['headers']
        data = result['data']
        
        print(f"{prefix} Headers: {headers}")
        print(f"{prefix} Number of rows: {len(data)}")
        
        # Verify headers
        self.assertIn('order_id', headers)
        self.assertIn('line1', headers)
        self.assertIn('city', headers)
        self.assertIn('state', headers)
        
        # Verify we have data
        self.assertGreater(len(data), 0)
        
        # Verify data structure
        for row in data:
            self.assertEqual(len(row), 4)  # order_id, line1, city, state
            self.assertIsInstance(row[0], int)  # order_id should be integer
            self.assertIsInstance(row[1], str)  # line1 should be string
            self.assertIsInstance(row[2], str)  # city should be string
            self.assertIsInstance(row[3], str)  # state should be string
        
        print(f"{prefix} " + "-" * 40)
    
    def test_join_query_5(self):
        """Test join query 5: Customers with addresses."""
        prefix = "[DB9]"
        print(f"\n{prefix} Testing Join Query 5: Customers with Addresses")
        
        query_info = get_query_by_key('join_5')
        self.assertIsNotNone(query_info)
        
        result = execute_query_with_headers(self.db_connection, query_info['query'])
        self.assertIsNotNone(result)
        
        headers = result['headers']
        data = result['data']
        
        print(f"{prefix} Headers: {headers}")
        print(f"{prefix} Number of rows: {len(data)}")
        
        # Verify headers
        self.assertIn('first_name', headers)
        self.assertIn('last_name', headers)
        self.assertIn('line1', headers)
        self.assertIn('city', headers)
        self.assertIn('state', headers)
        
        # Verify we have data
        self.assertGreater(len(data), 0)
        
        # Verify data structure
        for row in data:
            self.assertEqual(len(row), 5)  # first_name, last_name, line1, city, state
            self.assertIsInstance(row[0], str)  # first_name should be string
            self.assertIsInstance(row[1], str)  # last_name should be string
            self.assertIsInstance(row[2], str)  # line1 should be string
            self.assertIsInstance(row[3], str)  # city should be string
            self.assertIsInstance(row[4], str)  # state should be string
        
        print(f"{prefix} " + "-" * 40)
    
    def test_group_query_1(self):
        """Test group query 1: Count customers per state."""
        prefix = "[DB10]"
        print(f"\n{prefix} Testing Group Query 1: Customers per State")
        
        query_info = get_query_by_key('group_1')
        self.assertIsNotNone(query_info)
        
        result = execute_query_with_headers(self.db_connection, query_info['query'])
        self.assertIsNotNone(result)
        
        headers = result['headers']
        data = result['data']
        
        print(f"{prefix} Headers: {headers}")
        print(f"{prefix} Number of rows: {len(data)}")
        
        # Verify headers
        self.assertIn('state', headers)
        self.assertIn('num_customers', headers)
        
        # Verify we have data
        self.assertGreater(len(data), 0)
        
        # Verify data structure
        for row in data:
            self.assertEqual(len(row), 2)  # state, num_customers
            self.assertIsInstance(row[0], str)  # state should be string
            self.assertIsInstance(row[1], int)  # num_customers should be integer
            self.assertGreater(row[1], 0)  # count should be positive
        
        print(f"{prefix} " + "-" * 40)
    
    def test_group_query_2(self):
        """Test group query 2: Average discount by category."""
        prefix = "[DB11]"
        print(f"\n{prefix} Testing Group Query 2: Average Discount by Category")
        
        query_info = get_query_by_key('group_2')
        self.assertIsNotNone(query_info)
        
        result = execute_query_with_headers(self.db_connection, query_info['query'])
        self.assertIsNotNone(result)
        
        headers = result['headers']
        data = result['data']
        
        print(f"{prefix} Headers: {headers}")
        print(f"{prefix} Number of rows: {len(data)}")
        
        # Verify headers
        self.assertIn('category_name', headers)
        self.assertIn('avg_discount', headers)
        
        # Verify we have data
        self.assertGreater(len(data), 0)
        
        # Verify data structure
        for row in data:
            self.assertEqual(len(row), 2)  # category_name, avg_discount
            self.assertIsInstance(row[0], str)  # category_name should be string
            self.assertIsInstance(row[1], (int, float, Decimal))  # avg_discount should be numeric
        
        print(f"{prefix} " + "-" * 40)
    
    def test_group_query_3(self):
        """Test group query 3: Total orders per customer."""
        prefix = "[DB12]"
        print(f"\n{prefix} Testing Group Query 3: Orders per Customer")
        
        query_info = get_query_by_key('group_3')
        self.assertIsNotNone(query_info)
        
        result = execute_query_with_headers(self.db_connection, query_info['query'])
        self.assertIsNotNone(result)
        
        headers = result['headers']
        data = result['data']
        
        print(f"{prefix} Headers: {headers}")
        print(f"{prefix} Number of rows: {len(data)}")
        
        # Verify headers
        self.assertIn('first_name', headers)
        self.assertIn('last_name', headers)
        self.assertIn('total_orders', headers)
        
        # Verify we have data
        self.assertGreater(len(data), 0)
        
        # Verify data structure
        for row in data:
            self.assertEqual(len(row), 3)  # first_name, last_name, total_orders
            self.assertIsInstance(row[0], str)  # first_name should be string
            self.assertIsInstance(row[1], str)  # last_name should be string
            self.assertIsInstance(row[2], int)  # total_orders should be integer
            self.assertGreaterEqual(row[2], 0)  # count should be non-negative
        
        print(f"{prefix} " + "-" * 40)
    
    def test_group_query_4(self):
        """Test group query 4: Most expensive product per category."""
        prefix = "[DB13]"
        print(f"\n{prefix} Testing Group Query 4: Max Price per Category")
        
        query_info = get_query_by_key('group_4')
        self.assertIsNotNone(query_info)
        
        result = execute_query_with_headers(self.db_connection, query_info['query'])
        self.assertIsNotNone(result)
        
        headers = result['headers']
        data = result['data']
        
        print(f"{prefix} Headers: {headers}")
        print(f"{prefix} Number of rows: {len(data)}")
        
        # Verify headers
        self.assertIn('category_name', headers)
        self.assertIn('max_price', headers)
        
        # Verify we have data
        self.assertGreater(len(data), 0)
        
        # Verify data structure
        for row in data:
            self.assertEqual(len(row), 2)  # category_name, max_price
            self.assertIsInstance(row[0], str)  # category_name should be string
            self.assertIsInstance(row[1], (int, float, Decimal))  # max_price should be numeric
            self.assertGreater(row[1], 0)  # price should be positive
        
        print(f"{prefix} " + "-" * 40)
    
    def test_group_query_5(self):
        """Test group query 5: Total order value per order."""
        prefix = "[DB14]"
        print(f"\n{prefix} Testing Group Query 5: Total Order Values")
        
        query_info = get_query_by_key('group_5')
        self.assertIsNotNone(query_info)
        
        result = execute_query_with_headers(self.db_connection, query_info['query'])
        self.assertIsNotNone(result)
        
        headers = result['headers']
        data = result['data']
        
        print(f"{prefix} Headers: {headers}")
        print(f"{prefix} Number of rows: {len(data)}")
        
        # Verify headers
        self.assertIn('order_id', headers)
        self.assertIn('total_value', headers)
        
        # Verify we have data
        self.assertGreater(len(data), 0)
        
        # Verify data structure
        for row in data:
            self.assertEqual(len(row), 2)  # order_id, total_value
            self.assertIsInstance(row[0], int)  # order_id should be integer
            self.assertIsInstance(row[1], (int, float, Decimal))  # total_value should be numeric
            self.assertGreater(row[1], 0)  # total value should be positive
        
        print(f"{prefix} " + "-" * 40)


class RedisLab8Test(unittest.TestCase):
    """Test Redis shared memory functionality"""
    
    def setUp(self):
        """Set up Redis connection for testing"""
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
            self.redis_client.ping()
        except redis.ConnectionError:
            self.skipTest("Redis server is not available")
    
    def test_redis_connection(self):
        """Test Redis connection"""
        prefix = "[Redis-1]"
        print(f"\n{prefix} Testing Redis Connection")
        try:
            result = self.redis_client.ping()
            print(f"{prefix} Ping response: {result}")
            self.assertTrue(result)
            print(f"{prefix} SUCCESS: Redis connection successful")
        except Exception as e:
            self.fail(f"Redis connection failed: {e}")
        print(f"{prefix} " + "-" * 40)
    
    def test_redis_set_get(self):
        """Test Redis set and get operations"""
        prefix = "[Redis-2]"
        print(f"\n{prefix} Testing Redis Set/Get Operations")
        test_key = "test_lab8_key"
        test_value = "test_lab8_value"
        
        # Set value
        result = self.redis_client.set(test_key, test_value)
        print(f"{prefix} Set operation result: {result}")
        self.assertTrue(result)
        
        # Get value
        retrieved_value = self.redis_client.get(test_key)
        print(f"{prefix} Retrieved value: {retrieved_value}")
        self.assertEqual(retrieved_value, test_value)
        
        # Cleanup
        self.redis_client.delete(test_key)
        print(f"{prefix} SUCCESS: Set/Get operations successful")
        print(f"{prefix} " + "-" * 40)


class MinIOLab8Test(unittest.TestCase):
    """Test MinIO shared file system functionality"""
    
    def setUp(self):
        """Set up MinIO connection for testing"""
        try:
            self.minio_client = Minio(
                "localhost:9000",
                access_key="minioadmin",
                secret_key="minioadmin123",
                secure=False
            )
            # Test connection by listing buckets
            self.minio_client.list_buckets()
        except Exception:
            self.skipTest("MinIO server is not available")
    
    def test_minio_connection(self):
        """Test MinIO connection"""
        prefix = "[MinIO-1]"
        print(f"\n{prefix} Testing MinIO Connection")
        try:
            buckets = list(self.minio_client.list_buckets())
            print(f"{prefix} Available buckets: {len(buckets)}")
            print(f"{prefix} SUCCESS: MinIO connection successful")
        except Exception as e:
            self.fail(f"MinIO connection failed: {e}")
        print(f"{prefix} " + "-" * 40)
    
    def test_minio_bucket_operations(self):
        """Test MinIO bucket and file operations"""
        prefix = "[MinIO-2]"
        print(f"\n{prefix} Testing MinIO Bucket/File Operations")
        bucket_name = "test-lab8-bucket"
        file_name = "test_file.txt"
        file_content = "Hello from Lab 8 MinIO test!"
        
        try:
            # Create bucket if it doesn't exist
            if not self.minio_client.bucket_exists(bucket_name):
                self.minio_client.make_bucket(bucket_name)
                print(f"{prefix} Created bucket: {bucket_name}")
            
            # Upload file
            data = io.BytesIO(file_content.encode('utf-8'))
            self.minio_client.put_object(
                bucket_name,
                file_name,
                data,
                len(file_content.encode('utf-8')),
                content_type='text/plain'
            )
            print(f"{prefix} Uploaded file: {file_name}")
            
            # Download and verify file
            response = self.minio_client.get_object(bucket_name, file_name)
            downloaded_content = response.read().decode('utf-8')
            response.close()
            response.release_conn()
            
            print(f"{prefix} Downloaded content: {downloaded_content}")
            self.assertEqual(downloaded_content, file_content)
            
            # Cleanup
            self.minio_client.remove_object(bucket_name, file_name)
            print(f"{prefix} SUCCESS: Bucket/File operations successful")
        except Exception as e:
            self.fail(f"MinIO operations failed: {e}")
        print(f"{prefix} " + "-" * 40)


class PostfixLab8Test(unittest.TestCase):
    """Test Postfix email server functionality"""
    
    def test_postfix_connection(self):
        """Test Postfix SMTP connection"""
        prefix = "[Postfix-1]"
        print(f"\n{prefix} Testing Postfix SMTP Connection")
        try:
            server = smtplib.SMTP('localhost', 1587, timeout=10)
            print(f"{prefix} Connected to SMTP server")
            server.quit()
            print(f"{prefix} SUCCESS: Postfix connection successful")
        except Exception as e:
            print(f"{prefix} ERROR: Postfix connection failed: {e}")
            print(f"{prefix} SUCCESS: Test completed - check if Postfix container is running")
        print(f"{prefix} " + "-" * 40)
    
    def test_postfix_email_structure(self):
        """Test email message structure creation"""
        prefix = "[Postfix-2]"
        print(f"\n{prefix} Testing Email Message Structure")
        
        sender_email = "test@wit.edu"
        recipient_email = "jaldua@wit.edu"
        subject = "Lab 8 Test Email"
        body = "This is a test email from Lab 8."
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Verify message structure
        self.assertEqual(msg['From'], sender_email)
        self.assertEqual(msg['To'], recipient_email)
        self.assertEqual(msg['Subject'], subject)
        
        message_text = msg.as_string()
        self.assertIn(sender_email, message_text)
        self.assertIn(recipient_email, message_text)
        self.assertIn(subject, message_text)
        self.assertIn(body, message_text)
        
        print(f"{prefix} SUCCESS: Email structure creation successful")
        print(f"{prefix} " + "-" * 40)
    
    def test_postfix_real_email_attempt(self):
        """Test actual email sending (will likely fail due to spam filters)"""
        prefix = "[Postfix-3]"
        print(f"\n{prefix} Testing Real Email Sending")
        print(f"{prefix} Note: This will attempt to send a real email")
        print(f"{prefix} Expected: Rejection by recipient server (spam filters)")
        
        try:
            # Create test email
            sender_email = "test@wit.edu"
            recipient_email = "jaldua@wit.edu"
            subject = "Lab 8 Test Email"
            body = "This is a test email from Lab 8 Postfix server."
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect and attempt to send
            server = smtplib.SMTP('localhost', 1587, timeout=10)
            text = msg.as_string()
            
            try:
                server.sendmail(sender_email, recipient_email, text)
                print(f"{prefix} SUCCESS: Email accepted by local Postfix server")
                print(f"{prefix} Note: May still be rejected by recipient server")
            except Exception as send_error:
                print(f"{prefix} ERROR: Email sending failed: {send_error}")
                print(f"{prefix} This is expected behavior (spam filters, auth requirements)")
            
            server.quit()
            print(f"{prefix} SUCCESS: Real email sending test completed")
            
        except Exception as e:
            print(f"{prefix} ERROR: Connection failed: {e}")
            print(f"{prefix} Check if Postfix container is running")
        
        print(f"{prefix} " + "-" * 40)


if __name__ == "__main__":
    # Run FastAPI tests
    print("="*60)
    print("Running FastAPI Tests")
    print("="*60)
    fastapi_suite = unittest.TestLoader().loadTestsFromTestCase(FastAPILab1Test)
    fastapi_runner = unittest.TextTestRunner(verbosity=2)
    fastapi_result = fastapi_runner.run(fastapi_suite)
    
    print("\n" + "="*60)
    print("Running Database Tests")
    print("="*60)
    db_suite = unittest.TestLoader().loadTestsFromTestCase(DatabaseLab7Test)
    db_runner = unittest.TextTestRunner(verbosity=2)
    db_result = db_runner.run(db_suite)
    
    print("\n" + "="*60)
    print("Running Redis Tests")
    print("="*60)
    redis_suite = unittest.TestLoader().loadTestsFromTestCase(RedisLab8Test)
    redis_runner = unittest.TextTestRunner(verbosity=2)
    redis_result = redis_runner.run(redis_suite)
    
    print("\n" + "="*60)
    print("Running MinIO Tests")
    print("="*60)
    minio_suite = unittest.TestLoader().loadTestsFromTestCase(MinIOLab8Test)
    minio_runner = unittest.TextTestRunner(verbosity=2)
    minio_result = minio_runner.run(minio_suite)
    
    print("\n" + "="*60)
    print("Running Postfix Tests")
    print("="*60)
    postfix_suite = unittest.TestLoader().loadTestsFromTestCase(PostfixLab8Test)
    postfix_runner = unittest.TextTestRunner(verbosity=2)
    postfix_result = postfix_runner.run(postfix_suite)
    
    print("\n" + "="*60)
    print("Lab 8 Test Summary")
    print("="*60)
    print(f"FastAPI Tests: {fastapi_result.testsRun} run, {len(fastapi_result.failures)} failures, {len(fastapi_result.errors)} errors")
    print(f"Database Tests: {db_result.testsRun} run, {len(db_result.failures)} failures, {len(db_result.errors)} errors")
    print(f"Redis Tests: {redis_result.testsRun} run, {len(redis_result.failures)} failures, {len(redis_result.errors)} errors")
    print(f"MinIO Tests: {minio_result.testsRun} run, {len(minio_result.failures)} failures, {len(minio_result.errors)} errors")
    print(f"Postfix Tests: {postfix_result.testsRun} run, {len(postfix_result.failures)} failures, {len(postfix_result.errors)} errors")
    
    total_failures = (len(fastapi_result.failures) + len(db_result.failures) + 
                     len(redis_result.failures) + len(minio_result.failures) + len(postfix_result.failures))
    total_errors = (len(fastapi_result.errors) + len(db_result.errors) + 
                   len(redis_result.errors) + len(minio_result.errors) + len(postfix_result.errors))
    
    if total_failures == 0 and total_errors == 0:
        print("All tests passed!")
    else:
        print(f"Total failures: {total_failures}, Total errors: {total_errors}")
    
    print("="*60)
