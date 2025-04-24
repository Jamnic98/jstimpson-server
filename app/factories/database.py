from motor.motor_asyncio import AsyncIOMotorClient

from app.utils.config import settings
from app.utils.logger import logger


# Attempt to create a MongoDB client
logger.info("Connecting to MongoDB...")
mongo_client = AsyncIOMotorClient(settings.DB_URI)
logger.info("Database connection established")

# Attempt to get the database
db = mongo_client.get_database(settings.DB_NAME)

# Collections
runs_collection = db.get_collection("runs")
activities_collection = db.get_collection("activities")
strava_tokens_collection = db.get_collection("strava_tokens")
