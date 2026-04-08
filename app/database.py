"""Database setup: SQLAlchemy 2.x async engine + session factory.

Default: SQLite (file-based, no server needed).
Set DATABASE_URL=postgresql+asyncpg://... for Postgres.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# Convert a sync sqlite:// URL to async sqlite+aiosqlite://
def _make_async_url(url: str) -> str:
    if url.startswith("sqlite:///"):
        return url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    return url


async_url = _make_async_url(settings.database_url)

engine = create_async_engine(
    async_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False} if "sqlite" in async_url else {},
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    """FastAPI dependency that yields a database session."""
    async with AsyncSessionLocal() as session:
        yield session
