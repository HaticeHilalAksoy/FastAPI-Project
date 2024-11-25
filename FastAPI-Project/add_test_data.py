from database.connection import execute_query

# Test verisi ekle
execute_query("INSERT INTO tasks (title, date, duration) VALUES ('Test Görevi', '2024-11-20', 2)")
