from datetime import datetime
from typing import Dict

import psutil

from app.endpoints.custom import Router


def _get_status() -> Dict[str, str]:
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        return {
            "status": "healthy",
            "uptime": str(uptime),
            "cpu": str(cpu_usage),
            "ram": str(memory_usage),
        }

    except Exception as error:
        return {
            "status": "unhealthy",
            "error_type": error.__class__.__name__,
            "error": str(error),
        }


router = Router(
    prefix="/health",
    tags=["health"],
)


@router.get("/")
def update() -> Dict[str, str]:
    return _get_status()
