import unittest
import requests

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

if __name__ == '__main__':
    unittest.main()
