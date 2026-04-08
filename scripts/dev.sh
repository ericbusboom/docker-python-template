#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Activate virtual environment if present
if [ -f .venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

# Load .env
set -a
# shellcheck disable=SC1091
. ./.env 2>/dev/null || true
set +a

# Ensure DB migrations are up to date
echo "Applying migrations..."
alembic upgrade head

# Start uvicorn with hot-reload
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}" --reload
