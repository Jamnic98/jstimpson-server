from datetime import datetime
from fastapi import Query, HTTPException
from fastapi.routing import APIRouter
from pymongo.errors import PyMongoError

from app.utils.logger import logger
from app.factories.database import runs_collection
from app.core.models.run_model import RunCollection


router = APIRouter(prefix="/runs")


@router.get("", response_model=RunCollection)
async def index(after: int = Query(None)):
    """
    Fetch runs from the database.

    Parameters:
        after (int): Unix timestamp in milliseconds to filter runs after a certain date.

    Returns:
        RunCollection: A collection of runs.
    """
    logger.info("Fetching runs from database")
    if after is not None and after < 0:
        raise HTTPException(status_code=400, detail="Invalid timestamp: must be a positive integer.")

    try:
        query = {}
        if after:
            # Convert timestamp from Unix time (milliseconds)
            query = {"start_date_local": {"$gt": datetime.fromtimestamp(after / 1000)}}

        # Fetch and return the list of runs
        runs = await runs_collection.find(query).to_list(length=None)
        return RunCollection(runs=runs).model_dump()

    except PyMongoError as e:
        logger.error("Database error occurred: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error: Database operation failed.") from e

    except (RuntimeError, Exception) as e:
        logger.error("Unexpected error occurred: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error: An unexpected error occurred.") from e
