# Deploy App with Docker

## Recipes

```Dockerfile
# syntax=docker/dockerfile:1
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app
# Only copy uv.lock and not pyproject.toml
# This ensures hermiticity of the build
# And prevents docker image invalidation in case non-dependency changes
# are made to pyproject.toml
COPY uv.lock /app
# Install dependencies
# virtual env is created in "/app/.venv" directory
RUN uv init --name src && uv sync --no-dev --frozen

FROM python:3.13-slim-bookworm AS runner

COPY src /app/src
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app/.venv/lib/python3.13/site-packages

WORKDIR /app
ENTRYPOINT ["python", "src/main.py"]
```

```bash
docker build -t <DOCKER-IMAGE-NAME> .
```

## References

- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [`uv` (Python Cookbook)](../pkg/uv)
- [`uv` Docker Images](https://docs.astral.sh/uv/guides/integration/docker/#available-images)
- [`uv-docker-example` (GitHub Repository)](https://github.com/astral-sh/uv-docker-example)
