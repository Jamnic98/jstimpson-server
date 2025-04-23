import asyncio
from http import HTTPStatus
from pydantic import ValidationError

from app.core.controllers.run_controllers import add_new_runs_to_db
from app.factories.database import runs_collection


async def handler(_event, _context):
    try:
        response = await add_new_runs_to_db(runs_collection)
        if response:
            return {"statusCode": HTTPStatus.OK, "body": f"Successfully uploaded {len(response)} runs"}

    except (RuntimeError, TypeError, ValidationError, ValueError) as e:
        return {"statusCode": HTTPStatus.INTERNAL_SERVER_ERROR, "body": f"Failed to upload run data to database: {e}"}


# For local invocation
if __name__ == "__main__":
    event = {}
    context = {}
    asyncio.run(handler(event, context))
