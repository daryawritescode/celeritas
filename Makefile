.PHONY: build-dev lint test build run serve compose-up compose-down

build-dev:
	docker compose build dev

lint: build-dev
	docker compose run --rm dev poetry run ruff check .
	docker compose run --rm dev poetry run mypy src tests

test: build-dev
	docker compose run --rm dev poetry run pytest --cov=src --cov-report=term-missing

build:
	docker compose build celeritas

run: build
	docker compose run --rm celeritas poetry run python -m celeritas.cli.app run

serve: build
	docker compose run --rm --service-ports celeritas poetry run python -m celeritas.cli.app serve

compose-up:
	docker compose up -d celeritas

compose-down:
	docker compose down
