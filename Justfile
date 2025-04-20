set dotenv-filename := ".env.base"

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
    #!/bin/bash
    source utils.sh
    load_env .env.develop
    alembic -c ${ALEMBIC_CONFIG_PATH} revision --autogenerate


migrate:
    #!/bin/bash
    source utils.sh
    load_env .env.develop
    alembic -c ${ALEMBIC_CONFIG_PATH} upgrade head


alembic *args:
    #!/bin/bash
    source utils.sh
    load_env .env.develop
    alembic -c ${ALEMBIC_CONFIG_PATH} {{args}}
    exit 0

clean:
    find app tests -type d -name ".*_cache" -exec rm -rf {} +
    find app tests -type d -name "__pycache__" -exec rm -rf {} +
    find app tests -type f \( -name "*.pyc" -o -name "*.pyo" \) -exec rm -f {} +
    find . -type f -name ".DS_Store" -exec rm {} \;


build:
    #!/bin/bash
    docker build \
      --file Dockerfile \
      --build-arg APP_NAME=${APP_NAME} \
      --build-arg POETRY_VERSION=${POETRY_VERSION} \
      --build-arg PYTHON_IMAGE=${PYTHON_IMAGE} \
      -t ${APP_NAME}:latest .


rebuild:
    #!/bin/bash
    source utils.sh
    load_env .env.develop
    docker build \
      --build-arg APP_NAME=${APP_NAME} \
      --build-arg POETRY_VERSION=${POETRY_VERSION} \
      --build-arg PYTHON_IMAGE=${PYTHON_IMAGE} \
      --no-cache \
      -t ${APP_NAME}:latest .


publish tag:
    docker tag ${APP_NAME}:latest ${DOCKER_HUB_USER}/${APP_NAME}:{{tag}}
    docker push ${DOCKER_HUB_USER}/${APP_NAME}:{{tag}}


debug:
    docker run -it --rm --entrypoint bash ${APP_NAME}


start:
    docker-compose --file docker-compose.develop.yml up db


stop:
    #!/bin/bash
    export CONTAINERS=$(docker ps -aq)
    if [ -n "${CONTAINERS}" ]; then
        docker stop ${CONTAINERS}
        docker rm ${CONTAINERS}
    fi


up:
    docker compose -f docker-compose.production.yml up


make-erd:
    python app/database/utils/introspection.py