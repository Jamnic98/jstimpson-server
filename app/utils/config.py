from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str = "dev_database"
    DB_URI: str = "mongodb://localhost:27017"
    DEBUG: bool = True
    PORT: int = 8080
    RELOAD: bool = True
    STRAVA_CLIENT_ID: Optional[str] = None
    STRAVA_CLIENT_SECRET: Optional[str] = None

    model_config = SettingsConfigDict(env_file='.env.local', case_sensitive=True)

settings: Settings = Settings()
