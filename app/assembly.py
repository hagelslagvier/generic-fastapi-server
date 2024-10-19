import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from injector import Injector
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.config import Config
from app.database.utils.versions import migrate
from app.endpoints.health.health import router as health_router
from app.endpoints.users.users import router as users_router
from app.interactors.health_check.interactors import HealthCheckProbe
from app.interactors.health_check.interfaces import HealthCheckProbeInterface

ROOT_PATH = Path(__file__).parents[1]
ENV_BASE_PATH = ROOT_PATH / ".env.base"
ENV_PRODUCTION = ROOT_PATH / ".env"
ENV_DEVELOPMENT_PATH = ROOT_PATH / ".env.development"

for path in [
    ENV_BASE_PATH,  # dev + prod
    ENV_DEVELOPMENT_PATH,  # dev only
    ENV_PRODUCTION,  # prod only (see Dockerfile: COPY .env.production .env)
]:
    if path.exists() and path.is_file():
        load_dotenv(path)


def assemble_config(injector: Injector | None = None) -> Injector:
    def make_config() -> Config:
        return Config(
            host=os.environ["HOST"],
            port=os.environ["PORT"],
            db_url=os.environ["DB_URL"],
            alembic_config_path=os.environ["ALEMBIC_CONFIG_PATH"],
            db_migrations_path=os.environ["MIGRATIONS_PATH"],
            reload=os.getenv("RELOAD", False),
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
    injector.binder.bind(HealthCheckProbeInterface, HealthCheckProbe())

    return injector


def assemble_app(injector: Injector) -> Injector:
    config = injector.get(Config)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator:
        migrate(config=config)
        yield

    def make_app() -> FastAPI:
        app = FastAPI()
        app.state.injector = injector
        app.include_router(router=users_router)
        app.include_router(router=health_router)

        return app

    injector.binder.bind(FastAPI, to=make_app)

    return injector


root_injector = Injector()
assemble_config(root_injector)
assemble_db(root_injector)
assemble_endpoints(root_injector)
assemble_app(root_injector)
