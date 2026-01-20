"""Middleware for request logging and processing."""

import time
from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log request information and processing time."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request and log information."""
        start_time = time.perf_counter()

        logger.info(f"Request started: {request.method} {request.url.path}")

        response = await call_next(request)

        process_time = time.perf_counter() - start_time
        logger.info(
            f"Request completed: {request.method} {request.url.path} "
            f"status={response.status_code} duration={process_time:.3f}s"
        )

        response.headers["X-Process-Time"] = f"{process_time:.3f}"
        return response
