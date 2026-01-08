import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from backend.app.main import app

    print("Successfully imported app from backend.app.main")
except Exception as e:
    print(f"Error importing app: {e}")
    sys.exit(1)
