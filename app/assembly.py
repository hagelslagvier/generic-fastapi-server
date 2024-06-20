from typing import Optional

import pathlib
from dotenv import dotenv_values
from injector import Injector

HERE = pathlib.Path(__file__)
CONFIG = dotenv_values(str(HERE.parent / ".env"))


def db_assembly(injector: Optional[Injector] = None) -> Injector:
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine, Engine

    injector = injector or Injector()

    def make_engine() -> Engine:
        db_url = CONFIG["DB_URI"]

        return create_engine(url=db_url)

    injector.binder.bind(Engine, to=make_engine)

    def make_session() -> Session:
        engine = injector.get(Engine)
        session = Session(bind=engine)

        return session

    injector.binder.bind(Session, to=make_session)

    return injector


def root_assembly(injector: Optional[Injector] = None) -> Injector:
    from fastapi import FastAPI
    from app.endpoints.users.users import router as users_router

    injector = injector or Injector()

    def make_app() -> FastAPI:
        app = FastAPI()
        app.include_router(users_router)

        return app

    injector.binder.bind(FastAPI, to=make_app)

    return injector
