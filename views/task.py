from typing import Optional

from fastapi import APIRouter, Depends

from models.task import Task
from models.task_history import TaskHistory
from models.responses.create_item import CreateItemResponse
from models.responses.update_item import UpdateItemResponse
from models.responses.get_all import GetAllItemResponse
from models.responses.get_all_history import GetAllHistoryResponse
from models.responses.delete_item import DeleteItemResponse
from config.db import db
from helper_funcs.save_action_to_log import save_action_log_item_create, save_action_log_item_update, save_action_log_item_delete

from schemas.task_create import TaskCreateSchema
from schemas.task_update import TaskUpdateSchema
from schemas.task_search_by_criteria import TaskSearchByCriteriaSchema

from utils.app_exceptions import AppException
from utils.service_result import ServiceResult
from utils.service_result import handle_result

from serializers.task import TaskSerializer # put in service


task_api = APIRouter(
    prefix="/v1/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


@task_api.get("/")
async def get_all_tasks(db_session=Depends(db.get_db)):
    tasks = await Task.get_all(db_session)
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
    ).model_dump() for task in tasks]
    if not tasks:
        return ServiceResult(AppException.GetAllTask(tasks))
    result = ServiceResult(tasks_list)
    return handle_result(result)


@task_api.post("/")
async def create_task(
        task: TaskCreateSchema,
        db_session=Depends(db.get_db)
):
    task = await Task.create(db_session, **task.model_dump())
    new_task = CreateItemResponse(task_id=task.task_id, title=task.title)
    log_result = await save_action_log_item_create(db_session, task.task_id)
    if not new_task:
        return ServiceResult(AppException.CreateTask(new_task))
    result = ServiceResult(new_task.model_dump())
    return handle_result(result)


@task_api.patch("/{task_id}")
async def update(
        task_id: str,
        task: TaskUpdateSchema,
        db_session=Depends(db.get_db)
):
    task = await Task.update(db_session, task_id, **task.model_dump())
    log_result = await save_action_log_item_update(db, task_id, **task.model())
    updated_task = UpdateItemResponse(
        task_id=task.task_id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        status=task.status,
        created_at=task.created_at,
        created_by=task.created_by,
        updated_at=task.updated_at,
        updated_by=task.updated_by)
    if not updated_task:
        return ServiceResult(AppException.UpdateTask(updated_task))
    result = ServiceResult(updated_task.model_dump())
    return handle_result(result)

# title: Optional[str] = ""
    # description: Optional[str] = ""
    # due_date: Optional[datetime]
    # status: Optional[str] = ""
    # created_at: Optional[datetime]
    # created_by: Optional[str] = ""
    # updated_at: Optional[datetime]
    # updated_by: Optional[str] = ""


@task_api.delete("/{task_id}")
async def delete_user(
        task_id: str,
        db_session=Depends(db.get_db)
):
    log_result = await save_action_log_item_delete(db_session, task_id)
    is_delete_success = await Task.delete(db_session, task_id)
    delete_task = DeleteItemResponse(
        is_delete_success=is_delete_success
    )
    if not is_delete_success:
        return ServiceResult(AppException.DeleteTask(delete_task))
    result = ServiceResult(delete_task.model_dump())
    return result
    pass


@task_api.get("/search_by_criteria/")
async def get_all_tasks(
        task_id: Optional[str] = None,
        title: Optional[str] = None,
        user_id: Optional[str] = None,
        due_date: Optional[str] = None,
        status: Optional[str] = None,
        created_by: Optional[str] = None,
        updated_by: Optional[str] = None,
        db_session=Depends(db.get_db)):
    criteria = TaskSearchByCriteriaSchema(
        task_id=task_id,
        title=title,
        user_id=user_id,
        due_date=due_date,
        status=status,
        created_by=created_by,
        updated_by=updated_by
    )
    tasks = await Task.get(db_session, criteria)
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
    ).model_dump() for task in tasks]
    if not tasks:
        return ServiceResult(AppException.GetTaskByCriteria(tasks))
    result = ServiceResult(tasks_list)
    return handle_result(result)


@task_api.get("/history")
async def get_all_tasks_history(db_session=Depends(db.get_db)):
    tasks = await TaskHistory.get_all(db_session)
    tasks_list = [GetAllHistoryResponse(
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
    ).model_dump() for task in tasks]
    if not tasks_list:
        return ServiceResult(AppException.GetAllTaskHistory(tasks_list))
    result = ServiceResult(tasks_list)
    return handle_result(result)
