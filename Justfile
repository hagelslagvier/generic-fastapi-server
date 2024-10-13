set dotenv-filename := ".env.base"


ABS_VENV_PATH := absolute_path(clean("${VENV}"))

fix:
    find app/ tests/ -name "*.py" -type f | xargs -I {} pyupgrade --py312-plus {}
    ruff check app/ tests/ --fix
    ruff format app/ tests/


type-check:
    mypy app/
    mypy tests/

test:
    pytest -s --cov=app/ --cov-report=html:tests/coverage tests/

show-coverage:
    #!/usr/bin/env python3
    import pathlib
    import webbrowser

    report_path = f"file://{pathlib.Path.cwd()/'tests/coverage/index.html'}"
    webbrowser.open(report_path)

check:
    just fix
    just type-check
    just test

make-migrations:
    alembic -c ${ALEMBIC_CONFIG_PATH} revision --autogenerate

migrate:
    alembic -c ${ALEMBIC_CONFIG_PATH} upgrade head

clean:
    find app tests -type d -name ".*_cache" -exec rm -rf {} +
    find app tests -type d -name "__pycache__" -exec rm -rf {} +
    find app tests -type f \( -name "*.pyc" -o -name "*.pyo" \) -exec rm -f {} +

build:
    just clean
    docker build \
      --build-arg APP_NAME=${APP_NAME} \
      --build-arg POETRY_VERSION=${POETRY_VERSION} \
      --build-arg PYTHON_IMAGE=${PYTHON_IMAGE} \
      -t ${APP_NAME} .

rebuild:
    just clean
    docker build \
      --build-arg APP_NAME=${APP_NAME} \
      --build-arg POETRY_VERSION=${POETRY_VERSION} \
      --build-arg PYTHON_IMAGE=${PYTHON_IMAGE} \
      --no-cache \
      -t ${APP_NAME} .

debug:
    docker run --rm -it --entrypoint bash ${APP_NAME}

start:
    docker compose --env-file .env.dev up db

stop:
    #!/bin/bash
    export CONTAINERS=$(docker ps -aq)
    if [ -n "${CONTAINERS}" ]; then  # ??? why use ""
        docker stop ${CONTAINERS}
        docker rm ${CONTAINERS}
    fi

up:
    docker compose --env-file .env.prod up

check-health:
    docker compose --env-file .env.prod ps

install:
    #!/bin/bash
    if [ ! -d {{ABS_VENV_PATH}} ]; then
        ${PYTHON} -m venv {{ABS_VENV_PATH}}
    fi

    source {{ABS_VENV_PATH}}/bin/activate
    pip3 install --upgrade pip
    poetry env info
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_PATH={{ABS_VENV_PATH}} \
    POETRY_VIRTUALENVS_PREFER_ACTIVE_PYTHON=true \
    poetry install

    echo -e "\e[32m!! venv created in folder '{{ABS_VENV_PATH}}'\e[0m"

publish tag:
    docker tag ${APP_NAME}:latest ${DOCKER_HUB_USER}/${APP_NAME}:{{tag}}
    docker push ${DOCKER_HUB_USER}/${APP_NAME}:{{tag}}

#  TODO: add make-erm