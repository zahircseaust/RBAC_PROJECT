from sqlalchemy import text
from app.database.session import engine

def migrate():
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='sbus' AND column_name='is_deleted'
        """))

        if result.fetchone() is None:
            conn.execute(text(
                "ALTER TABLE sbus ADD COLUMN is_deleted BOOLEAN NOT NULL DEFAULT FALSE"
            ))
            conn.commit()
            print("Column 'is_deleted' added to sbus table")
        else:
            print("Column 'is_deleted' already exists")

if __name__ == "__main__":
    migrate()
