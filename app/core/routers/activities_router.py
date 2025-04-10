from datetime import datetime
from fastapi import Query, HTTPException
from fastapi.routing import APIRouter
from pymongo.errors import PyMongoError

from app.utils.logger import logger
from app.core.models.activity_model import ActivityCollection
from app.factories.database import activities_collection


router = APIRouter(
    prefix="/activities"
)


@router.get("", response_model=ActivityCollection)
async def index(after: int = Query(None)):
    """
    Fetch activities from database

    Parameters:
        after (int): unix time stamp to filter activities after a certain date

    """
    logger.info("Fetching activities from database")
    if after is not None and after < 0:
        raise HTTPException(status_code=400, detail="Invalid timestamp: must be a positive integer.")

    try:
        query = {}
        if after:
            # convert timestamp from unix time
            query = {"start_date_local": {"$gt": datetime.fromtimestamp(after / 1000)}}

        # fetch and return the list of activities
        return ActivityCollection(
            activities=await activities_collection.find(query).to_list(length=None)
        ).model_dump()

    except PyMongoError as e:
        logger.error("Database error occurred: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error: Database operation failed.") from e

    except (RuntimeError, Exception) as e:
        logger.error("Unexpected error occurred: %s", e)
        raise HTTPException(500, detail="Internal Server Error") from e
