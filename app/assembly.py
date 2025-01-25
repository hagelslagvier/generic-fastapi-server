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
from app.database.utils.versioning import migrate
from app.dependencies.auth import get_user_from_token
from app.endpoints.liveness.liveness import router as liveness_router
from app.endpoints.readiness.readiness import router as readiness_router
from app.endpoints.tokens.tokens import router as token_router
from app.endpoints.users.users import router as users_router
from app.interactors.auth.interactors import Auth
from app.interactors.auth.interfaces import (
    AuthInterface,
    SecretManagerInterface,
    TokenManagerInterface,
)
from app.interactors.auth.secret_manager import SecretManager
from app.interactors.auth.token_manager import TokenManager
from app.interactors.liveness.interactors import LivenessProbe
from app.interactors.liveness.interfaces import LivenessProbeInterface
from app.interactors.readiness.interactors import ReadinessProbe
from app.interactors.readiness.interfaces import ReadinessProbeInterface
from tests.fake import get_user_from_token_stub

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
            port=os.environ["PORT"],  # noqa
            db_url=os.environ["DB_URL"],
            alembic_config_path=os.environ["ALEMBIC_CONFIG_PATH"],
            db_migrations_path=os.environ["MIGRATIONS_PATH"],
            reload=os.getenv("RELOAD", False),
            secret_key=os.environ["SECRET_KEY"],
            algorithm=os.environ["ALGORITHM"],
            refresh_token_expiration_minutes=os.environ[  # noqa
                "REFRESH_TOKEN_EXPIRATION_MINUTES"
            ],
            access_token_expiration_minutes=os.environ[  # noqa
                "ACCESS_TOKEN_EXPIRATION_MINUTES"
            ],
            key_length=os.environ["KEY_LENGTH"],  # noqa
            iterations=os.environ["ITERATIONS"],  # noqa
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


def assemble_interactors(injector: Injector) -> Injector:
    config = injector.get(Config)

    injector.binder.bind(
        LivenessProbeInterface, LivenessProbe(CPU_LIMIT=95, RAM_LIMIT=95)
    )

    injector.binder.bind(
        ReadinessProbeInterface, ReadinessProbe(bind=injector.get(Engine))
    )

    def make_secret_manager() -> SecretManagerInterface:
        secret_manager = SecretManager(
            key_length=config.key_length, iterations=config.iterations
        )
        return secret_manager

    injector.binder.bind(SecretManagerInterface, to=make_secret_manager)

    def make_token_manager() -> TokenManagerInterface:
        token_manager = TokenManager(
            secret_key=config.secret_key, algorithm=config.algorithm
        )
        return token_manager

    injector.binder.bind(TokenManagerInterface, to=make_token_manager)

    def make_auth() -> AuthInterface:
        auth = Auth(
            engine=injector.get(Engine),
            secret_manager=injector.get(SecretManagerInterface),
            token_manager=injector.get(TokenManagerInterface),
            token_ttl=config.access_token_expiration_minutes,
        )
        return auth

    injector.binder.bind(AuthInterface, to=make_auth)

    return injector


def override_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[get_user_from_token] = get_user_from_token_stub


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
        app.include_router(router=liveness_router)
        app.include_router(router=readiness_router)
        app.include_router(router=token_router)
        override_dependencies(app=app)
        return app

    injector.binder.bind(FastAPI, to=make_app)

    return injector


root_injector = Injector()
assemble_config(root_injector)
assemble_db(root_injector)
assemble_interactors(root_injector)
assemble_app(root_injector)
