# Docker Python App Template Specification

> This document describes the **template** — the starting point you get when you
> create a new project from this repository. Actual applications built from
> the template may diverge from the defaults described here.

---

## 1. Overview

This template provides a fully containerised, Python-first application stack.
It is designed for:

- REST APIs and background processing
- Scheduled / cron jobs
- Web scraping and data pipelines
- Video processing and media workflows
- Modest operational / admin interfaces

It is **not** designed for rich single-page applications.  If you need a complex
client UI, use the separate `docker-node-template` instead.

| Component | Technology | Location |
|---|---|---|
| Backend | FastAPI (Python 3.12) | `app/` |
| Templates | Jinja2 (server-rendered HTML) | `app/templates/` |
| Partial updates | htmx | CDN / static |
| Client interactions | Alpine.js | CDN / static |
| Database | SQLite (default) / Postgres | `data/` |
| ORM / Migrations | SQLAlchemy 2.x + Alembic | `alembic/` |
| Scheduled jobs | APScheduler | `app/scheduler.py` |
| Container | Docker (python:3.12-slim) | `docker/` |
| Config / secrets | dotconfig + SOPS + age | `config/` |

---

## 2. Repository Layout

```
.
├── CLAUDE.md                     # AI agent configuration
├── AGENTS.md                     # Agent behavioural rules
├── README.md                     # Quick start
├── .devcontainer/                # Codespace / VS Code config
├── .mcp.json                     # CLASI MCP server config
├── alembic.ini                   # Alembic configuration
├── pytest.ini                    # pytest configuration
├── requirements.txt              # Production Python dependencies
├── requirements-dev.txt          # Dev / test dependencies
├── docker-compose.yml            # Production Swarm stack
├── docker-compose.dev.yml        # Docker dev environment
├── app/
│   ├── main.py                   # FastAPI entry point + lifespan
│   ├── config.py                 # pydantic-settings configuration
│   ├── database.py               # Async SQLAlchemy engine + session
│   ├── models.py                 # SQLAlchemy ORM models
│   ├── scheduler.py              # APScheduler job registration
│   ├── routers/
│   │   ├── health.py             # GET /api/health
│   │   ├── pages.py              # Server-rendered HTML routes
│   │   └── counter.py            # Demo counter (htmx target)
│   ├── templates/
│   │   ├── base.html             # Base layout (navbar, modals)
│   │   ├── index.html            # Home page
│   │   └── partials/
│   │       └── counter.html      # htmx-swapped counter widget
│   └── static/
│       └── css/app.css           # Application CSS
├── alembic/
│   ├── env.py                    # Alembic async env config
│   ├── script.py.mako            # Migration template
│   └── versions/
│       └── 0001_initial.py       # Initial schema
├── tests/
│   ├── conftest.py               # pytest fixtures (in-memory DB)
│   └── test_app.py               # FastAPI endpoint tests
├── config/
│   ├── rundbat.yaml              # rundbat project config
│   ├── sops.yaml                 # SOPS encryption policy
│   ├── dev/
│   │   ├── public.env            # Non-secret dev config
│   │   ├── secrets.env           # SOPS-encrypted dev secrets
│   │   └── secrets.env.example   # Required secrets template
│   └── prod/
│       ├── public.env            # Non-secret prod config
│       ├── secrets.env           # SOPS-encrypted prod secrets
│       └── secrets.env.example   # Required secrets template
├── docker/
│   ├── Dockerfile.app            # Production multi-stage image
│   ├── Dockerfile.app.dev        # Dev image (hot-reload)
│   └── entrypoint.sh             # Container entrypoint (migrations + start)
├── scripts/
│   ├── install.sh                # First-time setup
│   └── dev.sh                    # Start dev server
└── docs/                         # Human-facing documentation
```

---

## 3. Technology Choices

### FastAPI
- Async-first, type-annotated, OpenAPI docs at `/docs`
- Dependency injection for DB sessions, settings, auth

### SQLAlchemy 2.x (async)
- `AsyncSession` + `async_sessionmaker` for non-blocking DB access
- `DeclarativeBase` ORM with typed `Mapped` columns
- SQLite default (`sqlite+aiosqlite://`) — swap `DATABASE_URL` for Postgres

### Alembic
- Migrations in `alembic/versions/`
- `env.py` reads `DATABASE_URL` from app settings
- Run `alembic revision --autogenerate` after model changes

### APScheduler
- `AsyncIOScheduler` integrates with FastAPI's async event loop
- Started/stopped in the FastAPI `lifespan` context manager
- Register jobs in `app/scheduler.py`

### Jinja2 + htmx + Alpine.js
- Pages are server-rendered HTML — no JavaScript build step
- htmx handles server-driven partial updates (AJAX without writing JS)
- Alpine.js for local UI state (modals, toggles, tabs)
- htmx and Alpine.js loaded from CDN in development; bundle locally for production

### dotconfig + SOPS + age
- `config/dev/public.env` — non-secret config, committed
- `config/dev/secrets.env` — SOPS-encrypted, committed
- `config/local/` — developer overrides, gitignored
- `.env` — assembled at install time, gitignored

---

## 4. Development Workflow

```
./scripts/install.sh   # Once: venv, deps, DB, .env
./scripts/dev.sh       # Daily: start hot-reload server
alembic upgrade head   # After pulling new migrations
alembic revision --autogenerate -m "..."   # After model changes
python3 -m pytest tests/ -v               # Run tests
ruff check app/ tests/                    # Lint
```

---

## 5. Docker

### Dev
```bash
docker compose -f docker-compose.dev.yml up --build
```

### Production
```bash
docker build -f docker/Dockerfile.app -t myapp:latest .
TAG=v1 docker stack deploy -c docker-compose.yml myapp
```
