import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect
import urllib.parse

# Load env vars same as database.py
load_dotenv()

db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "Sriram@2004")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "student_db")

# Mask password for output
masked_password = "*****"
if db_password:
    encoded_password = urllib.parse.quote_plus(db_password)
    # Construct URL for display with masked password
    display_url = (
        f"postgresql://{db_user}:{masked_password}@{db_host}:{db_port}/{db_name}"
    )
else:
    display_url = "Password not found in env"

print(f"--- Database Configuration ---")
print(f"HOST: {db_host}")
print(f"PORT: {db_port}")
print(f"DB NAME: {db_name}")
print(f"USER: {db_user}")
print(f"CONNECTION URL (Masked): {display_url}")
print("-" * 30)

# Construct actual URL for connection
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = (
        f"postgresql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    )

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("\nSuccessfully connected to the database!")

        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"\nTables found: {tables}")

        for table in tables:
            try:
                result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                print(f" - Table '{table}': {count} rows")

                if count > 0:
                    print(f"   Sample data from '{table}':")
                    rows = connection.execute(text(f"SELECT * FROM {table} LIMIT 2"))
                    for row in rows:
                        print(f"   {row}")
            except Exception as e:
                print(f"   Error querying table '{table}': {e}")

except Exception as e:
    print(f"\nCRITICAL ERROR: Could not connect to database.\nError: {e}")
