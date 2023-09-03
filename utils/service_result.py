from loguru import logger
import inspect
from starlette.responses import JSONResponse
from enum import Enum

from utils.app_exceptions import AppExceptionCase



class ResponseCode(Enum):
    SUCCESS = "0000"
    FAILED = "9999"


class ServiceResult(object):
    def __init__(self, arg):
        if isinstance(arg, AppExceptionCase):
            self.success = False
            self.exception_case = arg.exception_case
            self.status_code = ResponseCode.FAILED.value
        else:
            self.success = True
            self.exception_case = None
            self.status_code = ResponseCode.SUCCESS.value
        self.value = arg

    def __str__(self):
        if self.success:
            return f"code: {self.status_code}, description: {self.exception_case}, data: {self.value}"
        return f'[Exception] "{self.exception_case}"'

    def __repr__(self):
        if self.success:
            return "<ServiceResult Success>"
        return f"<ServiceResult AppException {self.exception_case}>"

    def __enter__(self):
        return self.value

    def __exit__(self, *kwargs):
        pass


def caller_info() -> str:
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


def handle_result(result: ServiceResult):
    if not result.success:
        with result as exception:
            logger.error(f"{exception} | caller={caller_info()}")
            raise exception
    resp = {"code": result.status_code, "description": result.exception_case, "data": result.value}
    return JSONResponse(content=resp, status_code=200)

