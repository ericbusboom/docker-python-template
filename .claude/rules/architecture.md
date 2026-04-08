# Architecture Rules

## Routers Are Thin

Business logic lives in service modules (`app/services/`), not in
route handlers.  Routers validate input, call a service function, and
return the response.

## API Conventions

- All JSON API routes are prefixed with `/api`
- HTML routes return full pages or htmx partials (no prefix)
- Standard HTTP status codes
- FastAPI dependency injection for DB sessions and settings
- Raise `HTTPException` for expected errors; let the global exception
  handler deal with unexpected ones

## Database Philosophy

SQLite is the default.  Before reaching for additional services:

- Need document/schemaless data? Use a JSON column.
- Need a job queue? Use a database table with `SELECT ... FOR UPDATE SKIP LOCKED` (Postgres).
- Need full-text search? Use SQLite FTS5 or Postgres `tsvector`.

**Do not add Redis or MongoDB** without stakeholder discussion.

## SQLite → Postgres Migration Path

- Always use `DATABASE_URL` — never hardcode the connection string.
- Use SQLAlchemy ORM methods, not raw SQL.
- When raw SQL is unavoidable, check the dialect and branch:
  ```python
  from sqlalchemy import inspect
  if inspect(engine).dialect.name == "sqlite":
      ...
  ```
- Add `asyncpg` to `requirements.txt` and set `DATABASE_URL=postgresql+asyncpg://...`
  to switch to Postgres.

## htmx vs Alpine.js vs Full Page

| Use case | Approach |
|---|---|
| Initial page load | FastAPI route + Jinja2 template |
| Server data update | htmx (`hx-post`, `hx-get`) → returns HTML partial |
| Local UI state | Alpine.js (`x-data`, `@click`, `x-show`) |
| Complex SPA | Use the `docker-node-template` instead |

## Integrations Degrade Gracefully

Optional integrations must not prevent the app from starting.  Check
for required secrets at startup and log a warning if missing; return
**501** from the relevant endpoint.
