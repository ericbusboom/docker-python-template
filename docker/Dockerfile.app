# Multi-stage production build for Python FastAPI app
# Usage: docker build -f docker/Dockerfile.app -t myapp:latest .

# ── Stage 1: Build / install dependencies ─────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a separate prefix for copying
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Slim runtime ─────────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Copy startup scripts
COPY docker/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Create data directory for SQLite
RUN mkdir -p /app/data

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
