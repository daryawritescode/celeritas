# Celeritas

Celeritas is a containerized speedtest and network metric utility written in modern Python using FastAPI and Typer.

## Features

- Run speedtests natively.
- Measure gateway and DNS latency.
- Command-line interface.
- Vibrant modern Web Dashboard with Polling.
- Full local SQLite History tracked dynamically via Chart.js.

## Running the application

```bash
# Execute CLI speedtest
poetry run celeritas run

# Or using the makefile
make run

# Start Dashboard server
make serve
```

## Docker Compose Build

Start the container and the application will be routed automatically through Traefik at [http://celeritas.localhost](http://celeritas.localhost).

```bash
docker compose up -d
```
