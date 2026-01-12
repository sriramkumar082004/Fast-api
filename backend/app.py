from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import models
from database.db_connect import engine

# Import Routers from Routes
from routes.auth_routes import router as auth_router
from routes.aadhaar_routes import router as aadhaar_router
from routes.student_routes import router as students_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://react-vite-deploy-murex-gamma.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
