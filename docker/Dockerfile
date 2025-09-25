# +++++++++++++++
#     Builder
# +++++++++++++++
FROM registry.poppet.io/ghcr/astral-sh/uv:0.8-python3.13-trixie-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked \
            --no-install-project \
            --no-dev;

COPY . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked \
            --no-dev;


# ++++++++++++++
#   App Target
# ++++++++++++++
FROM registry.poppet.io/dockerhub/library/python:3.13-slim-trixie AS app

ENV USER_ID=1000
ENV GROUP_ID=1000

RUN groupadd --system \
             --gid "$GROUP_ID" ccc \
 && useradd --system \
            --gid "$GROUP_ID" \
            --uid "$USER_ID" \
            --create-home ccc;

COPY --from=builder \
     --chown=ccc:ccc \
     /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER ccc

WORKDIR /app

CMD ["python3", "app.py"]
