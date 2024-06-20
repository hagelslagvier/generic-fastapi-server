#!/bin/bash

PARAMS=(--host "${HOST}" --port "${PORT}")
if [[ $RELOAD == true ]]; then
    PARAMS+=(--reload)
fi

set -e
source ${VENV_PATH}/bin/activate
uvicorn app.main:app "${PARAMS[@]}"