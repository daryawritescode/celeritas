.PHONY: build-dev lint test build run serve compose-up compose-down

build-dev:
	docker build --build-arg INSTALL_DEV=true -t celeritas:dev .

lint: build-dev
	docker run --rm celeritas:dev poetry run ruff check .
	docker run --rm celeritas:dev poetry run mypy src tests

test: build-dev
	docker run --rm celeritas:dev poetry run pytest --cov=src --cov-report=term-missing

build:
	docker build -t celeritas:latest .

run: build
	docker run --rm --network host celeritas:latest poetry run python -m celeritas.cli.app run

serve: build
	docker run --rm -p 8000:8000 celeritas:latest poetry run python -m celeritas.cli.app serve

compose-up:
	docker compose up -d

compose-down:
	docker compose down
