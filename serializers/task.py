from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskSerializer(BaseModel):
    task_id: str
    user_id: str
    title: str
    description: str
    due_date: datetime
    status: Status = None
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str

    class Config:
        from_attributes = True

