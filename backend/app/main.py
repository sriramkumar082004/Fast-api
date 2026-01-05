from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://react-vite-deploy-umber-psi.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {"message": "API is running"}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)


@app.get("/students", response_model=list[schemas.StudentResponse])
def read_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return crud.delete_student(db, student_id)


@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int, student: schemas.StudentCreate, db: Session = Depends(get_db)
):
    db_student = (
        db.query(models.Student).filter(models.Student.id == student_id).first()
    )
    if not db_student:
        return None

    db_student.name = student.name
    db_student.email = student.email
    db_student.age = student.age

    db.commit()
    db.refresh(db_student)
    return db_student
