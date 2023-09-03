from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class TaskCreateSchema(BaseModel):
    user_id: Optional[str] = ""
    title: str
    description: Optional[str] = ""
    due_date: datetime
    status: Optional[str] = ""
    status: str
    created_by: str


    @field_validator('due_date', mode="before")
    def string_due_date_to_datetime(cls, v: object) -> object:
        if isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
        return v

    class Config:
        from_attributes = True
        fields = {'user_id': {'exclude': True},
                  'title': {'exclude': True}, 'description': {'exclude': True}, 'due_date': {'exclude': True},
                  'status': {'exclude': True}, 'updated_by': {'exclude': True}, }

