# Developer commands; run `make` or `make help` for the list.
.DEFAULT_GOAL := help

# Generated API contract lives with the frontend that consumes it
API_DIR := frontend/src/lib/api

# Runs a backend command in a throwaway uv container; schema export needs settings, not a database
BACKEND_RUN := docker run --rm --user "$$(id -u):$$(id -g)" \
	-e HOME=/tmp -e UV_CACHE_DIR=/tmp/uv-cache -e UV_PROJECT_ENVIRONMENT=/tmp/venv \
	-e DJANGO_SECRET_KEY=schema-export -e DATABASE_URL=postgres://unused@localhost/unused \
	-v "$(CURDIR)/backend":/app -w /app \
	ghcr.io/astral-sh/uv:python3.12-bookworm-slim uv run --frozen --quiet

.PHONY: help api

help: ## List available commands
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "} {printf "  %-10s %s\n", $$1, $$2}'

# Export to a temp file first so a failed export never truncates the committed schema
api: ## Regenerate the OpenAPI schema from Django Ninja and the TypeScript client types
	$(BACKEND_RUN) python manage.py export_openapi_schema --api config.api.api --indent 2 --sorted \
		> $(API_DIR)/openapi.json.tmp || { rm -f $(API_DIR)/openapi.json.tmp; exit 1; }
	mv $(API_DIR)/openapi.json.tmp $(API_DIR)/openapi.json
	npm --prefix frontend run --silent gen:api
