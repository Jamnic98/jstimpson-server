import os
from typing import ClassVar, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Default settings
    DB_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "dev_database"
    STRAVA_CLIENT_ID: Optional[str] = None
    STRAVA_CLIENT_SECRET: Optional[str] = None
    DEBUG: bool = True
    RELOAD: bool = True
    PORT: int = 8080

    # Dynamically determine the environment file
    env_file: ClassVar[str] = f".env.{os.getenv('ENV', 'dev')}"

    # Check if the file exists, if not, log a warning or handle it
    if not os.path.exists(env_file):
        print(f"Warning: Environment file '{env_file}' not found. Default settings will be used")

    model_config = SettingsConfigDict(
        env_file=env_file,
        case_sensitive=True
    )


settings: Settings = Settings()
