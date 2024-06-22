from fastapi import FastAPI

from app.assembly import root_injector

app = root_injector.get(FastAPI)
