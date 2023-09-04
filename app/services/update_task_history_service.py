from schemas.task_history_update import TaskLogUpdateSchema

from models.task_history import TaskHistory

from models.responses.get_all_history import GetAllHistoryResponse


async def update_history_task_service(db_session, task: GetAllHistoryResponse, is_archived=False):
    task_history_id = task.task_history_id
    new_task_history = await archive_task_history(db_session, task, task_history_id, is_archived)
    if new_task_history:
        updated_task_history = GetAllHistoryResponse(
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
            is_archived=task.is_archived)
        is_success = True
    else:
        updated_task_history = new_task_history
        is_success = False
    return is_success, updated_task_history


async def archive_task_history(db_session, task: GetAllHistoryResponse, task_history_id: str, is_archived: bool = True):
    task_history_to_be_update = TaskLogUpdateSchema(
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
        is_archived=is_archived
    )
    return await TaskHistory.update(db_session, task_history_id, **task_history_to_be_update.model_dump())
