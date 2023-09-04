from starlette.responses import JSONResponse


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: any):
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
    class FailedToGetAllTask(AppExceptionCase):
        def __init__(self, context: any = None):
            """
            Tasks not found
            """
            status_code = 10001
            AppExceptionCase.__init__(self, status_code, context)

    class FailedToCreateTask(AppExceptionCase):
        def __init__(self, context: any = None):
            """
            Failed to create task
            """
            status_code = 10002
            AppExceptionCase.__init__(self, status_code, context)

    class FailedToUpdateTask(AppExceptionCase):
        def __init__(self, context: any = None):
            """
            Failed to update task
            """
            status_code = 10003
            AppExceptionCase.__init__(self, status_code, context)

    class FailedToDeleteTask(AppExceptionCase):
        def __init__(self, context: any = None):
            """
            Failed to delete task
            """
            status_code = 10004
            AppExceptionCase.__init__(self, status_code, context)

    class FailedToGetTaskByCriteria(AppExceptionCase):
        def __init__(self, context: any = None):
            """
            Task not found
            """
            status_code = 10005
            AppExceptionCase.__init__(self, status_code, context)

    class FailedToGetAllTaskHistory(AppExceptionCase):
        def __init__(self, context: any = None):
            """
            Tasks history not found
            """
            status_code = 10006
            AppExceptionCase.__init__(self, status_code, context)

    class FailedToUndoLastAction(AppExceptionCase):
        def __init__(self, context: any = None):
            """
            Failed to undo action
            """
            status_code = 10007
            AppExceptionCase.__init__(self, status_code, context)
