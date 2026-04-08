"""Counter API routes — called by htmx for partial HTML updates."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Counter

router = APIRouter(prefix="/api/counter")
templates = Jinja2Templates(directory="app/templates")


async def _get_or_create_counter(db: AsyncSession, name: str = "default") -> Counter:
    result = await db.execute(select(Counter).where(Counter.name == name))
    counter = result.scalar_one_or_none()
    if counter is None:
        counter = Counter(name=name, value=0)
        db.add(counter)
        await db.commit()
        await db.refresh(counter)
    return counter


@router.post("/increment", response_class=HTMLResponse)
async def increment(request: Request, db: AsyncSession = Depends(get_db)):
    """Increment the default counter and return the updated partial."""
    counter = await _get_or_create_counter(db)
    counter.value += 1
    await db.commit()
    await db.refresh(counter)
    return templates.TemplateResponse(
        request,
        "partials/counter.html",
        {"counter": counter},
    )


@router.post("/reset", response_class=HTMLResponse)
async def reset(request: Request, db: AsyncSession = Depends(get_db)):
    """Reset the default counter and return the updated partial."""
    counter = await _get_or_create_counter(db)
    counter.value = 0
    await db.commit()
    await db.refresh(counter)
    return templates.TemplateResponse(
        request,
        "partials/counter.html",
        {"counter": counter},
    )


@router.get("/value", response_class=HTMLResponse)
async def get_value(request: Request, db: AsyncSession = Depends(get_db)):
    """Return the current counter partial (used by hx-get polling)."""
    counter = await _get_or_create_counter(db)
    return templates.TemplateResponse(
        request,
        "partials/counter.html",
        {"counter": counter},
    )
