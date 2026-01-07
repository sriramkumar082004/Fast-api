import uvicorn
import sys
import os

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting debug server on port 8001...")
    # Run without reload to capture output more easily in this script context if needed,
    # but reload=False is safer for a one-off debug script.
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, log_level="debug")
