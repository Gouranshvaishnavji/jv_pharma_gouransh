from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.errors import CustomAPIError
from app.core.logger import setup_logger

logger = setup_logger()

async def custom_api_error_handler(request: Request, exc: CustomAPIError):
    logger.error(f"CustomAPIError: {exc.message} | Code={exc.error_code} | Path={request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTPException: {exc.detail} | Path={request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "message": exc.detail,
                "code": "HTTP_ERROR",
                "details": {"path": str(request.url.path)}
            }
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error at {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "message": "Validation failed for input data.",
                "code": "VALIDATION_ERROR",
                "details": exc.errors()
            }
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled Exception at {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "message": "An unexpected server error occurred.",
                "code": "INTERNAL_SERVER_ERROR",
                "details": {}
            }
        }
    )
