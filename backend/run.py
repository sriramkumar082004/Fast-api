import uvicorn
import os

if __name__ == "__main__":
    # Ensure we are running from the backend directory
    # This maps 'app.main' to 'backend/app/main.py'
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


