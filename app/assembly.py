import os
import pathlib
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from injector import Injector
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.config import Config

HERE = pathlib.Path(__file__)
ENV_FILE_PATH = HERE.parent / ".env"

load_dotenv(ENV_FILE_PATH)


def assemble_config(injector: Optional[Injector] = None) -> Injector:
    def make_config() -> Config:
        return Config(db_url=os.environ["DB_URL"])

    injector = injector or Injector()
    injector.binder.bind(Config, to=make_config)

    return injector


def assemble_db(injector: Injector) -> Injector:
    def make_engine() -> Engine:
        config = injector.get(Config)
        return create_engine(url=config.db_url)

    injector.binder.bind(Engine, to=make_engine)

    def make_session() -> Session:
        engine = injector.get(Engine)
        session = Session(bind=engine)

        return session

    injector.binder.bind(Session, to=make_session)

    return injector


def assemble_app(injector: Injector) -> Injector:
    from app.endpoints.users.users import router as users_router
    from app.endpoints.health.health import router as health_router

    users_router.injector = injector  # type: ignore

    def make_app() -> FastAPI:
        app = FastAPI()
        app.include_router(users_router)
        app.include_router(health_router)

        return app

    injector.binder.bind(FastAPI, to=make_app)

    return injector


root_injector = Injector()
assemble_config(root_injector)
assemble_db(root_injector)
assemble_app(root_injector)
