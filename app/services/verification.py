"""Verification service for image-task matching."""

import asyncio
import time
import base64
from fastapi import UploadFile
from loguru import logger
from app.clients import vlm_client
from app.config import get_settings
from app.schemas.response import VerifyResponse, VerificationResult
from app.utils.prompts import build_verification_prompt


# Semaphore for concurrency control
settings = get_settings()
request_semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_REQUESTS)


async def verify_image_task(image: UploadFile, task_description: str) -> VerifyResponse:
    """
    Verify if an image matches the given task using VLM.

    Args:
        image: Uploaded image file
        task_description: Description of the task

    Returns:
        VerifyResponse with match result, reason, and processing time

    Raises:
        Exception: If VLM service fails or returns invalid data
    """
    start_time = time.perf_counter()

    logger.info(f"Starting verification: {task_description[:50]}...")

    async with request_semaphore:
        try:
            # Read image file and encode to base64
            image_bytes = await image.read()
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")

            # Build prompt
            prompt = build_verification_prompt(task_description)

            # Prepare messages with image
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                        },
                    ],
                }
            ]

            # Call VLM with guided JSON output
            logger.debug(f"Calling VLM service at {settings.VLM_BASE_URL}")
            response = await vlm_client.client.chat.completions.create(
                model=settings.VLM_MODEL_NAME,
                messages=messages,
                extra_body={
                    "guided_json": VerificationResult.model_json_schema(),
                },
                temperature=0.1,
                max_tokens=512,
            )

            # Parse structured output
            content = response.choices[0].message.content
            logger.info(f"VLM response: {content}")

            result = VerificationResult.model_validate_json(content)
            logger.info(f"Verification completed: match={result.match}")

        except Exception as e:
            logger.error(f"Verification failed: {str(e)}")
            raise

    processing_time = time.perf_counter() - start_time

    return VerifyResponse(
        match=result.match,
        reason=result.reason,
        processing_time=round(processing_time, 3),
    )
