from fastapi import FastAPI

from app.assembly import root_injector
from app.db.utils import migrate

app = root_injector.get(FastAPI)


@app.on_event("startup")
async def on_startup() -> None:
    migrate()
