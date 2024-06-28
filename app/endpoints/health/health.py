import json
import subprocess
from typing import Dict

from fastapi import APIRouter


def _mpstat():
    command = "mpstat -o JSON"
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        raise RuntimeError(process.stderr)

    return json.loads(process.stdout)


router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/")
def update() -> Dict:
    return _mpstat()
