from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskLogUpdateSchema(BaseModel):
    task_id: Optional[str] = ""
    user_id: Optional[str] = ""
    action_type: Optional[str] = ""
    title: Optional[str] = ""
    description: Optional[str] = ""
    due_date: Optional[datetime]
    status: Optional[str] = ""
    created_at: Optional[datetime]
    created_by: Optional[str] = ""
    updated_at: Optional[datetime]
    updated_by: Optional[str] = ""
    logged_at: Optional[datetime] = ""
    is_archived: Optional[bool]

    class Config:
        from_attributes = True
        fields = {'task_id': {'exclude': True}, 'user_id': {'exclude': True},
                  'title': {'exclude': True}, 'description': {'exclude': True}, 'due_date': {'exclude': True},
                  'status': {'exclude': True}, 'updated_by': {'exclude': True}, 'logged_at': {'exclude': True}, 'is_archived': {'exclude': True}, }
