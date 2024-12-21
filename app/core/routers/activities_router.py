from datetime import datetime
from fastapi import Query, HTTPException
from fastapi.routing import APIRouter

from app.core.models.activity_model import ActivityCollection
from app.factories.database import activities_collection
from app.utils.logger import logger

router = APIRouter(
    prefix="/activities"
)


@router.get("", response_model=ActivityCollection)
async def index(after: int = Query(None)):
    try:
        """
        Fetch activities from database

        Parameters:
            after (int): unix time stamp to filter activities after a certain date

        """
        logger.info("Fetching activities from database")
        query = {}
        if after:
            # convert timestamp from unix time
            query = {"start_date_local": {"$gt": datetime.fromtimestamp(after / 1000)}}

        # fetch and return the list of activities
        return ActivityCollection(
            activities=await activities_collection.find(query).to_list(length=None)
        ).model_dump()

    except RuntimeError:
        raise HTTPException(500, detail="Internal Server Error")
