from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "dev_database"
    STRAVA_CLIENT_ID: Optional[str] = None
    STRAVA_CLIENT_SECRET: Optional[str] = None
    DEBUG: bool = True
    RELOAD: bool = True
    PORT: int = 8080

    model_config = SettingsConfigDict(case_sensitive=True)

settings: Settings = Settings()
