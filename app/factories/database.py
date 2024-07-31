from motor import motor_asyncio

from app.config import settings

mongo_client = motor_asyncio.AsyncIOMotorClient(settings.DB_URI)
db = mongo_client.get_database(settings.DB_NAME)

# collections
runs_collection = db.get_collection("runs")
activities_collection = db.get_collection("activities")
strava_tokens_collection = db.get_collection("strava_tokens")
