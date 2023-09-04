from typing import Optional

from fastapi import APIRouter, Depends

from config.db import db
from services.post_task_history_service import post_task_history_service
from services.undo_action_service import undo_task_action

from schemas.task_create import TaskCreateSchema
from schemas.task_update import TaskUpdateSchema
from schemas.task_search_by_criteria import TaskSearchByCriteriaSchema
from schemas.task_history_search_by_criteria import TaskHistorySearchByCriteriaSchema

from utils.app_exceptions import AppException
from utils.service_result import ServiceResult
from utils.service_result import handle_response
from constants.action_type_constant import ActionType

from services.update_task_service import update_task_service
from services.delete_task_service import delete_task_service
from services.get_task_by_criteria_service import get_task_by_criteria_service
from services.create_task_service import create_task_service
from services.get_task_history_service import get_task_history_service
from services.get_task_history_by_criteria_service import get_task_history_by_criteria_service
from services.update_task_history_service import update_history_task_service
from services.get_all_task_service import get_all_task_service

task_api = APIRouter(
    prefix="/v1/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


@task_api.get("/")
async def get_all_tasks(db_session=Depends(db.get_db)):
    is_success, tasks = await get_all_task_service(db_session)
    tasks_list = [task.model_dump() for task in tasks]
    if not tasks:
        return ServiceResult(AppException.FailedToGetAllTask(tasks_list))
    result = ServiceResult(tasks_list)
    return handle_response(result)


@task_api.post("/")
async def create_task(
        task: TaskCreateSchema,
        db_session=Depends(db.get_db)
):
    is_success, new_task = await create_task_service(db_session, task)
    await post_task_history_service(db_session, new_task.task_id, ActionType.CREATE)
    if not is_success:
        return ServiceResult(AppException.FailedToCreateTask(new_task))
    result = ServiceResult(new_task.model_dump())
    return handle_response(result)


@task_api.patch("/")
async def patch_task(
        task: TaskUpdateSchema,
        db_session=Depends(db.get_db)
):
    task_id = task.task_id
    await post_task_history_service(db_session, task_id, ActionType.UPDATE)
    is_success, updated_task = await update_task_service(db_session, task)
    if not is_success:
        return ServiceResult(AppException.FailedToUpdateTask(updated_task))
    result = ServiceResult(updated_task.model_dump())
    return handle_response(result)


@task_api.delete("/{task_id}")
async def delete_task(
        task_id: str,
        db_session=Depends(db.get_db)
):
    await post_task_history_service(db_session, task_id, ActionType.DELETE)
    is_delete_success, deleted_task = await delete_task_service(db_session, task_id)
    if not is_delete_success:
        return ServiceResult(AppException.FailedToDeleteTask(deleted_task))
    result = ServiceResult(deleted_task.model_dump())
    return handle_response(result)


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
    tasks_list = [task.model_dump() for task in tasks]
    if not is_success:
        return ServiceResult(AppException.FailedToGetTaskByCriteria(tasks_list))
    result = ServiceResult(tasks_list)
    return handle_response(result)


@task_api.get("/history")
async def get_all_tasks_history(db_session=Depends(db.get_db)):
    is_success, tasks_history = await get_task_history_service(db_session)
    tasks_history_list = [task_history.model_dump() for task_history in tasks_history]
    if not is_success:
        return ServiceResult(AppException.FailedToGetAllTaskHistory(tasks_history_list))
    result = ServiceResult(tasks_history_list)
    return handle_response(result)


@task_api.get("/undo")
async def undo_last_action(
        user_id: str,
        db_session=Depends(db.get_db)):
    criteria = TaskHistorySearchByCriteriaSchema(
        user_id=user_id,
        is_archived=False
    )
    _, tasks_history = await get_task_history_by_criteria_service(db_session, criteria)
    is_undo_success, is_undo_log_success = await undo_task_action(db_session, tasks_history)
    task_history = tasks_history[0]
    if is_undo_success and is_undo_log_success:
        await update_history_task_service(db_session, task_history, is_archived=True) # save log result via pub/sub
    if not is_undo_success:
        return ServiceResult(AppException.FailedToUndoLastAction(task_history))
    result = ServiceResult(task_history.model_dump())
    return handle_response(result)


