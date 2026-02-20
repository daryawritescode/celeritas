.PHONY: install lint test build run serve compose-up compose-down

install:
	poetry install

lint:
	poetry run ruff check .
	poetry run mypy src tests

test:
	poetry run pytest --cov=src --cov-report=term-missing

build:
	docker build -t celeritas .

run:
	poetry run python -m celeritas.cli.app run

serve:
	poetry run python -m celeritas.cli.app serve

compose-up:
	docker compose up -d

compose-down:
	docker compose down
