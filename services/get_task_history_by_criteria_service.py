from schemas.task_history_search_by_criteria import TaskHistorySearchByCriteriaSchema

from models.task_history import TaskHistory

from models.responses.get_all_history import GetAllHistoryResponse


async def get_task_history_by_criteria_service(db_session, criteria: TaskHistorySearchByCriteriaSchema):
    tasks = await TaskHistory.get(db_session, criteria)
    if tasks:
        tasks_history_list = [GetAllHistoryResponse(
            task_history_id=task.task_history_id,
            task_id=task.task_id,
            user_id=task.user_id,
            action_type=task.action_type,
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            status=task.status,
            created_at=task.created_at,
            created_by=task.created_by,
            updated_at=task.updated_at,
            updated_by=task.updated_by,
            logged_at=task.logged_at,
            is_archived=task.is_archived
        ) for task in tasks]
        is_success = True
    else:
        tasks_history_list = tasks
        is_success = False
    return is_success, tasks_history_list

