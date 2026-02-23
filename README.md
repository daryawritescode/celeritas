# Celeritas ⚡

Celeritas is a high-performance, containerized network utility designed for modern environments. It provides native speedtest capabilities, latency monitoring, and a beautiful live dashboard, all while tracking historical data locally.

Built with **Python 3.11+**, **FastAPI**, **Typer**, and **Polars**.

## ✨ Features

- **Native Speedtests**: Run accurate speedtests directly from your environment.
- **Latency Monitoring**: Track gateway and DNS latency to identify network bottlenecks.
- **Scheduled Tests**: Automatically run network diagnostics at fixed intervals.
- **Modern Dashboard**: A vibrant, responsive web interface with real-time polling.
- **Historical Analysis**: Local SQLite storage with dynamic visualizations using Chart.js.
- **Container First**: Designed to run seamlessly in Docker with Traefik integration.
- **Developer Friendly**: Fully type-hinted, linted, and covered by comprehensive tests.

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- [Poetry](https://python-poetry.org/docs/#installation) (for local development)

### Quick Start (Docker)

The easiest way to run Celeritas is via Docker Compose. It comes pre-configured to work with Traefik for automatic routing.

```bash
docker compose up -d
```

Access the dashboard at [http://celeritas.localhost](http://celeritas.localhost).

### Scheduled Testing

Celeritas includes an optional scheduler service. To enable once-per-hour tests, start the scheduler with:

```bash
docker compose --profile scheduler up -d
```

You can customize the interval in `docker-compose.yml`.

### Local Execution

If you prefer to run it natively:

```bash
# Install dependencies
poetry install

# Run a speedtest CLI command
make run

# Start the dashboard server
make serve
```

## ⚙️ Configuration

Celeritas can be configured using environment variables or a `.env` file.

| Variable                      | Description                       | Default               |
| ----------------------------- | --------------------------------- | --------------------- |
| `CELERITAS_DB_PATH`           | Path to the SQLite database.      | `./data/celeritas.db` |
| `CELERITAS_PORT`              | Port for the dashboard server.    | `80`                  |
| `CELERITAS_SCHEDULE_INTERVAL` | Default test interval in minutes. | `60`                  |

See `.env.example` for a template.

## 🛠️ Development

We maintain high standards for code quality.

### Linting & Formatting

```bash
make lint
```

### Testing

We aim for 100% coverage.

```bash
make test
```

### Documentation

Documentation is built automatically into the container and served directly by the application.

```bash
# Documentation is accessible at:
http://celeritas.localhost/docs/
```

## 📂 Project Structure

```text
celeritas/
├── src/celeritas/      # Main package source
│   ├── api/            # FastAPI endpoints
│   ├── cli/            # Typer logic
│   ├── core/           # Business logic & metrics
│   ├── models/         # Pydantic models
│   └── storage/        # Database & Polars logic
├── docs/               # Markdown documentation
├── tests/              # Pytest suite
├── Dockerfile          # Production image definition
└── docker-compose.yml  # Multi-container orchestration
```

## 🗺️ Roadmap / TODO

- [ ] **Alerts & Notifications**: Support for Slack, Discord, and Email alerts when performance dips below thresholds.
- [ ] **Custom Thresholds**: Define acceptable latency and speed ranges for your specific environment.
- [ ] **Multi-server Comparisons**: Run tests against multiple speedtest servers to identify server-specific issues.
- [ ] **Latency Precision (0/0 issue)**: Further investigations into sub-millisecond precision for specific network configurations to ensure no "0ms" readings occur under any conditions.

## 📄 License

This project is licensed under the MIT License.
