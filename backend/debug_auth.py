import sys
import os

# Add backend directory to sys.path to allow imports from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app import crud, schemas, models
from app.auth import security, jwt


def test_auth():
    print("Testing Auth Components...")

    db = SessionLocal()
    try:
        # 1. Test Password Hashing
        print("\n1. Testing Hashing...")
        pwd = "testpassword"
        hashed = security.hash_password(pwd)
        print(f"Password: {pwd}")
        print(f"Hashed: {hashed}")

        # 2. Test Password Verification
        print("\n2. Testing Verification...")
        is_valid = security.verify_password(pwd, hashed)
        print(f"Verification Result: {is_valid}")

        # 3. Test Token Creation
        print("\n3. Testing Token Creation...")
        token = jwt.create_access_token({"sub": "test@example.com"})
        print(f"Token: {token}")

        # 4. Test User Creation & Retrieval
        print("\n4. Testing DB User Operations...")
        email = "debug_auth@example.com"
        user_in = schemas.UserCreate(email=email, password=pwd)

        # Check if user exists
        user = crud.get_user_by_email(db, email=email)
        if user:
            print(f"User {email} already exists. ID: {user.id}")
        else:
            print(f"Creating user {email}...")
            user = crud.create_user(db, user_in)
            print(f"User created. ID: {user.id}")

        # Verify password in DB
        print(f"Verifying stored password for {email}...")
        is_db_valid = security.verify_password(pwd, user.password)
        print(f"DB Password Valid: {is_db_valid}")

    except Exception as e:
        print(f"\nResource Error: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_auth()
