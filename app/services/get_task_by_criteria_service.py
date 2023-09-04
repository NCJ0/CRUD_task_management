from schemas.task_search_by_criteria import TaskSearchByCriteriaSchema

from models.task import Task

from models.responses.get_all import GetAllItemResponse


async def get_task_by_criteria_service(db_session, criteria: TaskSearchByCriteriaSchema):
    tasks = await Task.get(db_session, criteria)
    if tasks:
        tasks_list = [GetAllItemResponse(
            task_id=task.task_id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            status=task.status,
            created_at=task.created_at,
            created_by=task.created_by,
            updated_at=task.updated_at,
            updated_by=task.updated_by
        ) for task in tasks]
        is_success = True
    else:
        tasks_list = tasks
        is_success = False
    return is_success, tasks_list

