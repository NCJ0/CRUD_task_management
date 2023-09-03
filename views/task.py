from typing import List

from fastapi import APIRouter, Depends

from models.task import Task
from config.db import db
from serializers.task import TaskSerializer
from utils.app_exceptions import AppException
from utils.service_result import ServiceResult


task_api = APIRouter(
    prefix="/v1/task",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


@task_api.get("/")
async def get_all_users(db_session=Depends(db.get_db)) -> ServiceResult:
    tasks = await Task.get_all(db_session)
    if not tasks:
        return ServiceResult(AppException.TaskGetAllItem())
    return ServiceResult(tasks)
