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
from services.post_task_history_service import post_task_history_service
from services.undo_action_service import undo_task_action

from schemas.task_create import TaskCreateSchema
from schemas.task_update import TaskUpdateSchema
from schemas.task_search_by_criteria import TaskSearchByCriteriaSchema
from schemas.task_history_search_by_criteria import TaskHistorySearchByCriteriaSchema

from utils.app_exceptions import AppException
from utils.service_result import ServiceResult
from utils.service_result import handle_result
from constants.action_type import ActionType

from services.update_task_service import update_task_service
from services.delete_task_service import delete_task_service
from services.get_task_by_criteria_service import get_task_by_criteria_service
from services.create_task_service import create_task_service
from services.get_task_history import get_task_history_service
from services.get_task_history_by_criteria_service import get_task_history_by_criteria_service
from services.update_task_history_service import update_history_task_service

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
    is_success, new_task = await create_task_service(db_session, task)
    await post_task_history_service(db_session, new_task.task_id, ActionType.CREATE)
    if not is_success:
        return ServiceResult(AppException.CreateTask(new_task))
    result = ServiceResult(new_task.model_dump())
    return handle_result(result)


@task_api.patch("/")
async def patch_task(
        task_id: str,
        task: TaskUpdateSchema,
        db_session=Depends(db.get_db)
):
    await post_task_history_service(db_session, task_id, ActionType.UPDATE)
    is_success, updated_task = await update_task_service(db_session, task)
    if not is_success:
        return ServiceResult(AppException.UpdateTask(updated_task))
    result = ServiceResult(updated_task.model_dump())
    return handle_result(result)


@task_api.delete("/{task_id}")
async def delete_task(
        task_id: str,
        db_session=Depends(db.get_db)
):
    await post_task_history_service(db_session, task_id, ActionType.DELETE)
    is_delete_success, deleted_task = await delete_task_service(db_session, task_id)
    if not is_delete_success:
        return ServiceResult(AppException.DeleteTask(deleted_task))
    result = ServiceResult(delete_task.model_dump())
    return result


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
    is_success, tasks = await get_task_by_criteria_service(db_session, criteria)
    if not is_success:
        return ServiceResult(AppException.GetTaskByCriteria(tasks))
    result = ServiceResult(tasks)
    return handle_result(result)


@task_api.get("/history")
async def get_all_tasks_history(db_session=Depends(db.get_db)):
    is_success, tasks_history_list = get_task_history_service(db_session)
    if not is_success:
        return ServiceResult(AppException.GetAllTaskHistory(tasks_history_list))
    result = ServiceResult(tasks_history_list)
    return handle_result(result)


@task_api.get("/undo")
async def undo_last_action(
        user_id: str,
        db_session=Depends(db.get_db)):
    criteria = TaskHistorySearchByCriteriaSchema(
        user_id=user_id,
        is_archived=False
    )
    tasks_history = await get_task_history_by_criteria_service(db_session, criteria)
    is_success, updated_task_history = await update_history_task_service(db_session, tasks_history, is_archived=True)
    if not is_success:
        return ServiceResult(AppException.UndoLastAction(updated_task_history))
    result = ServiceResult(updated_task_history)
    return handle_result(result)


