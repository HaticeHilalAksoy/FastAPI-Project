import sqlite3

def get_db_connection():
    connection = sqlite3.connect("tasks.db")  # Veritabanı dosyasını oluşturur
    connection.row_factory = sqlite3.Row     # Verileri sözlük formatında döndürür
    return connection

def execute_query(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()
    return cursor
