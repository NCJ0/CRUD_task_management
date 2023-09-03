from models.task_history import TaskHistory
from models.task import Task
from constants.action_type import ActionType

from schemas.task_log import TaskLogSchema
from schemas.task_search_by_criteria import TaskSearchByCriteriaSchema


async def save_action_log_item_create(db, task_id):
    action_type = ActionType.CREATE.value
    return await TaskHistory.create(db, task_id, action_type)


async def save_action_log_item_update(db, task_id, **kwargs):
    action_type = ActionType.UPDATE.value
    return await TaskHistory.create(db, task_id, action_type, **kwargs)


async def save_action_log_item_delete(db, task_id):
    criteria = TaskSearchByCriteriaSchema(
        task_id=task_id
    )
    tasks = await Task.get(db, criteria)
    task = tasks[0]
    log_task = TaskLogSchema(
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        status=task.status,
        created_at=task.created_at,
        created_by=task.created_by,
        updated_at=task.updated_at,
        updated_by=task.updated_by,
    )
    action_type = ActionType.DELETE.value
    return await TaskHistory.create(db, task_id, action_type, **log_task.model_dump())
