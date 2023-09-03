from typing import List

from fastapi import APIRouter, Depends

from models.task import Task
from models.responses.create_item import CreateItemResponse
from models.responses.get_all import GetAllItemResponse
from config.db import db

from schemas.task import TaskCreateSchema
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
    task = CreateItemResponse(task_id=task[0], title=task[1])
    if not task:
        return ServiceResult(AppException.CreateTask(task))
    result = ServiceResult(task.model_dump())
    return handle_result(result)
