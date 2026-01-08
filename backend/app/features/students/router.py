from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ... import schemas, crud, models
from ...database import get_db
from ..auth.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=schemas.StudentResponse)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_student(db, student, user_id=current_user.id)


@router.get("/", response_model=list[schemas.StudentResponse])
def read_students(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_students(db, user_id=current_user.id)


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.delete_student(db, student_id, user_id=current_user.id)


@router.put("/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.update_student(db, student_id, student, user_id=current_user.id)
