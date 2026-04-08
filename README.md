# Docker Python App Template

A Python-first web application template for building APIs, scheduled jobs, scraping,
queues, and operational interfaces.  Optimised for fast iteration in GitHub Codespaces
and easy production deployment via Docker Swarm.

## Stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI (Python 3.12) |
| Templates | Jinja2 (server-rendered HTML) |
| Partial updates | htmx |
| Client interactions | Alpine.js |
| Database | SQLite (default) → Postgres-ready |
| ORM / migrations | SQLAlchemy 2.x + Alembic |
| Scheduled jobs | APScheduler |
| Container | Docker (python:3.12-slim) |
| Config / secrets | dotconfig + SOPS + age |
| Dev tooling | CLASI, rundbat |

## Quick Start (Codespaces or local)

```bash
# 1. Install Python dependencies and set up the environment
./scripts/install.sh

# 2. Start the dev server (with hot-reload)
./scripts/dev.sh
# → Open http://localhost:8000
```

## Development

```bash
# Run tests
python3 -m pytest tests/ -v

# Run linter
ruff check app/ tests/

# Create a new Alembic migration
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

## Production Deployment

See [docs/deployment.md](docs/deployment.md).

## Project Structure

```
app/
  main.py           # FastAPI entry point
  config.py         # Settings (pydantic-settings, reads .env)
  database.py       # SQLAlchemy engine + session factory
  models.py         # ORM models
  scheduler.py      # APScheduler jobs
  routers/
    health.py       # GET /api/health
    pages.py        # Server-rendered HTML pages
    counter.py      # Demo counter API (htmx target)
  templates/
    base.html       # Base layout (navbar, Alpine modal)
    index.html      # Home page
    partials/
      counter.html  # htmx-swapped counter widget
  static/
    css/app.css     # Application styles
alembic/            # Database migrations
  versions/
    0001_initial.py
tests/              # pytest test suite
config/             # dotconfig / SOPS config and secrets
docker/
  Dockerfile.app        # Production image
  Dockerfile.app.dev    # Dev image (hot-reload)
  entrypoint.sh         # Container entrypoint (runs migrations)
.devcontainer/      # Codespaces / VS Code devcontainer
scripts/
  install.sh        # First-time setup
  dev.sh            # Start dev server
```

## Extending the Template

- **Add a new page** → create a route in `app/routers/pages.py` and a Jinja2 template.
- **Add a new API** → add a router in `app/routers/`, register in `app/main.py`.
- **Add a new model** → add to `app/models.py`, run `alembic revision --autogenerate`.
- **Add a scheduled job** → register in `app/scheduler.py`.
- **Switch to Postgres** → set `DATABASE_URL=postgresql+asyncpg://...` in `.env` and add `asyncpg` to `requirements.txt`.
