import os
from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.logger import logger


class Settings(BaseSettings):
    DB_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "dev_database"
    STRAVA_CLIENT_ID: Optional[str] = None
    STRAVA_CLIENT_SECRET: Optional[str] = None
    DEBUG: bool = False
    RELOAD: bool = False
    PORT: int = 8080

    # Dynamically determine the environment file
    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('ENV', 'dev')}",
        case_sensitive=True
    )

settings: Settings = Settings()

# function for dependency injection
@lru_cache()
def get_settings() -> Settings:
    logger.info("Using environment: %s", {os.getenv('ENV', 'dev')})
    return settings
