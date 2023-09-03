from typing import List

from fastapi import APIRouter, Depends

from models.task import Task
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
    if not tasks:
        return ServiceResult(AppException.GetAllTask())
    result = ServiceResult(tasks)
    return handle_result(result)


@task_api.post("/")
async def create_task(
        task: TaskCreateSchema,
        db_session=Depends(db.get_db)
):
    print('task.model_dump()', task.model_dump())
    task = await (Task.create(db_session, **task.model_dump()))
    task = tuple(task)
    print('type task', type(task))
    if not task:
        print('here1')
        return ServiceResult(AppException.CreateTask(task))
    print('here2')
    result = ServiceResult(task)
    print('result', result)
    return handle_result(result)
