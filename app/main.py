"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.clients import vlm_client
from app.exceptions import setup_exception_handlers
from app.middleware import RequestLoggingMiddleware
from app.utils.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    setup_logging()
    vlm_client.initialize()
    yield
    # Shutdown
    await vlm_client.close()


app = FastAPI(
    title="VLM-Recheck API",
    description="Image-task verification service using Qwen3-VL",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)

# Exception handlers
setup_exception_handlers(app)

# Routes
app.include_router(api_router, prefix="/api/v1")
