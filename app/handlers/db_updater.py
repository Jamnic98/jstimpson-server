import asyncio

from app.core.controllers.run_controllers import add_new_runs_to_db


def handler():
    asyncio.run(add_new_runs_to_db())
    return {"statusCode": 200, "body": "Strava update completed"}
