# syntax=docker/dockerfile:1

FROM python:3.12-slim as builder

ARG APP_NAME
ENV APP_NAME=${APP_NAME}

WORKDIR /${APP_NAME}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.12-slim

ARG APP_NAME
ARG HOST
ENV HOST=${HOST}
ENV APP_NAME=${APP_NAME}

COPY --from=builder /opt/venv /opt/venv

WORKDIR /${APP_NAME}
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app && \
    mkdir -p /static && \
    chown app:app /${APP_NAME} && \
    chown app:app /static

USER app

COPY --chown=app:app ./${APP_NAME}/ /${APP_NAME}/
COPY --chown=app:app docker-entrypoint.sh /docker-entrypoint.sh

CMD ["daphne", "-e", "ssl:8000:privateKey=/etc/ssl/localhost.key:certKey=/etc/ssl/localhost.crt", "core.asgi:application"]

ENTRYPOINT ["/docker-entrypoint.sh"]