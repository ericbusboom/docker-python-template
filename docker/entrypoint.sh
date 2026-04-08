#!/bin/sh
set -e

# Load each Docker Swarm secret file as an environment variable.
# File name maps to variable name (uppercased).
# e.g. /run/secrets/database_url -> $DATABASE_URL
for secret_file in /run/secrets/*; do
  if [ -f "$secret_file" ]; then
    var_name=$(basename "$secret_file" | tr '[:lower:]' '[:upper:]')
    export "$var_name"="$(cat "$secret_file")"
  fi
done

# Run database migrations before starting the server
echo "Running database migrations..."
alembic upgrade head

echo "Starting application..."
exec "$@"
