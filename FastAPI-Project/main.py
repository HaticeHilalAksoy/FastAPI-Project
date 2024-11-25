from fastapi import FastAPI
from models.task_model import create_tasks_table, add_is_notified_column
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from database.connection import execute_query
from datetime import datetime
import requests
from routes.task_routes import task_router

# FastAPI uygulamasını başlat
app = FastAPI(title="Günlük Çalışma Planlayıcı API")
app.include_router(task_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Veritabanı tablolarını oluşturma
def initialize_database():
    create_tasks_table()
    add_is_notified_column()

# Telegram mesaj gönderme
def send_telegram_message(chat_id: str, message: str):
    bot_token = "7620146666:AAFxcwEO-8lskWn1NIR9MYos24eQWw1cCs4"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": 1939709909,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram mesajı başarıyla gönderildi!")
        else:
            print(f"Mesaj gönderilemedi: {response.json()}")
    except Exception as e:
        print(f"Telegram mesajı gönderiminde hata: {e}")


# Hatırlatma işlemi
def check_and_notify():
    now = datetime.now()
    today = now.date()
    current_time = now.strftime("%H:%M:%S")

    query = """
    SELECT * FROM tasks
    WHERE date = :today
    AND reminder_time <= :current_time
    AND is_completed = 0
    AND is_notified = 0  -- Bildirim gönderilmeyen görevleri seç
    """
    tasks = execute_query(query, {"today": today, "current_time": current_time}).fetchall()

    for task in tasks:
        message = f"Hatırlatma! {task['title']} konusundan {task['duration']} saat çalışmanız gerekiyor."
        send_telegram_message("1939709909", message)  # Kullanıcı ID'nizi buraya yazın

        # Bildirim gönderildi olarak işaretle
        update_query = """
        UPDATE tasks
        SET is_notified = 1
        WHERE id = :task_id
        """
        execute_query(update_query, {"task_id": task["id"]})


# Zamanlayıcıyı başlat
scheduler = BackgroundScheduler()
scheduler.add_job(check_and_notify, 'interval', minutes=1)
scheduler.start()

@app.get("/")
def read_root():
    return {"message": "Günlük Çalışma Planlayıcı API'ye hoş geldiniz!"}

# Veritabanını başlat
initialize_database()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
