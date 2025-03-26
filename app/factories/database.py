from motor.motor_asyncio import AsyncIOMotorClient

from app.utils.config import settings


# Attempt to create a MongoDB client
mongo_client = AsyncIOMotorClient(settings.DB_URI)

# Attempt to get the database
db = mongo_client.get_database(settings.DB_NAME)

# Collections
runs_collection = db.get_collection("runs")
activities_collection = db.get_collection("activities")
strava_tokens_collection = db.get_collection("strava_tokens")
