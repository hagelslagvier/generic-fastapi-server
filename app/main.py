from fastapi import FastAPI

from app.assembly import root_injector
from app.db.utils import create_db_schema

app = root_injector.get(FastAPI)


@app.on_event("startup")
async def on_startup() -> None:
    create_db_schema()
