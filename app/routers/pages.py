"""Page routers — server-rendered HTML responses using Jinja2 templates."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Counter

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: AsyncSession = Depends(get_db)):
    """Home page with counter demo."""
    result = await db.execute(select(Counter).where(Counter.name == "default"))
    counter = result.scalar_one_or_none()
    if counter is None:
        counter = Counter(name="default", value=0)
        db.add(counter)
        await db.commit()
        await db.refresh(counter)

    return templates.TemplateResponse(
        request,
        "index.html",
        {"counter": counter},
    )
