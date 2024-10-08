# syntax=docker/dockerfile:1

FROM python:3.12-slim as builder

ARG POETRY_VERSION=1.8

ENV POETRY_HOME /opt/poetry
ENV POETRY_NO_INTERACTION 1
ENV POETRY_VIRTUALENVS_IN_PROJECT 1
ENV POETRY_VIRTUALENVS_CREATE 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_CACHE_DIR /opt/.cache
ARG APP_NAME
ENV APP_NAME ${APP_NAME}

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install "poetry==${POETRY_VERSION}"

WORKDIR /${APP_NAME}

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-root && rm -rf ${POETRY_CACHE_DIR}

FROM python:3.12-slim

ARG APP_NAME
ARG HOST
ENV HOST ${HOST}
ENV APP_NAME ${APP_NAME}
ENV VIRTUAL_ENV /${APP_NAME}/.venv
ENV PATH="/${APP_NAME}/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /${APP_NAME}

RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app && \
    mkdir -p /static && \
    chown app:app /${APP_NAME} && \
    chown app:app /static

USER app

COPY --chown=app:app ./${APP_NAME}/ /${APP_NAME}/
COPY --chown=app:app docker-entrypoint.sh /docker-entrypoint.sh

EXPOSE 8000

CMD exec daphne -e ssl:8000:privateKey=/etc/ssl/$HOST.key:certKey=/etc/ssl/$HOST.crt core.asgi:application

ENTRYPOINT ["/docker-entrypoint.sh"]