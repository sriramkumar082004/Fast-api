from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine

# Import Routers from Features
from .features.auth.router import router as auth_router
from .features.aadhaar.router import router as aadhaar_router
from .features.students.router import router as students_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# main.py in your Backend
origins = [
    "http://localhost:5173",
    "https://react-vite-deploy-murex-gamma.vercel.app",
    "http://localhost:5174",  # Added based on user history context
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # OR use ["*"] to allow everyone (easier for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(aadhaar_router)
app.include_router(students_router, prefix="/students", tags=["students"])


@app.get("/")
def home():
    return {"message": "Aadhar OCR API running successfully 🚀"}
