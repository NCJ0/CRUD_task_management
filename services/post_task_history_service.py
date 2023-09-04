from models.task_history import TaskHistory
from models.task import Task
from constants.action_type_constant import ActionType

from schemas.task_log import TaskLogSchema
from schemas.task_search_by_criteria import TaskSearchByCriteriaSchema

from services.get_task_by_criteria_service import get_task_by_criteria_service


async def post_task_history_service(db_session, task_id, mode: ActionType):
    criteria = TaskSearchByCriteriaSchema(
        task_id=task_id
    )
    is_success, tasks = await get_task_by_criteria_service(db_session, criteria)
    if is_success:
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
        action_type = mode.value
        result = await TaskHistory.create(db_session, task_id, action_type, **log_task.model_dump())
    else:
        result = tasks
    # save log result via pub/sub
    return is_success, result

