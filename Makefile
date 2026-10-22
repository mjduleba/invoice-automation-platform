# Developer commands; run `make` or `make help` for the list.
.DEFAULT_GOAL := help

# Generated API contract lives with the frontend that consumes it
API_DIR := frontend/src/lib/api

# One-off backend command in the dev image; --no-deps since not every command needs the database
BACKEND_RUN := docker compose run --rm --no-deps -T backend

.PHONY: help up down logs migrate shell api

help: ## List available commands
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "} {printf "  %-10s %s\n", $$1, $$2}'

up: ## Build and start Postgres, Django, Vite and Mailpit; app at http://localhost:5173
	docker compose up --build

down: ## Stop all services (data volumes are kept)
	docker compose down

logs: ## Follow logs from all services
	docker compose logs -f

migrate: ## Apply Django migrations
	docker compose run --rm backend python manage.py migrate

shell: ## Open a Django shell
	docker compose run --rm backend python manage.py shell

# Export to a temp file first so a failed export never truncates the committed schema
api: ## Regenerate the OpenAPI schema from Django Ninja and the TypeScript client types
	$(BACKEND_RUN) python manage.py export_openapi_schema --api config.api.api --indent 2 --sorted \
		> $(API_DIR)/openapi.json.tmp || { rm -f $(API_DIR)/openapi.json.tmp; exit 1; }
	mv $(API_DIR)/openapi.json.tmp $(API_DIR)/openapi.json
	npm --prefix frontend run --silent gen:api
