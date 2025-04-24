import asyncio
from http import HTTPStatus
from pydantic import ValidationError

from app.core.controllers.run_controllers import add_new_runs_to_db
from app.factories.database import runs_collection


def handler(_event, _context):
    try:
        response = asyncio.run(add_new_runs_to_db(runs_collection))
        if not response:
            return {
                "statusCode": HTTPStatus.OK,
                "body": "No data to upload."
            }

        return {
            "statusCode": HTTPStatus.OK,
            "body": f"Successfully uploaded {len(response)} runs"
        }

    except (RuntimeError, TypeError, ValidationError, ValueError):
        return {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": "Failed to upload run data to database"
        }
