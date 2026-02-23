# Configuration ⚙️

Celeritas is designed to be highly configurable via environment variables.

## 🌐 Environment Variables

| Variable            | Description                                                | Default               |
| ------------------- | ---------------------------------------------------------- | --------------------- |
| `CELERITAS_DB_PATH` | The absolute or relative path to the SQLite database file. | `./data/celeritas.db` |
| `CELERITAS_PORT`    | The port the dashboard server will listen on.              | `80`                  |

## 📝 .env File

For local development, you can use a `.env` file in the project root. Celeritas uses `pydantic-settings` to automatically load these variables.

Example `.env`:

```env
CELERITAS_DB_PATH=./data/celeritas.db
CELERITAS_PORT=80
```

## 🐳 Docker Environment

When using Docker Compose, environment variables are passed through the `environment` section in `docker-compose.yml`.
