from fastapi import Request
from starlette.responses import JSONResponse


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
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
        def __init__(self, context: dict = None):
            """
            Tasks not found
            """
            status_code = 404
            AppExceptionCase.__init__(self, status_code, context)

    class CreateTask(AppExceptionCase):
        def __init__(self, context: dict = None):
            """
            Failed to create task
            """
            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)

