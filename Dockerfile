ARG USER=me
ARG POETRY_VERSION=1.3.1

FROM python:3.8-slim

ARG USER
ARG POETRY_VERSION

ENV PATH "/home/${USER}/.local/bin:$PATH"

RUN useradd -ms /bin/bash ${USER}

USER ${USER}

RUN pip3 install --upgrade pip && \
    pip3 install poetry==${POETRY_VERSION}

WORKDIR /home/${USER}/tiny

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN POETRY_VIRTUALENVS_PREFER_ACTIVE_PYTHON=false \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    poetry install

#COPY --from=base /home/${USER}/tiny/.venv /home/${USER}/tiny/.venv
#COPY --from=base .venv .venv
COPY app app

ENTRYPOINT ["./app/entrypoint.sh"]
