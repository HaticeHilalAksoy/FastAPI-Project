from pydantic import BaseModel
from datetime import date
from typing import Optional
from datetime import time
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: date
    duration: int  # Dakika cinsinden
    is_completed: Optional[bool] = False
    reminder_time: Optional[datetime] = None  # Yeni sütun


class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    title: str
    description: str
    date: datetime
    duration: int
    is_completed: bool
    reminder_time: Optional[datetime] = None

    class Config:
        from_attributes = True 
class UpdateTaskSchema(BaseModel):
    is_completed: bool