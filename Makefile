.PHONY: build up down lint test run serve help

DC = docker compose

help:
	@echo "Available targets:"
	@echo "  run        Execute a single speedtest run"
	@echo "  serve      Start the web dashboard"
	@echo ""
	@echo "Utility targets:"
	@echo "  build      Build container images"
	@echo "  up         Start application in background"
	@echo "  down       Stop all services"
	@echo "  lint       Run linting (ruff, mypy)"
	@echo "  test       Run tests with 100% coverage"
	@echo "  docs       Preview documentation locally"

build:
	$(DC) build

up:
	$(DC) up -d

down:
	$(DC) down

lint:
	$(DC) run --rm dev poetry run ruff check .
	$(DC) run --rm dev poetry run mypy src tests

test:
	$(DC) run --rm dev poetry run pytest --cov=src --cov-report=term-missing

run:
	$(DC) run --rm celeritas poetry run celeritas run

docs:
	$(DC) run --rm dev poetry run mkdocs serve -a 0.0.0.0:8000

serve:
	$(DC) up celeritas
