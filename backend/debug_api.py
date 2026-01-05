import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_api():
    print("Testing API...")

    # 1. Create a student
    student_data = {"name": "Debug User", "email": "debug@example.com", "age": 25}
    print(f"Creating student: {student_data}")
    try:
        response = requests.post(f"{BASE_URL}/students", json=student_data)
        print(f"Create Response [{response.status_code}]: {response.text}")
    except Exception as e:
        print(f"Create failed: {e}")

    # 2. Get students
    print("Fetching students...")
    try:
        response = requests.get(f"{BASE_URL}/students")
        print(f"Get Response [{response.status_code}]: {response.text}")
        students = response.json()
        print(f"Student count: {len(students)}")
        for s in students:
            print(s)
    except Exception as e:
        print(f"Get failed: {e}")


if __name__ == "__main__":
    test_api()
