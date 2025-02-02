# app/__init__.py

import os
import psycopg2
import dotenv
from glob import glob

dotenv.load_dotenv()  # Now os.getenv() will see any vars defined in .env

DATABASE_URL = os.getenv("DATABASE_URL")


def run_migrations():
    """
    Connects to the DB, creates a 'schema_migrations' tracking table (if needed),
    and applies any new .sql files in the 'migrations/' folder.
    """
    # 1. Connect to the database
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True  # Auto-commit each statement
    cur = conn.cursor()

    # 2. Ensure the schema_migrations table exists
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS schema_migrations (
        id SERIAL PRIMARY KEY,
        file_name VARCHAR(255) NOT NULL,
        applied_at TIMESTAMP NOT NULL DEFAULT NOW()
    );
    """
    cur.execute(create_table_sql)

    # 3. Get a set of already applied migration filenames
    cur.execute("SELECT file_name FROM schema_migrations;")
    applied_files = {row[0] for row in cur.fetchall()}

    # 4. Find all SQL files in 'migrations' folder
    migrations_path = os.path.join(os.path.dirname(__file__), "migrations", "*.sql")
    migration_files = sorted(glob(migrations_path))  # sorted so we apply in order (001, 002, etc.)

    # 5. Apply each migration if not applied yet
    for file_path in migration_files:
        file_name = os.path.basename(file_path)
        if file_name not in applied_files:
            with open(file_path, "r", encoding="utf-8") as f:
                sql_script = f.read()

            # Execute the SQL script
            cur.execute(sql_script)

            # Record that we've applied this migration
            cur.execute(
                "INSERT INTO schema_migrations (file_name) VALUES (%s)",
                (file_name,),
            )
            print(f"[MIGRATIONS] Applied: {file_name}")

    # 6. Clean up
    cur.close()
    conn.close()


# 7. Run migrations automatically on import
run_migrations()
