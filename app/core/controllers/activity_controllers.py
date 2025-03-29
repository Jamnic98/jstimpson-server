from datetime import datetime, timedelta

from pydantic import ValidationError
from requests import get

from app.factories.database import strava_tokens_collection, activities_collection
from app.core.models.activity_model import ActivityCollection
from app.core.models.strava_token_model import StravaTokenModel

from app.utils.logger import logger
from app.utils.constants import DEFAULT_STRAVA_TOKEN_ID, STRAVA_ACTIVITIES_API_ENDPOINT, REQUEST_TIMEOUT


async def fetch_strava_activities_data(after: int = 0) -> ActivityCollection | None:
    """
        Fetches activities from Strava API after a given unix timestamp

        :param after: Unix timestamp of a past date
        :return: List of Strava activities
    """
    logger.info("Fetching activities from Strava API")
    try:
        # fetch token from db
        token_data = await strava_tokens_collection.find_one({"_id": DEFAULT_STRAVA_TOKEN_ID})
        if not token_data:
            raise ValueError(f"Failed to find a token with id: {DEFAULT_STRAVA_TOKEN_ID}")

        strava_token = StravaTokenModel(**token_data)
        if not strava_token.is_token_valid():
            await strava_token.refresh()

        # fetch activities data from strava
        return get(
            STRAVA_ACTIVITIES_API_ENDPOINT,
            headers={"Authorization": f"Bearer {strava_token.access_token}"},
            params={"after": after},
            timeout=REQUEST_TIMEOUT
        ).json()

    except (ValidationError, ValueError) as e:
        logger.error("Failed to fetch Strava activities: %s", e)
        return None


async def add_new_activities_to_db() -> None:
    logger.info("Attempting to add new activities to DB")
    # get a date from a week ago
    current_date = datetime.now()
    date_in_past = current_date - timedelta(days=14)
    # create a query to get all activities from DB that are newer than the date in past
    query = {"start_date_local": {"$gt": date_in_past}}
    try:
        # fetch recent activities from Strava's API using past date
        strava_activities_data = await fetch_strava_activities_data(int(date_in_past.timestamp()))
        # fetch recent activities from DB using past date
        db_activity_data = await activities_collection.find(query).to_list(length=None)

        # filter recent Strava activities not already in DB
        filtered_strava_activities = list(
            # TODO: filter by id instead of start_date_local
            filter(lambda activity: datetime.strptime(
                activity["start_date_local"], "%Y-%m-%dT%H:%M:%SZ"
            ) not in (db_activity["start_date_local"] for db_activity in db_activity_data),
                strava_activities_data
            )
        )
        # add new activities to DB
        if filtered_strava_activities:
            # upload new activities to DB
            activity_data = []
            for strava_activity in filtered_strava_activities:
                activity_data.append({
                    "distance": strava_activity["distance"],
                    "duration": strava_activity["moving_time"],
                    "start_date_local": strava_activity["start_date_local"],
                })
            activities = ActivityCollection.model_validate(activity_data)
            await activities_collection.insert_many(activities)
            logger.info("Successfully inserted new activities to DB: %s", activities)
        else:
            logger.info("No new activities to upload")

    except (TypeError, ValidationError, ValueError) as e:
        logger.error("Failed to insert new activities to DB: %s", e)
