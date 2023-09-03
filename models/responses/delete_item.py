from pydantic import BaseModel


class DeleteItemResponse(BaseModel):
    is_delete_success: bool

