from pydantic import BaseModel


class CreateItemResponse(BaseModel):
    task_id: str
    title: str



