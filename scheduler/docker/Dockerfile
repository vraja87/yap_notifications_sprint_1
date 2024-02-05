ARG DEBIAN_FRONTEND=noninteractive
ARG BUILD_IMAGE=3.11-bookworm
ARG BASE_IMAGE=3.11-slim-bookworm

#######################################
# Stage Dependencies
#######################################
FROM python:${BUILD_IMAGE} AS modules

WORKDIR /wheels

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

COPY ./conf/requirements.txt requirements.txt

RUN --mount=type=cache,target=/root/.cache \
    pip wheel -r requirements.txt --wheel-dir ./

#######################################
# Stage dev runtime
#######################################
FROM python:${BASE_IMAGE} AS develop

ARG APP_DIR

ENV PYTHONPATH="${APP_DIR}:$PYTHONPATH"

WORKDIR /wheels

COPY --from=modules /wheels ./

RUN --mount=type=cache,target=/root/.cache \
    pip install --no-cache-dir --no-index -r requirements.txt -f ./ && \
    rm -rf ./* && \
    rm -rf /root/.cache/pip/*

WORKDIR ${APP_DIR}

COPY ./src ./

CMD ["python", "main.py"]
