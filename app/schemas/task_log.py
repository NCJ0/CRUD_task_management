from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class TaskLogSchema(BaseModel):
    user_id: Optional[str] = ""
    title: Optional[str] = ""
    description: Optional[str] = ""
    due_date: Optional[datetime]
    status: Optional[str] = ""
    created_at: Optional[datetime]
    created_by: Optional[str] = ""
    updated_at: Optional[datetime]
    updated_by: Optional[str] = ""

    class Config:
        from_attributes = True
        fields = {'user_id': {'exclude': True},
                  'title': {'exclude': True}, 'description': {'exclude': True}, 'due_date': {'exclude': True},
                  'status': {'exclude': True}, 'updated_by': {'exclude': True}, }

