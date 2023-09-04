from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class TaskHistorySearchByCriteriaSchema(BaseModel):
    task_history_id: Optional[str] = None
    task_id: Optional[str] = None
    action_type: Optional[str] = None
    user_id: Optional[str] = None
    title: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    logged_at: Optional[datetime] = None
    is_archived: Optional[bool] = None

    @field_validator('due_date', mode="before")
    def string_due_date_to_datetime(cls, v: object) -> object:
        if isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
        return v

    @field_validator('logged_at', mode="before")
    def string_logged_at_to_datetime(cls, v: object) -> object:
        if isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
        return v

    class Config:
        from_attributes = True
        fields = {'task_history_id': {'exclude': True}, 'task_id': {'exclude': True}, 'user_id': {'exclude': True},
                  'title': {'exclude': True}, 'due_date': {'exclude': True},
                  'status': {'exclude': True}, 'created_by': {'exclude': True}, 'updated_by': {'exclude': True},
                  'logged_at': {'exclude': True}, 'is_archived': {'exclude': True}, }
