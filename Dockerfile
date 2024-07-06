ARG APP_NAME
ARG POETRY_VERSION
ARG PYTHON_IMAGE

FROM ${PYTHON_IMAGE} as base

ARG APP_NAME
ARG POETRY_VERSION

RUN pip3 install --upgrade pip \
    && pip3 install poetry==${POETRY_VERSION}

WORKDIR /${APP_NAME}
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN POETRY_VIRTUALENVS_PREFER_ACTIVE_PYTHON=false \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    poetry install --without dev

FROM ${PYTHON_IMAGE}

ARG APP_NAME

RUN apt-get update -y

WORKDIR /${APP_NAME}

COPY --from=base /${APP_NAME}/.venv /${APP_NAME}/.venv
COPY app app

ENV ABS_VENV_PATH=/${APP_NAME}/.venv

ENTRYPOINT ["app/entrypoint.sh"]
