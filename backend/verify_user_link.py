import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def register(email, password):
    response = requests.post(
        f"{BASE_URL}/register", json={"email": email, "password": password}
    )
    if response.status_code != 200:
        print(f"Register failed: {response.status_code} - {response.text}")
    return response


def login(email, password):
    response = requests.post(
        f"{BASE_URL}/login", json={"email": email, "password": password}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    print(f"Login failed: {response.status_code} - {response.text}")
    return None


def create_student(token, name, age, course):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/students",
        json={"name": name, "age": age, "course": course},
        headers=headers,
    )
    if response.status_code != 200:
        print(f"Create student failed: {response.status_code} - {response.text}")
    return response


def get_students(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/students", headers=headers)
    return response


def main():
    # 1. Create Users
    print("--- Registering Users ---")
    reg_a = register("userA@example.com", "password123")
    reg_b = register("userB@example.com", "password123")
    print(f"Register User A: {reg_a.status_code}")
    print(f"Register User B: {reg_b.status_code}")

    # 2. Login
    print("\n--- Logging In ---")
    token_a = login("userA@example.com", "password123")
    token_b = login("userB@example.com", "password123")

    if not token_a or not token_b:
        print("Login failed, exiting.")
        return

    print("Login successful")

    # 3. Create Data for User A
    print("\n--- Creating Student for User A ---")
    create_a = create_student(token_a, "Student A", 20, "CS101")
    print(f"Create Student A: {create_a.status_code} - {create_a.json()}")

    # 4. Create Data for User B
    print("\n--- Creating Student for User B ---")
    create_b = create_student(token_b, "Student B", 22, "BIO101")
    print(f"Create Student B: {create_b.status_code} - {create_b.json()}")

    # 5. Verify Isolation
    print("\n--- Verifying Isolation ---")

    students_a = get_students(token_a).json()
    students_b = get_students(token_b).json()

    print(
        f"User A sees {len(students_a)} student(s): {[s['name'] for s in students_a]}"
    )
    print(
        f"User B sees {len(students_b)} student(s): {[s['name'] for s in students_b]}"
    )

    if (
        len(students_a) == 1
        and students_a[0]["name"] == "Student A"
        and len(students_b) == 1
        and students_b[0]["name"] == "Student B"
    ):
        print("\nSUCCESS: Users see only their own students!")
    else:
        print("\nFAILURE: Data isolation not working correctly.")


if __name__ == "__main__":
    main()
