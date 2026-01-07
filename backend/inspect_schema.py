from sqlalchemy import text
from app.database import engine


def inspect_columns():
    with engine.connect() as connection:
        result = connection.execute(
            text(
                "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'students';"
            )
        )
        columns = result.fetchall()
        print("Columns in 'students' table:")
        for col in columns:
            print(f"- {col[0]} ({col[1]})")


if __name__ == "__main__":
    inspect_columns()
