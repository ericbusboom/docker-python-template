# Testing Guide

## Test Stack

| Tool | Purpose |
|---|---|
| pytest | Test runner |
| pytest-asyncio | Async test support |
| httpx (AsyncClient) | FastAPI test client |
| aiosqlite in-memory | Isolated test DB |

## Running Tests

```bash
# All tests
python3 -m pytest tests/ -v

# Single file
python3 -m pytest tests/test_app.py -v

# With coverage
python3 -m pytest tests/ --cov=app --cov-report=term-missing
```

## Fixtures (`tests/conftest.py`)

### `db_session`
Creates a fresh in-memory SQLite database for each test, applies the
SQLAlchemy schema, and yields an `AsyncSession`.  The session is rolled
back after each test.

### `client`
Returns an `httpx.AsyncClient` using `ASGITransport` (no network).
Overrides the `get_db` FastAPI dependency with the test `db_session`.

## Writing Tests

```python
import pytest

@pytest.mark.asyncio
async def test_my_endpoint(client):
    response = await client.get("/my-path")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_db_interaction(client, db_session):
    from app.models import MyModel
    from sqlalchemy import select

    # Set up test data
    db_session.add(MyModel(name="test"))
    await db_session.commit()

    # Test the endpoint
    response = await client.get("/api/my-model")
    assert response.status_code == 200
```

## Conventions

- Tests are in `tests/` (flat structure for small projects; add sub-dirs as needed)
- Each test function is `async` and decorated with `@pytest.mark.asyncio`
- Test DB is always in-memory SQLite — never touches the dev or prod database
- Tests do not test template rendering in detail; they check status codes and
  key strings in the HTML response body
