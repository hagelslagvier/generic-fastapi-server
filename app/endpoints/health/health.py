import json
import subprocess
from json import JSONDecodeError
from typing import Dict

from app.endpoints.custom import Router


def _mpstat() -> Dict:
    command = "mpstat -o JSON"
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        raise RuntimeError(f"Error while doing health check: {process.stderr}")

    try:
        stats = json.loads(process.stdout)
    except JSONDecodeError as error:
        raise RuntimeError("Error while doing health check") from error

    health = {"stats": stats}

    return health


router = Router(
    prefix="/health",
    tags=["health"],
)


@router.get("/")
def update() -> Dict:
    return _mpstat()
