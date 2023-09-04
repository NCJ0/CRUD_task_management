from schemas.task_history_update import TaskLogUpdateSchema

from models.task_history import TaskHistory

from models.responses.get_all_history import GetAllHistoryResponse


async def update_history_task_service(db_session, task: GetAllHistoryResponse, is_archived=False):
    task_history_id = task.task_history_id
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
    new_task = await TaskHistory.update(db_session, task_history_id, **task_history_to_be_update.model_dump())
    if new_task:
        updated_task = GetAllHistoryResponse(
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
        updated_task = new_task
        is_success = False
    return is_success, updated_task
