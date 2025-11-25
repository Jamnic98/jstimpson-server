import asyncio
from http import HTTPStatus
from pydantic import ValidationError

from app.core.controllers.activity_controllers import add_new_activities_to_db
from app.core.controllers.run_controllers import add_new_runs_to_db
from app.factories.database import runs_collection
from app.utils.logger import logger


def handler(_event, _context):
    runs_result, activities_result = [], []

    # Handle runs
    try:
        runs_result = asyncio.run(add_new_runs_to_db(runs_collection))
    except (RuntimeError, TypeError, ValidationError, ValueError) as e:
        logger.error("Failed to upload runs: %s", e)

    # Handle activities independently
    try:
        activities_result = asyncio.run(add_new_activities_to_db())
    except (RuntimeError, TypeError, ValidationError, ValueError) as e:
        logger.error("Failed to upload activities: %s", e)

    # Prepare response
    if not runs_result and not activities_result:
        return {
            "statusCode": HTTPStatus.OK,
            "body": "No new runs or activities to upload."
        }

    return {
        "statusCode": HTTPStatus.OK,
        "body": f"Successfully uploaded {len(runs_result)} runs and {len(activities_result)} activities"
    }
