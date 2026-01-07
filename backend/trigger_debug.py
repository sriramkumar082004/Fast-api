import requests
import sys

BASE_URL = "http://127.0.0.1:8002"


def trigger_error():
    # 1. Register a user (to ensure it exists)
    email = "govind23@gmail.com"
    password = "govind@23"

    print(f"Registering {email}...")
    try:
        resp = requests.post(
            f"{BASE_URL}/register", json={"email": email, "password": password}
        )
        print(f"Register: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Register failed: {e}")

    # 2. Login (this is where the 500 is reported)
    print(f"Logging in {email}...")
    try:
        resp = requests.post(
            f"{BASE_URL}/login", json={"email": email, "password": password}
        )
        print(f"Login: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Login failed: {e}")


if __name__ == "__main__":
    trigger_error()
