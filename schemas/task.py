from pydantic import BaseModel, field_validator
from enum import Enum
from datetime import datetime


class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskCreateSchema(BaseModel):
    user_id: str
    title: str
    description: str
    due_date: datetime
    status: str = None
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str

    @field_validator('due_date', mode="before")
    def string_due_date_to_datetime(cls, v: object) -> object:
        if isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
        return v

    @field_validator('created_at', mode="before")
    def string_created_at_to_datetime(cls, v: object) -> object:
        if isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
        return v

    @field_validator('updated_at', mode="before")
    def string_updated_at_to_datetime(cls, v: object) -> object:
        if isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
        return v

    class Config:
        from_attributes = True

