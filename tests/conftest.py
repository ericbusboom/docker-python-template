"""Shared test fixtures."""

import os
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Override settings before importing app modules
os.environ.setdefault("DATABASE_URL", "sqlite:///./data/test.db")


@pytest_asyncio.fixture
async def db_session():
    """Create an in-memory DB, apply schema, yield a session."""
    from app.database import Base

    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionFactory = async_sessionmaker(engine, expire_on_commit=False)
    async with SessionFactory() as session:
        yield session
        await session.rollback()

    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session):
    """Return an AsyncClient wired to the FastAPI app with the test DB session."""
    from app.main import app
    from app.database import get_db

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
