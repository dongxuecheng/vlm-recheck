"""Custom exceptions for the application."""

from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger


class VLMServiceError(Exception):
    """Raised when VLM service fails."""

    pass


async def vlm_service_error_handler(
    request: Request, exc: VLMServiceError
) -> JSONResponse:
    """Handle VLM service errors."""
    logger.error(f"VLM service error: {str(exc)}")
    return JSONResponse(
        status_code=503,
        content={"detail": "VLM service unavailable. Please try again later."},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle generic exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred."},
    )


def setup_exception_handlers(app) -> None:
    """Register exception handlers with the FastAPI app."""
    app.add_exception_handler(VLMServiceError, vlm_service_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
