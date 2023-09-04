from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

from constants.datetime_constant import DateTimeConstant


class GetAllHistoryResponse(BaseModel):
    task_history_id: str
    task_id: Optional[str] = None
    user_id: Optional[str] = None
    action_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    created_by: Optional[str] = None
    updated_at: Optional[str] = None
    updated_by: Optional[str] = None
    logged_at: Optional[str] = None
    is_archived: Optional[bool] = None

    @field_validator('due_date', mode="before")
    def string_due_date_to_datetime(cls, v: object) -> object:
        if isinstance(v, datetime):
            return datetime.strftime(v, DateTimeConstant.GLOBAL_TIME_FORMAT)
        return v

    @field_validator('created_at', mode="before")
    def string_created_at_to_datetime(cls, v: object) -> object:
        if isinstance(v, datetime):
            return datetime.strftime(v, DateTimeConstant.GLOBAL_TIME_FORMAT)
        return v

    @field_validator('updated_at', mode="before")
    def string_updated_at_to_datetime(cls, v: object) -> object:
        if isinstance(v, datetime):
            return datetime.strftime(v, DateTimeConstant.GLOBAL_TIME_FORMAT)
        return v

    @field_validator('logged_at', mode="before")
    def string_logged_at_to_datetime(cls, v: object) -> object:
        if isinstance(v, datetime):
            return datetime.strftime(v, DateTimeConstant.GLOBAL_TIME_FORMAT)
        return v


