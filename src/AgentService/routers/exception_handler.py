from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from utils.exception import AppException


def register_handler(app: FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.message,
            },
        )

