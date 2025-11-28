import asyncio

from app.core.controllers.run_controllers import add_new_runs_to_db
from app.factories.database import runs_collection

def handler(_event, _context):
    try:
        runs = asyncio.run(add_new_runs_to_db(runs_collection))
    except Exception as e:
        print("Failed to upload runs:", e)
        runs = []

    return {
        "statusCode": 200,
        "body": f"Uploaded {len(runs)} runs"
    }
