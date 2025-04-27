from datetime import datetime, timedelta
from typing import List
from pydantic import ValidationError

from app.core.controllers.activity_controllers import fetch_strava_activities_data
from app.core.models.run_model import RunCollection, RunModel
from app.utils.logger import logger


async def add_new_runs_to_db(runs_collection) -> List[RunModel]:
    logger.info("Attempting to add new runs to DB")
    try:
        # Get a date from a day ago
        current_date = datetime.now()
        date_in_past = current_date - timedelta(days=1)

        # Fetch recent runs from DB using past date
        query = {"start_date_local": {"$gte": date_in_past}}
        db_run_data = await runs_collection.find(query).to_list(length=None)
        db_run_data_dates = list(db_run["start_date_local"] for db_run in db_run_data)

        # Fetch recent runs from Strava's API using past date
        strava_activities_data = await fetch_strava_activities_data(int(date_in_past.timestamp()))
        # TODO: filter by id instead of start_date_local
        filtered_strava_runs = list(filter(lambda activity: activity.get('type') == 'Run' and datetime.strptime(
                activity["start_date_local"], "%Y-%m-%dT%H:%M:%SZ"
            ) not in db_run_data_dates, strava_activities_data))

        if not filtered_strava_runs:
            logger.info("No new runs to upload")
            return []

        # Insert new runs into DB
        run_data = [{
            "distance": strava_run["distance"],
            "duration": strava_run["moving_time"],
            "start_date_local": strava_run["start_date_local"],
        } for strava_run in filtered_strava_runs]

        # Wrap list in a dict for RunCollection validation
        runs_collection_data = RunCollection.model_validate({"runs": run_data})

        # Convert all runs to dictionaries once
        runs_dicts = [run.model_dump() for run in runs_collection_data.runs]

        # Insert the validated and dumped runs into the database
        await runs_collection.insert_many(runs_dicts)

        logger.info("Successfully inserted new runs to DB: %s", runs_dicts)
        return runs_dicts

    except (RuntimeError, TypeError, ValidationError, ValueError) as e:
        logger.error("Failed to insert new runs to DB: %s", e)
        raise RuntimeError from e
