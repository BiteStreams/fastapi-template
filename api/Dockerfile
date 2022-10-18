FROM python:3.9-slim as base

ARG PROJECT=api

# Create a non-root user to run the app with.
RUN groupadd --gid 1000 user &&  adduser --disabled-password --gecos '' --uid 1000 --gid 1000 user
USER user

WORKDIR /home/user

# Install Poetry.
RUN --mount=type=cache,target=/root/.cache pip install --user poetry==1.2.0
ENV \
    PATH="/home/user/.local/bin:/home/user/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

COPY --chown=user:user ./pyproject.toml ./
COPY --chown=user:user ./poetry.lock ./


FROM base as dev

WORKDIR /home/user/$PROJECT
RUN --mount=type=cache,target=/root/.cache poetry install
COPY --chown=user:user ./$PROJECT /home/user/$PROJECT

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]


FROM dev as test

RUN --mount=type=cache,target=/root/.cache poetry install --with dev


# Default target.
FROM dev

