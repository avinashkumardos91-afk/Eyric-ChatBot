import requests
import json

URL = "http://localhost:5000/login"

def test_login(username, password):
    payload = {"username": username, "password": password}
    response = requests.post(URL, json=payload)
    print(f"Testing {username}:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 30)

if __name__ == "__main__":
    print("Sending login requests to backend...")
    # Test valid login
    test_login("admin", "password123")
    # Test invalid login
    test_login("user", "wrongpassword")
    # Test missing fields
    response = requests.post(URL, json={})
    print(f"Testing missing fields:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
