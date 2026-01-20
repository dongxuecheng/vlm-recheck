"""Response schemas for API endpoints."""

from pydantic import BaseModel, Field


class VerificationResult(BaseModel):
    """Internal model for VLM structured output (guided JSON)."""

    match: bool = Field(..., description="Whether the image matches the task")
    reason: str = Field(..., description="Explanation for the decision")


class VerifyResponse(BaseModel):
    """Response model for image-task verification."""

    match: bool = Field(..., description="Whether the image matches the task")
    reason: str = Field(..., description="Explanation for the verification result")
    processing_time: float = Field(
        ..., ge=0.0, description="Processing time in seconds"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "match": True,
                "reason": "检测到图像中人员拥挤的情况。",
                "processing_time": 0.523,
            }
        }
    }
