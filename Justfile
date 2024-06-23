APP_NAME := "tiny"  # name of the app and docker image
PYTHON := "/home/alexey_naumov/.pyenv/versions/3.10.13/bin/python3.10"  # absolute path to python interpreter
VENV := ".venv"  # virtual environment folder name in project root, when change see also project.toml
RELOAD := "true"  # reload web server
HOST := "0.0.0.0"
PORT := "8000"

VENV_PATH := absolute_path(clean(VENV))

fix:
    ruff check app/ tests/ --fix
    ruff format app/ tests/

type-check:
    mypy app/
#    mypy tests/

test:
    pytest -s --cov=app/ --cov-report=html:tests/coverage tests/

check:
    just fix
    just type-check
    just test

clean:
    rm -f .coverage
    rm -rf .ruff_cache
    rm -rf .mypy_cache
    rm -rf .pytest_cache
    find ./app ./tests -regex '^.*\(__pycache__\|\.py[co]\)$' -delete
    yes Y | docker image prune
    docker images -a | grep none | awk '{ print $3; }' | xargs docker rmi --force 2>/dev/null || true

build:
    docker build --build-arg="APP_NAME={{APP_NAME}}" -t {{APP_NAME}} .

rebuild:
    docker build --build-arg="APP_NAME={{APP_NAME}}" --no-cache -t {{APP_NAME}} .

debug:
    docker run --rm -it --entrypoint bash {{APP_NAME}}

run:
    VENV_PATH={{VENV_PATH}} \
    HOST={{HOST}} \
    PORT={{PORT}} \
    RELOAD={{RELOAD}} \
    ./app/entrypoint.sh

deploy:
    just clean
    just build
    APP_NAME={{APP_NAME}} \
    VENV_PATH="/{{APP_NAME}}/{{VENV}}" \
    HOST={{HOST}} \
    PORT={{PORT}} \
    docker-compose up

stop:
    #!/bin/bash
    export CONTAINERS=$(docker ps -aq)
    if [ -n "${CONTAINERS}" ]; then  # ??? why use ""
        docker stop ${CONTAINERS}
        docker rm ${CONTAINERS}
    fi

install:
    #!/bin/bash
    if [ ! -d {{VENV_PATH}} ]; then
        {{PYTHON}} -m venv {{VENV_PATH}}
    fi

    source {{VENV_PATH}}/bin/activate
    pip3 install --upgrade pip
    poetry env info
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_PATH={{VENV_PATH}} \
    POETRY_VIRTUALENVS_PREFER_ACTIVE_PYTHON=true \
    poetry install

    echo -e "\e[32m!! venv created in folder '{{VENV_PATH}}'\e[0m"
