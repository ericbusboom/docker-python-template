# Testing Rules

When writing or modifying tests, follow these rules.

## Framework

| Tool | Purpose |
|---|---|
| pytest | Test runner |
| pytest-asyncio | Async test support (`asyncio_mode = auto`) |
| httpx AsyncClient | FastAPI test client (no network) |
| aiosqlite in-memory | Isolated test database |

## Fixtures

Use the shared fixtures in `tests/conftest.py`:

- `db_session` — fresh in-memory SQLite, schema applied, rolled back after test
- `client` — `httpx.AsyncClient` with `get_db` overridden to use `db_session`

## Writing Tests

```python
import pytest

@pytest.mark.asyncio
async def test_my_endpoint(client):
    response = await client.get("/my-path")
    assert response.status_code == 200
```

## Database Assertions

When a route modifies data, assert both the HTTP response AND query
the database directly via `db_session`:

```python
from app.models import MyModel
from sqlalchemy import select

async def test_creates_record(client, db_session):
    await client.post("/api/items", json={"name": "Test"})
    result = await db_session.execute(select(MyModel).where(MyModel.name == "Test"))
    assert result.scalar_one_or_none() is not None
```

## File Naming

- `tests/test_<feature>.py` — flat structure for small projects
- Add sub-directories (`tests/api/`, `tests/services/`) as the project grows

## Coverage Requirements

- Every new API route gets at least a happy-path test and an error test.
- Run `python3 -m pytest tests/ -v` after any backend change.
- All tests must pass before a ticket is marked done.

## No Global State

Tests must not depend on order.  Use fresh fixtures per test.
Never commit a `.db` file or leave state in `data/` between runs.
