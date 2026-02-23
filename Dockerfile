# Build stage for documentation and dependencies
FROM ubuntu:24.04 AS builder

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
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
# Install all dependencies (including docs) to build the site
RUN poetry install --no-root

COPY src/ ./src/
COPY docs/ ./docs/
COPY mkdocs.yml README.md ./
RUN poetry install
RUN poetry run mkdocs build -d site

# Final stage
FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python-is-python3 \
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
COPY README.md LICENSE ./
COPY --from=builder /app/site ./site
RUN if [ "$INSTALL_DEV" = "true" ]; then poetry install; else poetry install --without dev; fi

EXPOSE 80
CMD ["poetry", "run", "celeritas", "serve", "--host", "0.0.0.0"]
