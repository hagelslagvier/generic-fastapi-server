import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator, Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from injector import Injector
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.config import Config
from app.db.utils import migrate
from app.endpoints.custom import App
from app.endpoints.health.health import router as health_router
from app.endpoints.health.interactors import HealthCheckProbe
from app.endpoints.health.interfaces import HealthCheckProbeInterface
from app.endpoints.users.users import router as users_router

ROOT_PATH = Path(__file__).parents[1]
ENV_BASE_PATH = ROOT_PATH / ".env.base"
ENV_DEV_PATH = ROOT_PATH / ".env.dev"

for path in [
    ENV_BASE_PATH,
    ENV_DEV_PATH,
]:  # in Dockerfile, ENV_DEV_PATH (.env.dev) is not copied to the image
    if path.exists() and path.is_file():
        load_dotenv(path)


def assemble_config(injector: Optional[Injector] = None) -> Injector:
    def make_config() -> Config:
        return Config(
            host=os.getenv("HOST", ""),
            port=os.getenv("PORT", 0),
            reload=os.getenv("RELOAD", False),
            db_url=os.getenv("DB_URL", ""),
            alembic_config_path=os.getenv("ALEMBIC_CONFIG_PATH", ""),
            db_migrations_path=os.getenv("MIGRATIONS_PATH", ""),
        )

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
        return Session(bind=engine)

    injector.binder.bind(Session, to=make_session)

    return injector


def assemble_endpoints(injector: Injector) -> Injector:
    injector.binder.bind(HealthCheckProbeInterface, HealthCheckProbe())  # type: ignore[type-abstract]

    return injector


def assemble_app(injector: Injector) -> Injector:
    config = injector.get(Config)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator:
        migrate(config=config)
        yield

    def make_app() -> App:
        app = App(injector=injector)
        app.include_router(users_router)
        app.include_router(health_router)

        return app

    injector.binder.bind(FastAPI, to=make_app)

    return injector


root_injector = Injector()
assemble_config(root_injector)
assemble_db(root_injector)
assemble_endpoints(root_injector)
assemble_app(root_injector)
