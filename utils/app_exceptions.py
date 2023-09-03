from fastapi import Request
from starlette.responses import JSONResponse
from models.responses.create_item import CreateItemResponse
from models.responses.update_item import UpdateItemResponse
from models.responses.get_all import GetAllItemResponse
from models.responses.delete_item import DeleteItemResponse


class AppExceptionCase(Exception):
    def __init__(self, status_code: str, context: any):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code={self.status_code} - context={self.context}>"
        )


async def app_exception_handler(exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "app_exception": exc.exception_case,
            "context": exc.context,
        }
    )


class AppException(object):
    class GetAllTask(AppExceptionCase):
        def __init__(self, context: GetAllItemResponse = None):
            """
            Tasks not found
            """
            status_code = "10001"
            AppExceptionCase.__init__(self, status_code, context)

    class CreateTask(AppExceptionCase):
        def __init__(self, context: CreateItemResponse = None):
            """
            Failed to create task
            """
            status_code = "10002"
            AppExceptionCase.__init__(self, status_code, context)

    class UpdateTask(AppExceptionCase):
        def __init__(self, context: UpdateItemResponse = None):
            """
            Failed to update task
            """
            status_code = "10003"
            AppExceptionCase.__init__(self, status_code, context)

    class DeleteTask(AppExceptionCase):
        def __init__(self, context: DeleteItemResponse = None):
            """
            Failed to delete task
            """
            status_code = "10004"
            AppExceptionCase.__init__(self, status_code, context)

