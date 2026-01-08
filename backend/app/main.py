
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, get_db
from .routes import auth
from .auth.dependencies import get_current_user

from fastapi import FastAPI, UploadFile, File
from .ocr import extract_aadhaar_data
import io
import pytesseract
from PIL import Image

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# main.py in your Backend
origins = [
    "http://localhost:5173",
    "https://react-vite-deploy-eta-cyan.vercel.app",  # Add this one (from screenshot 1)
    "https://react-vite-deploy-murex-gamma.vercel.app",  # Add this one (from screenshot 2)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # OR use ["*"] to allow everyone (easier for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "Aadhar OCR API running successfully 🚀"}

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return {"extracted_text": text}

@app.post("/students", response_model=schemas.StudentResponse)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_student(db, student, user_id=current_user.id)


@app.get("/students", response_model=list[schemas.StudentResponse])
def read_students(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_students(db, user_id=current_user.id)


@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.delete_student(db, student_id, user_id=current_user.id)


@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.update_student(db, student_id, student, user_id=current_user.id)
