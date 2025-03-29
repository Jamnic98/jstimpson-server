import asyncio
from fastapi.responses import JSONResponse

from app.core.controllers.run_controllers import add_new_runs_to_db


def handler(_event, _context):
    asyncio.run(add_new_runs_to_db())
    return JSONResponse("Strava update completed", 200)
