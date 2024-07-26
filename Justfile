set allow-duplicate-variables := true
set dotenv-filename := ".env.base"


ABS_VENV_PATH := absolute_path(clean("${VENV}"))

fix:
    isort app/ tests/
    ruff check app/ tests/ --extend-select I --fix
    ruff format app/ tests/

type-check:
    mypy app/
    mypy tests/

test:
    pytest -s --cov=app/ --cov-report=html:tests/coverage tests/

check:
    just fix
    just type-check
    just test

make-migrations:
    alembic -c app/db/alembic.ini revision --autogenerate

migrate:
    alembic -c app/db/alembic.ini upgrade head

clean:
    find ./app ./tests \
      -regextype posix-extended \
      -regex '.*(/\.ruff_cache|/\.mypy_cache|/.pytest_cache|/__pycache__|\.pyc|\.pyo)$' \
      -exec rm -rf {} +
    yes Y | docker image prune
    docker images -a | grep none | awk '{ print $3; }' | xargs docker rmi --force 2>/dev/null || true

build:
    just clean
    docker build \
      --build-arg=APP_NAME=${APP_NAME} \
      --build-arg=POETRY_VERSION=${POETRY_VERSION} \
      --build-arg=PYTHON_IMAGE=${PYTHON_IMAGE} \
      -t ${APP_NAME} .

rebuild:
    just clean
    docker build \
      --build-arg=APP_NAME=${APP_NAME} \
      --build-arg=POETRY_VERSION=${POETRY_VERSION} \
      --build-arg=PYTHON_IMAGE=${PYTHON_IMAGE} \
      --no-cache \
      -t ${APP_NAME} .

debug:
    docker run --rm -it --entrypoint bash ${APP_NAME}

run:
    docker-compose --env-file .env.dev up db

deploy:
    docker-compose --env-file .env.prod up

health-check:
    docker-compose --env-file .env.prod ps

stop:
    #!/bin/bash
    export CONTAINERS=$(docker ps -aq)
    if [ -n "${CONTAINERS}" ]; then  # ??? why use ""
        docker stop ${CONTAINERS}
        docker rm ${CONTAINERS}
    fi

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
