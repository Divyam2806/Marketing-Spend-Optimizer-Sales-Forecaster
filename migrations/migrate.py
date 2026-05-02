import sqlite3
import os


def run_migrations(db_path='data/marketing.db'):
    """
    Runs all pending SQL migration files in order.
    Tracks applied migrations in a migrations table inside the database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create migrations tracking table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            filename   TEXT NOT NULL UNIQUE,
            applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # Get list of already applied migrations
    applied = {row[0] for row in cursor.execute("SELECT filename FROM migrations")}

    # Get all .sql files in the migrations folder, sorted by name
    migrations_dir = os.path.dirname(__file__)
    sql_files = sorted([
        f for f in os.listdir(migrations_dir)
        if f.endswith('.sql')
    ])

    # Run pending migrations
    for filename in sql_files:
        if filename not in applied:
            filepath = os.path.join(migrations_dir, filename)
            with open(filepath, 'r') as f:
                sql = f.read()
            cursor.executescript(sql)
            cursor.execute("INSERT INTO migrations (filename) VALUES (?)", (filename,))
            conn.commit()
            print(f"   Applied migration: {filename}")
        else:
            print(f"   Skipped (already applied): {filename}")

    conn.close()