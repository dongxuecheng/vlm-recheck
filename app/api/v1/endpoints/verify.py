"""Verification endpoint for image-task matching."""

from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from loguru import logger
from app.schemas.response import VerifyResponse
from app.services.verification import verify_image_task
from app.exceptions import VLMServiceError

router = APIRouter()


@router.post(
    "/verify", response_model=VerifyResponse, summary="Verify image-task match"
)
async def verify(
    image: UploadFile = File(..., description="Image file to verify"),
    task_description: str = Form(
        ..., min_length=1, max_length=500, description="Task description"
    ),
) -> VerifyResponse:
    """
    Verify if an image matches the given task using VLM.

    This endpoint receives an image file along with a task description,
    then uses the Qwen3-VL model to determine if the image content matches the task.

    Args:
        image: Uploaded image file
        task_description: Detailed description of the task

    Returns:
        VerifyResponse with match result, reason, and processing time

    Raises:
        HTTPException: If validation fails or VLM service is unavailable
    """
    try:
        logger.info(f"Received verification request: {task_description[:50]}...")
        result = await verify_image_task(image, task_description)
        return result

    except VLMServiceError as e:
        logger.error(f"VLM service error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="VLM service is currently unavailable. Please try again later.",
        )

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error during verification: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during verification.",
        )
