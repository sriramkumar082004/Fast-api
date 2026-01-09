import os
from dotenv import load_dotenv
import urllib.parse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Fetch variables
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "Sriram@2004")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "student_db")

# Handle special characters in password
encoded_password = urllib.parse.quote_plus(db_password)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://student_db_qoou_user:D34DjKZetKeIQtMomUabBuLIxjOIFIYx@dpg-d5do7jbuibrs7394m4o0-a/student_db_qoou"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
