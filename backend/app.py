from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import models
from database.db_connect import engine

# image background removal api 
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import requests


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



APYHUB_API_KEY = "APY0wCGAe7CLWSlBUJVpESby26wVwgrWdvOdzhOJuCFQjBh68xKzNX1cfgPaJw7rznCRZrjW8"
APYHUB_URL = "https://apyhub.com/utility/image-processor-change-background"

@app.post("/change-background")
async def change_background(file: UploadFile = File(...)):
    headers = {
        "apy-token": APYHUB_API_KEY
    }
    
    files = {
        "file": (file.filename, await file.read(), file.content_type)
    }

    data = {
        "background_color": "#FFFFFF"  # white background
    }

    response = requests.post(
        APYHUB_URL,
        headers=headers,
        files=files,
        data=data
    )

    return Response(
        content=response.content,
        media_type="image/png"
    )