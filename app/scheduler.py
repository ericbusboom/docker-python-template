"""APScheduler background scheduler.

Register periodic jobs here; the scheduler is started/stopped alongside
the FastAPI lifespan.
"""

import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def _heartbeat_job() -> None:
    """Example cron job — logs a heartbeat every minute."""
    logger.info("Scheduler heartbeat")


def setup_scheduler() -> AsyncIOScheduler:
    """Register all periodic jobs and return the scheduler."""
    scheduler.add_job(
        _heartbeat_job,
        trigger=IntervalTrigger(minutes=1),
        id="heartbeat",
        replace_existing=True,
    )
    return scheduler
