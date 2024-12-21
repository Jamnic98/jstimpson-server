from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.utils.logger import logger
from app.config import settings

try:
    # Attempt to create a MongoDB client
    mongo_client = AsyncIOMotorClient(settings.DB_URI)

    # Attempt to get the database
    db = mongo_client.get_database(settings.DB_NAME)

    # Check the connection by running a simple command
    mongo_client.admin.command('ping')  # This will raise an exception if the connection fails

    # Collections
    runs_collection = db.get_collection("runs")
    activities_collection = db.get_collection("activities")
    strava_tokens_collection = db.get_collection("strava_tokens")

    logger.info("Successfully connected to the database.")

except Exception as e:
    logger.error(f"Failed to connect to the database: {e}")
    # Raise a 500 Internal Server Error
    raise HTTPException(status_code=500, detail="Internal Server Error: Unable to connect to the database.")
