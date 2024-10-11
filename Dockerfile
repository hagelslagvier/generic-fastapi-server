ARG APP_NAME
ARG POETRY_VERSION
ARG PYTHON_IMAGE

FROM ${PYTHON_IMAGE} AS base

ARG APP_NAME
ARG POETRY_VERSION

RUN pip3 install --upgrade pip \
    && pip3 install poetry==${POETRY_VERSION}

WORKDIR /${APP_NAME}

COPY pyproject.toml poetry.lock ./

RUN POETRY_VIRTUALENVS_PREFER_ACTIVE_PYTHON=false \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    poetry install --without dev

FROM ${PYTHON_IMAGE}

ARG APP_NAME

RUN apt update -y \
    && apt install sysstat -y

WORKDIR /${APP_NAME}

COPY --from=base /${APP_NAME}/.venv /${APP_NAME}/.venv
COPY .env.base .env.base
COPY .env.prod .env
COPY app app

CMD [ ".venv/bin/python",  "app/run.py" ]
