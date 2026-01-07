import sys
import os
from sqlalchemy import text

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal, db_name, db_host, db_port
from app.models import User


def check_db():
    print("Checking database connection...")
    try:
        # Check connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Connection successful: {result.scalar()}")

            # Check tables
            print("\nChecking tables...")
            result = connection.execute(
                text(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
                )
            )
            tables = [row[0] for row in result]
            print(f"Tables found: {tables}")

            if "users" in tables:
                # Check users count
                result = connection.execute(text("SELECT COUNT(*) FROM users"))
                count = result.scalar()
                print(f"User count in raw SQL: {count}")

        # Check via ORM
        print("\nChecking via ORM...")
        db = SessionLocal()
        try:
            users = db.query(User).all()
            print(f"Total Users: {len(users)}")
            for u in users:
                print(f" - {u.email} (ID: {u.id})")

            target_email = "govind23@gmail.com"
            target_user = db.query(User).filter(User.email == target_email).first()
            if target_user:
                print(
                    f"\nSUCCESS: User '{target_email}' FOUND in database '{db_name}' at '{db_host}'."
                )
            else:
                print(
                    f"\nFAILURE: User '{target_email}' NOT found in database '{db_name}'."
                )

        finally:
            db.close()

    except Exception as e:
        print(f"Database Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    check_db()
