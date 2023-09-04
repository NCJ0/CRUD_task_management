from schemas.task_create import TaskCreateSchema

from models.task import Task

from models.responses.create_task import CreateItemResponse


async def create_task_service(db_session, task: TaskCreateSchema):
    task = await Task.create(db_session, **task.model_dump())
    if task:
        task_created = CreateItemResponse(task_id=task.task_id, title=task.title)
        is_success = True
    else:
        task_created = task
        is_success = False
    return is_success, task_created
