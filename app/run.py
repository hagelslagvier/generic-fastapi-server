import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

ROOT = Path(__file__).parents[1]
sys.path.append(str(ROOT))

from app.assembly.assembly import root_injector  # noqa
from app.settings.config import Config  # noqa

config = root_injector.get(Config)
app = root_injector.get(FastAPI)


if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host=config.server.host,
        port=config.server.port,
        reload=config.server.reload,
    )
