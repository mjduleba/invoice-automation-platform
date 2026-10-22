# syntax=docker/dockerfile:1

# ---- Frontend build: SvelteKit SPA compiled to static files ----
FROM node:24-slim AS frontend-build
WORKDIR /frontend
# Install from the lockfile first so dependency layers cache across source edits
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

# ---- Python base: runtime dependencies only ----
FROM python:3.12-slim AS base
COPY --from=ghcr.io/astral-sh/uv:0.12.23 /uv /uvx /bin/
# Venv outside /app so the dev bind mount never hides it
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY backend/pyproject.toml backend/uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-install-project

# ---- Dev: adds test, lint and type tools; Compose bind-mounts the source ----
FROM base AS dev
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-install-project
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ---- Prod: app code plus built SPA, served by gunicorn on Cloud Run's $PORT ----
FROM base AS prod
COPY backend/ ./
COPY --from=frontend-build /frontend/build ./frontend_build
# collectstatic only reads settings; placeholder values never reach runtime
RUN DJANGO_SECRET_KEY=collectstatic DATABASE_URL=postgres://unused@localhost/unused \
    python manage.py collectstatic --noinput
RUN useradd --system --create-home --uid 10001 app
USER app
ENV PORT=8080
# One worker keeps Postgres connections low on the 1 GB VM; threads cover concurrent requests
CMD exec gunicorn config.wsgi --bind "0.0.0.0:${PORT}" \
    --workers "${WEB_CONCURRENCY:-1}" --threads "${GUNICORN_THREADS:-8}" --timeout 0
