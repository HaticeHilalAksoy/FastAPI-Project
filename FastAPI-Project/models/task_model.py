from database.connection import execute_query

def create_tasks_table():
    query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        date DATE NOT NULL,
        duration INTEGER NOT NULL,
        is_completed BOOLEAN NOT NULL DEFAULT 0,
        reminder_time TIME,
        is_notified BOOLEAN NOT NULL DEFAULT 0
    )
    """
    execute_query(query)

def add_is_notified_column():
    query = "ALTER TABLE tasks ADD COLUMN is_notified BOOLEAN NOT NULL DEFAULT 0"
    try:
        execute_query(query)
    except Exception as e:
        print(f"Sütun zaten mevcut: {e}")
