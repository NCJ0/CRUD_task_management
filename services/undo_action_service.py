from models.task_history import TaskHistory
from models.task import Task
from constants.action_type_constant import ActionType

from schemas.task_log import TaskLogSchema
from schemas.task_search_by_criteria import TaskSearchByCriteriaSchema
from schemas.task_update import TaskUpdateSchema
from schemas.task_create import TaskCreateSchema

from models.task_history import TaskHistory
from models.responses.delete_item import DeleteItemResponse
from models.responses.get_all_history import GetAllHistoryResponse

from utils.app_exceptions import AppException

from utils.service_result import ServiceResult

from services.update_task_service import update_task_service
from services.delete_task_service import delete_task_service
from services.get_task_by_criteria_service import get_task_by_criteria_service
from services.create_task_service import create_task_service
from services.get_task_history_service import get_task_history_service
from services.update_task_history_service import update_history_task_service


async def undo_task_action(db_session, tasks_history: [TaskHistory]):
    latest_task = tasks_history[0]
    archive_task_history = GetAllHistoryResponse(
        task_history_id=latest_task.task_history_id,
    )
    if latest_task.action_type == ActionType.CREATE.value:
        is_success, result = await delete_task_service(db_session, latest_task.task_id)
        is_log_success, _ = await update_history_task_service(db_session, archive_task_history, is_archived=True)

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
        is_log_success, _ = await update_history_task_service(db_session, archive_task_history, is_archived=True)

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
        is_log_success, _ = await update_history_task_service(db_session, archive_task_history, is_archived=True)

    else:
        is_success = False
        is_log_success = False

    return is_success, is_log_success


