FROM python:3.13 AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=.

FROM base AS user

ARG NAME
ENV NAME=$NAME

WORKDIR /services/user

COPY user/pyproject.toml ./

RUN uv sync --no-install-project

CMD ["uv", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "5000"]

FROM base AS product

ARG NAME
ENV NAME=$NAME

WORKDIR /services/product

COPY product/pyproject.toml ./

RUN uv sync --no-install-project

CMD ["uv", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "5000"]

FROM base AS order

ARG NAME
ENV NAME=$NAME

WORKDIR /services/order

COPY order/pyproject.toml ./

RUN uv sync --no-install-project

CMD ["uv", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "5000"]
