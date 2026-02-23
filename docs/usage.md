# Usage Guide 🏎️

Celeritas provides two main ways to interact with it: the Command Line Interface (CLI) and the Web Dashboard.

## 💻 CLI Usage

The CLI is built with `Typer` and provides a fast way to run network checks.

### Run Speedtest

Executes a full speedtest and network latency check.

```bash
make run
# or
poetry run celeritas run
```

### Start Dashboard

Starts the FastAPI server for the web interface.

```bash
make serve
# or
poetry run celeritas serve
```

## 📊 Web Dashboard

The dashboard provides a real-time view of your network metrics and historical trends.

- **Real-time Polling**: Metrics are updated automatically.
- **Historical Charts**: Dynamic visualizations of your speedtest history using Chart.js.
- **Traefik Integration**: Automatically routed when running in the provided Docker infrastructure.
