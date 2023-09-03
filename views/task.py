from typing import List

from fastapi import APIRouter, Depends

from models.task import Task
from models.responses.create_item import CreateItemResponse
from models.responses.update_item import UpdateItemResponse
from models.responses.get_all import GetAllItemResponse
from models.responses.delete_item import DeleteItemResponse
from config.db import db

from schemas.task_create import TaskCreateSchema
from schemas.task_update import TaskUpdateSchema
from utils.app_exceptions import AppException
from utils.service_result import ServiceResult
from utils.service_result import handle_result

from serializers.task import TaskSerializer # put in service
from datetime import datetime


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
    task = await (Task.create(db_session, **task.model_dump()))
    new_task = CreateItemResponse(task_id=task.task_id, title=task.title)
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


@task_api.delete("/{task_id}")
async def delete_user(
        task_id: str,
        db_session=Depends(db.get_db)
):
    is_delete_success = await Task.delete(db_session, task_id)
    delete_task = DeleteItemResponse(
        is_delete_success=is_delete_success
    )
    if not is_delete_success:
        return ServiceResult(AppException.DeleteTask(delete_task))
    result = ServiceResult(delete_task.model_dump())
    return result