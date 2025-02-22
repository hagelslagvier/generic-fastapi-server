import json
import logging
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from injector import Injector, singleton
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.database.utils.versioning import migrate
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
from app.settings.config import AuthConfig, Config, PersistenceConfig, ServerConfig

logger = logging.getLogger(__name__)


ROOT_PATH = Path(__file__).parents[2]
ENV_DEVELOPMENT_PATH = ROOT_PATH / ".env.develop"
for path in [
    ENV_DEVELOPMENT_PATH,
]:
    if path.exists() and path.is_file():
        logger.info(f"Loading ENV file from path: '{path}'")
        load_dotenv(path)
    else:
        logger.warning(f"Skipping ENV file with path: '{path}'")


def assemble_config(injector: Injector | None = None) -> Injector:
    def make_config() -> Config:
        ALEMBIC_CONFIG_PATH = ROOT_PATH / Path(os.environ["ALEMBIC_CONFIG_PATH"])
        DB_MIGRATIONS_PATH = ROOT_PATH / Path(os.environ["MIGRATIONS_PATH"])

        server_config = ServerConfig(
            host=os.environ["HOST"],
            port=os.environ["PORT"],  # noqa
            reload=os.getenv("RELOAD", False),
        )

        persistence_config = PersistenceConfig(
            db_url=os.environ["DB_URL"],
            db_migrations_path=str(DB_MIGRATIONS_PATH),
            alembic_config_path=str(ALEMBIC_CONFIG_PATH),
        )

        auth_config = AuthConfig(
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

        config = Config(
            server=server_config,
            persistence=persistence_config,
            auth=auth_config,
        )

        logger.info(f"CONFIG: {json.dumps(config.model_dump(), indent=4, default=str)}")

        return config

    injector = injector or Injector()
    injector.binder.bind(Config, to=make_config, scope=singleton)

    return injector


def assemble_db(injector: Injector) -> Injector:
    def make_engine() -> Engine:
        config = injector.get(Config)
        return create_engine(url=config.persistence.db_url)

    injector.binder.bind(Engine, to=make_engine)

    def make_session() -> Session:
        engine = injector.get(Engine)
        return Session(bind=engine)

    injector.binder.bind(Session, to=make_session)

    return injector


def assemble_interactors(injector: Injector) -> Injector:
    config = injector.get(Config)

    injector.binder.bind(
        LivenessProbeInterface, LivenessProbe(cpu_limit=95, ram_limit=95)
    )

    injector.binder.bind(ReadinessProbeInterface, ReadinessProbe())

    def make_secret_manager() -> SecretManagerInterface:
        secret_manager = SecretManager(
            key_length=config.auth.key_length,
            iterations=config.auth.iterations,
        )
        return secret_manager

    injector.binder.bind(SecretManagerInterface, to=make_secret_manager)

    def make_token_manager() -> TokenManagerInterface:
        token_manager = TokenManager(
            secret_key=config.auth.secret_key,
            algorithm=config.auth.algorithm,
        )
        return token_manager

    injector.binder.bind(TokenManagerInterface, to=make_token_manager)

    def make_auth() -> AuthInterface:
        auth = Auth(
            engine=injector.get(Engine),
            secret_manager=injector.get(SecretManagerInterface),
            token_manager=injector.get(TokenManagerInterface),
            token_ttl=config.auth.access_token_expiration_minutes,
        )
        return auth

    injector.binder.bind(AuthInterface, to=make_auth)

    return injector


def assemble_app(injector: Injector) -> Injector:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator:
        migrate(config=injector.get(Config))
        readiness_probe = injector.get(ReadinessProbeInterface)
        readiness_probe.set_ready(True)
        yield
        readiness_probe.set_ready(False)

    def make_app() -> FastAPI:
        app = FastAPI(lifespan=lifespan)
        app.state.injector = injector
        app.include_router(router=liveness_router)
        app.include_router(router=readiness_router)
        app.include_router(router=token_router)
        app.include_router(router=users_router)

        return app

    injector.binder.bind(
        FastAPI,
        to=make_app,
        scope=singleton,  # to override dependencies in tests
    )

    return injector


root_injector = Injector()
assemble_config(root_injector)
assemble_db(root_injector)
assemble_interactors(root_injector)
assemble_app(root_injector)
