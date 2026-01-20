"""Configuration management using Pydantic Settings."""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # VLM Service Configuration
    VLM_BASE_URL: str = "http://localhost:8001/v1"
    VLM_MODEL_NAME: str = "Qwen/Qwen2-VL-7B-Instruct"
    VLM_TIMEOUT: float = 120.0
    VLM_MAX_RETRIES: int = 2

    # API Configuration
    MAX_CONCURRENT_REQUESTS: int = 10

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_JSON: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
