from datetime import datetime
from fastapi import Query
from fastapi.routing import APIRouter

from app.factories.logger import logger
from app.factories.database import runs_collection
from app.core.models.run_model import RunCollection


router = APIRouter(
    prefix="/runs"
)


@router.get("", response_model=RunCollection)
async def index(after: int = Query(None)):
    """
    Fetch runs from database

    Parameters:
        after (int): unix time stamp to filter runs after a certain date

    """
    logger.info("Fetching runs from database")
    query = {}
    if after:
        # convert timestamp from unix time
        query = {"start_date_local": {"$gt": datetime.fromtimestamp(after / 1000)}}

    # fetch and return the list of runs
    return RunCollection(
        runs=await runs_collection.find(query).to_list(length=None)
    ).model_dump()
