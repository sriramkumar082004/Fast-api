import uvicorn
import sys
import os

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Same as run.py but with explicit logging setup if needed,
    # but run.py already uses uvicorn.run.
    # We will just use this to guarantee we control the execution.
    print("Starting production-like server on 8002...")
    uvicorn.run(
        "app.main:app", host="127.0.0.1", port=8002, reload=False
    )  # Disable reload to be sure
