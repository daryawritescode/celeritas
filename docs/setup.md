# Getting Started 🚀

Follow these instructions to get Celeritas up and running in your environment.

## 📋 Prerequisites

- **Docker & Docker Compose**: Recommended for most users.
- **Python 3.11+**: Required for local native execution.
- **Poetry**: Required for dependency management during local development.

## 🐳 Docker Setup (Recommended)

The easiest way to run Celeritas is using Docker Compose, especially behind a proxy like Traefik.

1. **Clone the repository**:

    ```bash
    git clone https://github.com/daryawritescode/celeritas.git
    cd celeritas
    ```

2. **Start the services**:

    ```bash
    docker compose up -d
    ```

3. **Access the dashboard**:
    Open [http://celeritas.localhost](http://celeritas.localhost) in your browser.

## 🐍 Local Native Setup

If you prefer to run Celeritas directly on your host:

1. **Install dependencies**:

    ```bash
    poetry install
    ```

2. **Configure environment**:

    ```bash
    cp .env.example .env
    # Edit .env as needed
    ```

3. **Run the application**:

    ```bash
    # Run a single speedtest
    make run

    # Start the web dashboard
    make serve
    ```
