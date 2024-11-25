from database.connection import execute_query

def create_tables():
    query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        duration INTEGER NOT NULL,
        is_completed BOOLEAN NOT NULL DEFAULT 0
    )
    """
    execute_query(query)
    print("Tablolar başarıyla oluşturuldu!")

if __name__ == "__main__":
    create_tables()
