from fastapi import FastAPI

from app.assembly import root_assembly

app = root_assembly().get(FastAPI)
