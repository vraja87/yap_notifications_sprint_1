ARG BUILD_IMAGE=3.11-buster
ARG BASE_IMAGE=3.11-slim-buster

# modules
FROM python:${BUILD_IMAGE} as modules
WORKDIR /wheels
COPY ./conf/requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache --mount=type=cache,target=/pkg pip install -U pip && pip wheel -r requirements.txt -w /pkg

### builder
FROM python:${BASE_IMAGE} as builder
RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    gettext curl \
    # used in entrypoint to wait for redis
    redis-tools \
  && apt-get purge -y --auto-remove \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY --from=modules /wheels /wheels
RUN --mount=type=cache,target=/pkg pip install -U pip \
       && pip install --no-index -r /wheels/requirements.txt -f /pkg \
       && rm -rf /wheels \
       && rm -rf /root/.cache/pip/*

### dev build base app image
FROM builder as base

ARG APP_DIR
WORKDIR ${APP_DIR}

RUN groupadd -r web && useradd -r -g web web \
  && chown web:web -R /opt/app
COPY --chown=web:web ./src ./

USER web
EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]