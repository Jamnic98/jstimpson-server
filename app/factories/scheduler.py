import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.utils.run_utils import add_new_runs_to_db


def create_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        add_new_runs_to_db,
        CronTrigger(hour=0, minute=0, timezone=pytz.timezone("Europe/London")),
        # TODO: removes
        # trigger='interval',
        # seconds=4
    )
    return scheduler
