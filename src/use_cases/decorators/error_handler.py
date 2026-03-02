from dataclasses import dataclass
from functools import wraps

@dataclass
class UseCaseExceptionResponse:
    message: str
    exit_code: int = 1


def ExceptionHandler(func):
    @wraps(func)
    def wrapper(use_case, request_model):
        try:
            return func(use_case, request_model)
        except Exception as exc:
            return UseCaseExceptionResponse(message=str(exc))

    return wrapper
