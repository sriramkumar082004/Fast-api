import sys
import os
from sqlalchemy import text

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine


def view_data():
    print("--- DATABASE CONTENT REPORT ---\n")
    try:
        with engine.connect() as connection:
            # 1. List Tables
            print("1. TABLES IN DATABASE:")
            result = connection.execute(
                text(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
                )
            )
            tables = [row[0] for row in result]
            for t in tables:
                print(f" - {t}")

            print("\n" + "=" * 30 + "\n")

            # 2. Dump Users Table
            if "users" in tables:
                print("2. CONTENT OF 'users' TABLE (Login Credentials):")
                result = connection.execute(
                    text("SELECT id, email, password FROM users")
                )
                rows = result.fetchall()
                if not rows:
                    print("   (Table is empty)")
                else:
                    print(f"   Found {len(rows)} users:")
                    for row in rows:
                        # Mask password for security in output
                        pwd_display = row[2][:10] + "..." if row[2] else "None"
                        print(
                            f"   - ID: {row[0]} | Email: {row[1]} | Password Hash: {pwd_display}"
                        )
            else:
                print("!! 'users' TABLE NOT FOUND !!")

            print("\n" + "=" * 30 + "\n")

            # 3. Dump Students Table
            if "students" in tables:
                print("3. CONTENT OF 'students' TABLE (App Data):")
                result = connection.execute(
                    text("SELECT id, name, email FROM students")
                )
                rows = result.fetchall()
                if not rows:
                    print("   (Table is empty)")
                else:
                    print(f"   Found {len(rows)} students:")
                    for row in rows:
                        print(f"   - ID: {row[0]} | Name: {row[1]} | Email: {row[2]}")
            else:
                print("!! 'students' TABLE NOT FOUND !!")

    except Exception as e:
        print(f"Error reading database: {e}")


if __name__ == "__main__":
    view_data()
