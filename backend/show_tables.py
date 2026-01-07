from app.database import engine, SessionLocal
from app import models
from sqlalchemy.orm import Session


def show_data():
    db = SessionLocal()

    print("\n--- CONTENT OF USERS TABLE ---")
    users = db.query(models.User).all()
    if not users:
        print("(No users found)")
    for u in users:
        print(
            f"ID: {u.id} | Email: {u.email} | Password: {u.password[:10]}... (hashed)"
        )

    print("\n--- CONTENT OF STUDENTS TABLE ---")
    students = db.query(models.Student).all()
    if not students:
        print("(No students found)")
    for s in students:
        print(
            f"ID: {s.id} | Name: {s.name} | Email: {s.email} | Age: {s.age} | Linked to User ID: {s.user_id}"
        )

    db.close()


if __name__ == "__main__":
    show_data()
