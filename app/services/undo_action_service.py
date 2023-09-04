from constants.action_type_constant import ActionType


from schemas.task_update import TaskUpdateSchema
from schemas.task_create import TaskCreateSchema

from models.task_history import TaskHistory

from models.responses.get_all_history import GetAllHistoryResponse


from services.update_task_service import update_task_service
from services.delete_task_service import delete_task_service
from services.create_task_service import create_task_service


async def undo_task_action(db_session, tasks_history: [TaskHistory]):
    latest_task = tasks_history[0]
    archive_task_history = GetAllHistoryResponse(
        task_history_id=latest_task.task_history_id,
    )
    if latest_task.action_type == ActionType.CREATE.value:
        is_success, result = await delete_task_service(db_session, latest_task.task_id)

    elif latest_task.action_type == ActionType.UPDATE.value:
        task_to_update = TaskUpdateSchema(
            task_id=latest_task.task_id,
            user_id=latest_task.user_id,
            title=latest_task.title,
            description=latest_task.description,
            due_date=latest_task.due_date,
            status=latest_task.status,
            updated_by=latest_task.updated_by
        )
        is_success, result = await update_task_service(db_session, task_to_update)

    elif latest_task.action_type == ActionType.DELETE.value:
        task_to_create = TaskCreateSchema(
            user_id=latest_task.user_id,
            title=latest_task.title,
            description=latest_task.description,
            due_date=latest_task.due_date,
            status=latest_task.status,
            created_by=latest_task.created_by
        )
        is_success, result = await create_task_service(db_session, task_to_create)

    else:
        is_success = False
        result = False

    return is_success, result


