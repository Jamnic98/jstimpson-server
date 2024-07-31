import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "dev_database"
    STRAVA_CLIENT_ID: str = None
    STRAVA_CLIENT_SECRET: str = None
    REQUEST_TIMEOUT: int = 30  # seconds
    PORT: int = 8080

    class Config:
        env_file = ".env"


settings = Settings()

settings.DB_URI = os.getenv("DB_URI", "mongodb://localhost:27017")
settings.DB_NAME = os.getenv("DB_NAME", "dev_database")
settings.STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
settings.STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
settings.PORT = int(os.getenv("PORT", 8080))
