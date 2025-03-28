from datetime import datetime, timedelta
from pydantic import ValidationError

from app.utils.logger import logger
from app.core.models.run_model import RunModel
from app.factories.database import runs_collection
from app.core.controllers.activity_controllers import fetch_strava_activities_data


async def add_new_runs_to_db() -> None:
    logger.info("Attempting to add new runs to DB")
    # get a date from a week ago
    current_date = datetime.now()
    date_in_past = current_date - timedelta(days=14)
    # create a query to get all runs from DB that are newer than the date in past
    query = {"start_date_local": {"$gt": date_in_past}}
    try:
        # fetch recent runs from Strava's API using past date
        strava_runs_data = await fetch_strava_activities_data(int(date_in_past.timestamp()))
        # fetch recent runs from DB using past date
        db_run_data = await runs_collection.find(query).to_list(length=None)
        db_run_data_dates = list(db_run["start_date_local"] for db_run in db_run_data)

        # filter recent Strava runs not already in DB
        filtered_strava_runs = list(
            # TODO: filter by id instead of start_date_local
            filter(lambda activity: datetime.strptime(
                activity["start_date_local"], "%Y-%m-%dT%H:%M:%SZ"
            ) not in db_run_data_dates,
                strava_runs_data
            )
        )
        # add new runs to DB
        if filtered_strava_runs:
            # upload new runs to DB
            run_data = []
            for strava_run in filtered_strava_runs:
                run_data.append(RunModel.model_validate({
                        "distance": strava_run["distance"],
                        "duration": strava_run["moving_time"],
                        "start_date_local": strava_run["start_date_local"],
                    }).model_dump()
                )
            await runs_collection.insert_many(run_data)
            logger.info("Successfully inserted new runs to DB: %s", run_data)
        else:
            logger.info("No new runs to upload")

    except (TypeError, ValidationError, ValueError) as e:
        logger.error("Failed to add new runs to DB: %s", e)
