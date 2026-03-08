FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

# Install system build deps and uv.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Install dependencies from lockfile first for layer caching.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy project files and install the project package itself.
COPY . .
RUN uv sync --frozen --no-dev

EXPOSE 8000
VOLUME /app/flow_data

CMD ["uv", "run", "python", "-m", "courierdb.server.app"]
