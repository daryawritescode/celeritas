FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY pyproject.toml poetry.lock* ./
ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ]; then poetry install --no-root; else poetry install --no-root --without dev; fi

COPY src/ ./src/
COPY tests/ ./tests/
COPY README.md ./
RUN if [ "$INSTALL_DEV" = "true" ]; then poetry install; else poetry install --without dev; fi

# We run as root in this simple container so ping3 can craft raw sockets properly
EXPOSE 8000
CMD ["poetry", "run", "python", "-m", "celeritas.cli.app", "serve", "--host", "0.0.0.0"]
