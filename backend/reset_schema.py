from app.database import engine, Base
from app.models import User, Student

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)
print("Tables dropped.")

print("Recreating tables...")
Base.metadata.create_all(bind=engine)
print("Tables recreated successfully.")
