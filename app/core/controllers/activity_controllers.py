from typing import List
from datetime import datetime, timedelta
from pydantic import ValidationError
from requests import get

from app.core.models.activity_model import ActivityCollection, ActivityModel
from app.core.models.strava_token_model import StravaTokenModel
from app.factories.database import strava_tokens_collection, activities_collection
from app.utils.constants import DEFAULT_STRAVA_TOKEN_ID, STRAVA_ACTIVITIES_API_ENDPOINT, REQUEST_TIMEOUT
from app.utils.logger import logger


async def fetch_strava_activities_data(after: int = 0) -> List[ActivityModel]:
    """
        Fetches activities from Strava API after a given unix timestamp

        :param after: Unix timestamp of a past date
        :return: List of Strava activities
    """
    logger.info("Fetching activities from Strava API")
    try:
        # Fetch token from db
        token_data = await strava_tokens_collection.find_one({"_id": DEFAULT_STRAVA_TOKEN_ID})
        if not token_data:
            raise ValueError(f"No token with id = {DEFAULT_STRAVA_TOKEN_ID}")

        strava_token = StravaTokenModel.model_validate(token_data)
        if not strava_token.is_token_valid():
            await strava_token.refresh()

        # Fetch activities data from strava
        strava_activities = get(
            STRAVA_ACTIVITIES_API_ENDPOINT,
            headers={"Authorization": f"Bearer {strava_token.access_token}"},
            params={"after": after},
            timeout=REQUEST_TIMEOUT
        ).json()

        logger.info("Fetched %d activities", len(strava_activities))
        return strava_activities

    except ValidationError as e:
        logger.error("Token data failed validation: %s", e)
        raise RuntimeError("Invalid token data format") from e

    except ValueError as e:
        logger.error("Token error: %s", e)
        raise RuntimeError("Missing or invalid Strava token") from e


async def add_new_activities_to_db() -> List[ActivityModel]:
    logger.info("Attempting to add new activities to DB")
    try:
        # Get a date from a day ago
        current_date = datetime.now()
        date_in_past = current_date - timedelta(days=1)

        # Fetch recent activities from DB using past date
        query = {"start_date_local": {"$gte": date_in_past}}
        db_activity_data = await activities_collection.find(query).to_list(length=None)
        db_activity_data_dates = list(db_activity["start_date_local"] for db_activity in db_activity_data)

        # Fetch recent activities from Strava's API using past date
        strava_activities_data = await fetch_strava_activities_data(int(date_in_past.timestamp()))
        # Filter recent Strava activities not already in DB
        filtered_strava_activities = list(
            # TODO: filter by id instead of start_date_local
            filter(lambda activity: datetime.strptime(
                activity["start_date_local"], "%Y-%m-%dT%H:%M:%SZ"
            ) not in db_activity_data_dates,
                strava_activities_data
           )
        )

        if not filtered_strava_activities:
            logger.info("No new activities to upload")
            return []

        # Insert new activities into DB
        activity_data = []
        for strava_activity in filtered_strava_activities:
            activity_data.append({
                "strava_id": str(strava_activity["id"]),
                "name": strava_activity.get("name"),
                "distance": strava_activity.get("distance"),
                "moving_time": strava_activity.get("moving_time"),
                "elapsed_time": strava_activity.get("elapsed_time"),
                "total_elevation_gain": strava_activity.get("total_elevation_gain"),
                "sport_type": strava_activity.get("sport_type"),  # will be converted to SportType
                "start_date": strava_activity.get("start_date"),
                "start_date_local": strava_activity.get("start_date_local"),
                "timezone": strava_activity.get("timezone"),
                "upload_id": str(strava_activity.get("upload_id")) if strava_activity.get("upload_id") else None,
                "average_speed": strava_activity.get("average_speed"),
                "max_speed": strava_activity.get("max_speed"),
                "average_watts": strava_activity.get("average_watts"),
                "max_watts": strava_activity.get("max_watts"),
                "weighted_average_watts": strava_activity.get("weighted_average_watts"),
                "kilojoules": strava_activity.get("kilojoules"),
                "device_watts": strava_activity.get("device_watts"),
                "average_heartrate": strava_activity.get("average_heartrate"),
                "max_heartrate": strava_activity.get("max_heartrate"),
                "pr_count": strava_activity.get("pr_count"),
                "suffer_score": strava_activity.get("suffer_score"),
            })

        # Wrap list in a dict for ActivityCollection validation
        activities_collection_data = ActivityCollection.model_validate({"activities": activity_data})

        # Convert all activities to dictionaries once
        activities_dicts = [activity.model_dump() for activity in activities_collection_data.activities]

        # Insert the validated and dumped activities into the database
        await activities_collection.insert_many(activities_dicts)

        logger.info("Successfully inserted new activities to DB: %s", activities_dicts)
        return activities_dicts

    except (RuntimeError, TypeError, ValidationError, ValueError) as e:
        logger.error("Failed to insert new activities to DB: %s", e)
        raise RuntimeError from e
