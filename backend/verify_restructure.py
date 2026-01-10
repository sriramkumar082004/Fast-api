import requests
import sys

BASE_URL = "http://127.0.0.1:8000"
EMAIL = "test_restructure@example.com"
PASSWORD = "password123"


def main():
    print(f"Verifying API at {BASE_URL}")

    # 1. Register
    print("[1] Registering...")
    resp = requests.post(
        f"{BASE_URL}/register",
        json={"email": EMAIL, "password": PASSWORD, "full_name": "Restructure Test"},
    )
    if resp.status_code == 200 or (
        resp.status_code == 400 and "already registered" in resp.text
    ):
        print("Registration OK")
    else:
        print(f"Registration Failed: {resp.status_code} {resp.text}")
        sys.exit(1)

    # 2. Login
    print("[2] Logging in...")
    resp = requests.post(
        f"{BASE_URL}/login", json={"email": EMAIL, "password": PASSWORD}
    )
    if resp.status_code != 200:
        print(f"Login Failed: {resp.status_code} {resp.text}")
        sys.exit(1)

    token = resp.json().get("access_token")
    print("Login OK")

    # 3. Create Student
    print("[3] Creating Student...")
    headers = {"Authorization": f"Bearer {token}"}
    student_data = {
        "name": "Restructure Student",
        "age": 22,
        "course": "IT",
        "aadhaar_number": "998877665544",
        "dob": "2002-02-02",
        "address": "456 Avenue",
        "gender": "Female",
    }
    resp = requests.post(f"{BASE_URL}/students/", json=student_data, headers=headers)
    if resp.status_code == 200:
        print("Create Student OK")
        print(resp.json())
    else:
        print(f"Create Student Failed: {resp.status_code} {resp.text}")


if __name__ == "__main__":
    main()
