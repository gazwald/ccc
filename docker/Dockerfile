# Multistage Reflex Dockerfile
# Cobbled together from https://github.com/reflex-dev/reflex/tree/main/docker-example
# +++++++++++++++
# Base Target
# +++++++++++++++
ARG REGISTRY_DOCKER="docker.io"
FROM ${REGISTRY_DOCKER}/library/python:3.13 AS base

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Setup reflex user
RUN adduser --disabled-password \
            --home /app \
            reflex \
 && mkdir -p /app/data \
             /app/uploaded_files;

WORKDIR /app

# Setup UV (copy from astral-sh image)
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
# TODO: Use $REGISTRY_GHCR?
COPY --from=ghcr.io/astral-sh/uv:0.8.13 \
    /uv /uvx \
    /bin/

# Install libpq-dev for psycopg (skip if not using postgres).
# RUN apt-get update -y && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# +++++++++++++++
# Builder Target
# +++++++++++++++
FROM base AS builder

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked \
            --compile-bytecode \
            --no-install-project;

COPY . .

# Build frontend
RUN --mount=type=cache,target=/root/.cache/uv \
    uv run reflex export --frontend-only \
                         --no-zip;

# +++++++++++++++
# Frontend Target
# +++++++++++++++
FROM ${REGISTRY_DOCKER}/library/caddy:2.10 AS app-frontend

ARG APP_FRONTEND_FQDN
ARG APP_BACKEND_FQDN
ARG APP_BACKEND_PORT

COPY <<EOF /etc/caddy/Caddyfile
localhost

encode gzip
tls internal

@backend_routes path /_event/* /ping /_upload /_upload/*
handle @backend_routes {
	reverse_proxy backend:8000
}

root * /srv
route {
	try_files {path} {path}/ /404.html
	file_server
}
EOF

COPY --from=builder \
      /app/.web/build/client \
      /srv

# +++++++++++++++
# Backend Target
# +++++++++++++++
FROM base AS app-backend

ARG APP_BACKEND_PORT

USER reflex

# Needed until Reflex properly passes SIGTERM on backend.
STOPSIGNAL SIGKILL

COPY --from=builder \
     --chown=reflex \
     /app \
     /app

# Always apply migrations before starting the backend.
CMD [ -d alembic ] \
 && uv run reflex db migrate; \
    exec uv run reflex run --env prod \
                           --loglevel debug \
                           --backend-only \
                           --backend-port ${APP_BACKEND_PORT:-8000}
