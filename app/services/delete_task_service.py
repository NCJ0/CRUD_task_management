from models.task import Task

from models.responses.delete_task import DeleteItemResponse


async def delete_task_service(db_session, task_id: str):
    is_delete_success = await Task.delete(db_session, task_id)
    delete_task = DeleteItemResponse(
        is_delete_success=is_delete_success
    )
    return is_delete_success, delete_task
