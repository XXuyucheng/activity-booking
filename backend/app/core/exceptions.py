"""异常类型与 handler 挂载点。"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class ApiError(Exception):
    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthError(ApiError):
    pass


class NotFoundError(ApiError):
    def __init__(self, message: str = "not found") -> None:
        super().__init__(message, status_code=404)


class ConflictError(ApiError):
    def __init__(self, message: str = "conflict") -> None:
        super().__init__(message, status_code=409)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def api_error_handler(_request: Request, exc: ApiError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )
