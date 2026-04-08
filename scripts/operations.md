# Operations Reference

Commands agents can run when asked. These are not in a Makefile because
humans don't type them — agents execute them directly.

## Dev Server

### Native (recommended for Codespaces)

```bash
./scripts/dev.sh
# → http://localhost:8000
```

Activates `.venv`, loads `.env`, applies migrations, starts uvicorn with `--reload`.

### Full Docker stack

```bash
set -a && . ./.env && set +a
DOCKER_CONTEXT=$DEV_DOCKER_CONTEXT docker compose -f docker-compose.dev.yml up --build
```

Stop:
```bash
DOCKER_CONTEXT=$DEV_DOCKER_CONTEXT docker compose -f docker-compose.dev.yml down
```

## Database

### Apply migrations

```bash
alembic upgrade head
```

### Create a new migration (after changing app/models.py)

```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```

### Roll back one step

```bash
alembic downgrade -1
```

### Show current revision

```bash
alembic current
```

### Show migration history

```bash
alembic history --verbose
```

## Build

### Build production Docker image

```bash
docker build -f docker/Dockerfile.app -t python-app:${TAG:-latest} .
```

### Build dev Docker image

```bash
docker build -f docker/Dockerfile.app.dev -t python-app-dev:latest .
```

## Testing

### Run all tests

```bash
python3 -m pytest tests/ -v
```

### Run with coverage

```bash
python3 -m pytest tests/ --cov=app --cov-report=term-missing
```

### Run a single test file

```bash
python3 -m pytest tests/test_app.py -v
```

## Linting

```bash
ruff check app/ tests/
ruff format app/ tests/
```

## Deploy

See `scripts/deploy.sh` and [docs/deployment.md](../docs/deployment.md).
