import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

ROOT = Path(__file__).parents[1]

sys.path.append(str(ROOT))


from app.assembly import root_injector  # noqa: E402

app = root_injector.get(FastAPI)


if __name__ == "__main__":
    from app.config import Config

    config = root_injector.get(Config)
    uvicorn.run("run:app", host=config.host, port=config.port, reload=config.reload)
