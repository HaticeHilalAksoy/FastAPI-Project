from fastapi import APIRouter, HTTPException
from database.connection import execute_query
from schemas.task_schema import TaskCreate, TaskResponse, UpdateTaskSchema
from typing import List
from datetime import date, timedelta
from fastapi.responses import JSONResponse
from datetime import datetime, date, time

task_router = APIRouter()

import logging

logging.basicConfig(level=logging.INFO)

@task_router.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    query = "SELECT * FROM tasks"
    result = execute_query(query)

    tasks = []
    for row in result:
        task = dict(row)
        
        # Loglama ekleyerek `reminder_time` alanını kontrol edelim
        logging.info(f"Orijinal reminder_time: {task.get('reminder_time')}")
        
        reminder_time = task.get("reminder_time")
        if reminder_time:
            try:
                task["reminder_time"] = datetime.fromisoformat(reminder_time)
            except ValueError:
                logging.warning(f"Geçersiz reminder_time formatı: {reminder_time}, None olarak ayarlandı.")
                task["reminder_time"] = None

        tasks.append(task)

    return tasks



# Yeni Görev Ekleme
# Yeni Görev Ekleme
@task_router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    query = """
    INSERT INTO tasks (title, description, date, duration, is_completed, reminder_time)
    VALUES (:title, :description, :date, :duration, :is_completed, :reminder_time)
    """
    values = task.dict()

    # Eğer `reminder_time` string olarak geliyorsa uygun formata çevirelim
    reminder_time = values.get("reminder_time")
    if reminder_time:
        try:
            # Eğer sadece saat bilgisi geldiyse bugünün tarihi ile birleştirip datetime oluşturun
            if isinstance(reminder_time, str) and len(reminder_time) == 8:  # Örneğin "02:11:00"
                today = date.today()
                reminder_time_obj = datetime.combine(today, time.fromisoformat(reminder_time))
                values["reminder_time"] = reminder_time_obj.isoformat()
            elif isinstance(reminder_time, str):
                reminder_time_obj = datetime.fromisoformat(reminder_time)
                values["reminder_time"] = reminder_time_obj.isoformat()
        except ValueError:
            raise HTTPException(status_code=400, detail="Geçersiz reminder_time formatı")
    else:
        values["reminder_time"] = None

    execute_query(query, values)

    # Eklenen görevi döndür
    result = execute_query("SELECT * FROM tasks ORDER BY id DESC LIMIT 1")
    return dict(result.fetchone())

# Görev Silme
@task_router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    query = "DELETE FROM tasks WHERE id = :task_id"
    result = execute_query(query, {"task_id": task_id})
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Görev bulunamadı")
    return {"detail": "Görev silindi"}

# Haftalık Rapor Alma
@task_router.get("/report")
def get_weekly_report():
    today = date.today()
    week_start = today - timedelta(days=7)

    query = """
    SELECT * FROM tasks
    WHERE date BETWEEN :week_start AND :today
    """
    values = {"week_start": week_start, "today": today}
    result = execute_query(query, values)

    tasks = [dict(row) for row in result]

    completed_tasks = [task for task in tasks if task["is_completed"]]
    not_completed_tasks = [task for task in tasks if not task["is_completed"]]

    total_completed_duration = sum(task["duration"] for task in completed_tasks)

    report = {
        "completed_tasks": completed_tasks,
        "not_completed_tasks": not_completed_tasks,
        "total_completed_duration": total_completed_duration,
        "week_start": week_start.isoformat(),
        "week_end": today.isoformat(),
    }

    return JSONResponse(content=report)

# Görev Güncelleme
@task_router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: UpdateTaskSchema):
    query = "SELECT * FROM tasks WHERE id = :task_id"
    db_task = execute_query(query, {"task_id": task_id}).fetchone()

    if not db_task:
        raise HTTPException(status_code=404, detail="Görev bulunamadı")

    update_query = """
    UPDATE tasks
    SET is_completed = :is_completed
    WHERE id = :task_id
    """
    execute_query(update_query, {"is_completed": task.is_completed, "task_id": task_id})

    updated_task = execute_query("SELECT * FROM tasks WHERE id = :task_id", {"task_id": task_id}).fetchone()
    return dict(updated_task)
