"""
Custom exception handlers and utilities for the API.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging
from typing import Union

from utils.exceptions import (
    UnauthorizedException,
    BadRequestException,
    NotFoundException,
    ValidationException,
    InternalServerErrorException,
    ConflictException
)
from api.schemas import ErrorResponse

logger = logging.getLogger(__name__)


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    error_response = ErrorResponse(
        code=500,
        message="Internal server error",
        details={"error": str(exc)} if str(exc) else None
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException) -> JSONResponse:
    """Handle unauthorized exceptions."""
    logger.warning(f"Unauthorized access: {exc}")
    error_response = ErrorResponse(
        code=401,
        message="Authentication failed or token expired",
        details={"error": str(exc)}
    )
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=error_response.model_dump()
    )


async def not_found_exception_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    """Handle not found exceptions."""
    logger.warning(f"Resource not found: {exc}")
    error_response = ErrorResponse(
        code=404,
        message="Resource not found",
        details={"error": str(exc)}
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error_response.model_dump()
    )


async def bad_request_exception_handler(request: Request, exc: BadRequestException) -> JSONResponse:
    """Handle bad request exceptions."""
    logger.warning(f"Bad request: {exc}")
    error_response = ErrorResponse(
        code=400,
        message="Bad request",
        details={"error": str(exc)}
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response.model_dump()
    )


async def validation_exception_handler(request: Request, exc: ValidationException) -> JSONResponse:
    """Handle validation exceptions."""
    logger.warning(f"Validation error: {exc}")
    error_response = ErrorResponse(
        code=422,
        message="Validation error",
        details={"error": str(exc)}
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump()
    )


async def conflict_exception_handler(request: Request, exc: ConflictException) -> JSONResponse:
    """Handle conflict exceptions."""
    logger.warning(f"Conflict: {exc}")
    error_response = ErrorResponse(
        code=409,
        message="Conflict",
        details={"error": str(exc)}
    )
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=error_response.model_dump()
    )


async def internal_server_error_exception_handler(
    request: Request,
    exc: InternalServerErrorException
) -> JSONResponse:
    """Handle internal server error exceptions."""
    logger.error(f"Internal server error: {exc}", exc_info=True)
    error_response = ErrorResponse(
        code=500,
        message="Internal server error",
        details={"error": str(exc)}
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump()
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors."""
    logger.warning(f"Validation error: {exc}")
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"][1:]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    error_response = ErrorResponse(
        code=422,
        message="Request validation failed",
        details={"errors": errors}
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump()
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers to the FastAPI app."""
    app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(BadRequestException, bad_request_exception_handler)
    app.add_exception_handler(ValidationException, validation_exception_handler)
    app.add_exception_handler(ConflictException, conflict_exception_handler)
    app.add_exception_handler(InternalServerErrorException, internal_server_error_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)
