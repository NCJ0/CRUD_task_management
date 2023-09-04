from schemas.task_update import TaskUpdateSchema

from models.task import Task

from models.responses.update_item import UpdateItemResponse


async def update_task_service(db_session, task: TaskUpdateSchema):
    task_id = task.task_id
    new_task = await Task.update(db_session, task_id, **task.model_dump())
    if new_task:
        updated_task = UpdateItemResponse(
            task_id=new_task.task_id,
            user_id=new_task.user_id,
            title=new_task.title,
            description=new_task.description,
            due_date=new_task.due_date,
            status=new_task.status,
            created_at=new_task.created_at,
            created_by=new_task.created_by,
            updated_at=new_task.updated_at,
            updated_by=new_task.updated_by)
        is_success = True
    else:
        updated_task = new_task
        is_success = False
    return is_success, updated_task
