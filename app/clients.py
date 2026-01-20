"""VLM client for interacting with Qwen3-VL service."""

from openai import AsyncOpenAI
from loguru import logger
from app.config import get_settings


class VLMClient:
    """Client for VLM service using OpenAI-compatible API."""

    def __init__(self):
        """Initialize VLM client."""
        self.client = None
        self.settings = get_settings()

    def initialize(self) -> None:
        """Initialize the OpenAI client."""
        self.client = AsyncOpenAI(
            base_url=self.settings.VLM_BASE_URL,
            api_key="EMPTY",  # vLLM doesn't require a real API key
            timeout=self.settings.VLM_TIMEOUT,
            max_retries=self.settings.VLM_MAX_RETRIES,
        )
        logger.info(
            f"VLM client initialized with base_url={self.settings.VLM_BASE_URL}"
        )

    async def close(self) -> None:
        """Close the client connection."""
        if self.client:
            await self.client.close()
            logger.info("VLM client closed")


# Global client instance
vlm_client = VLMClient()
