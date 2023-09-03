from pydantic import BaseModel, field_validator
from datetime import datetime
from constants.datetime import DateTimeConstant


class UpdateItemResponse(BaseModel):
    task_id: str
    user_id: str
    title: str
    description: str
    due_date: str
    status: str
    created_at: str
    created_by: str
    updated_at: str
    updated_by: str

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

