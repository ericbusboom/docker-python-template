"""FastAPI application entry point.

Stack:
  - FastAPI  (web framework)
  - SQLAlchemy 2.x async  (ORM)
  - Alembic  (migrations — run separately via `alembic upgrade head`)
  - APScheduler  (background cron jobs)
  - Jinja2  (server-rendered HTML templates)
  - htmx + Alpine.js  (served as static assets)
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine
from app.routers import counter, health, pages
from app.scheduler import setup_scheduler

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    # Ensure the data directory exists (SQLite)
    if settings.database_url.startswith("sqlite"):
        db_path = settings.database_url.replace("sqlite:///", "").replace("sqlite+aiosqlite:///", "")
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)

    # Start scheduler
    scheduler = setup_scheduler()
    scheduler.start()
    logger.info("Scheduler started")

    yield

    # Shutdown
    scheduler.shutdown()
    await engine.dispose()
    logger.info("Shutdown complete")


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

# Static files (CSS, htmx, Alpine.js)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers
app.include_router(health.router)
app.include_router(pages.router)
app.include_router(counter.router)
