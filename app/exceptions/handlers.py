import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.custom_exceptions import BaseAppException

logger = logging.getLogger(__name__)


def create_error_response(
    status_code: int,
    message: str,
    details: any = None,
    path: str = None
) -> dict:
    """Create a standardized error response."""
    response = {
        "success": False,
        "error": {
            "status_code": status_code,
            "message": message,
        }
    }
    if details:
        response["error"]["details"] = details
    if path:
        response["error"]["path"] = path
    return response


async def base_app_exception_handler(request: Request, exc: BaseAppException):
    """Handle all custom application exceptions."""
    logger.warning(
        f"Application exception: {exc.message} | Path: {request.url.path}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            status_code=exc.status_code,
            message=exc.message,
            details=exc.details,
            path=request.url.path
        )
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(f"Validation error: {errors} | Path: {request.url.path}")
    return JSONResponse(
        status_code=422,
        content=create_error_response(
            status_code=422,
            message="Validation error",
            details=errors,
            path=request.url.path
        )
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle Starlette/FastAPI HTTP exceptions."""
    logger.warning(
        f"HTTP exception: {exc.detail} | Status: {exc.status_code} | Path: {request.url.path}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            status_code=exc.status_code,
            message=str(exc.detail),
            path=request.url.path
        )
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors (e.g., unique constraint violations)."""
    logger.error(f"Integrity error: {str(exc)} | Path: {request.url.path}")
    return JSONResponse(
        status_code=409,
        content=create_error_response(
            status_code=409,
            message="A record with this data already exists",
            path=request.url.path
        )
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {str(exc)} | Path: {request.url.path}")
    return JSONResponse(
        status_code=500,
        content=create_error_response(
            status_code=500,
            message="A database error occurred",
            path=request.url.path
        )
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle any unhandled exceptions."""
    logger.exception(f"Unhandled exception: {str(exc)} | Path: {request.url.path}")
    return JSONResponse(
        status_code=500,
        content=create_error_response(
            status_code=500,
            message="An internal server error occurred",
            path=request.url.path
        )
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers with the FastAPI app."""
    app.add_exception_handler(BaseAppException, base_app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
