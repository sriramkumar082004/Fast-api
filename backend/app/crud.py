from sqlalchemy.orm import Session
from . import models, schemas
from .auth import security


def create_student(db: Session, student: schemas.StudentCreate, user_id: int):
    db_student = models.Student(**student.dict(), user_id=user_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_students(db: Session, user_id: int):
    return db.query(models.Student).filter(models.Student.user_id == user_id).all()


def delete_student(db: Session, student_id: int, user_id: int):
    student = (
        db.query(models.Student)
        .filter(models.Student.id == student_id, models.Student.user_id == user_id)
        .first()
    )
    if student:
        db.delete(student)
        db.commit()
    return student


def update_student(
    db: Session, student_id: int, student: schemas.StudentUpdate, user_id: int
):
    db_student = (
        db.query(models.Student)
        .filter(models.Student.id == student_id, models.Student.user_id == user_id)
        .first()
    )
    if db_student:
        db_student.name = student.name
        db_student.age = student.age
        db_student.course = student.course
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.hash_password(user.password)
    db_user = models.User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
