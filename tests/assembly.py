import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from injector import Injector, singleton
from sqlalchemy import Engine, StaticPool, create_engine
from sqlalchemy.orm import Session

from app.assembly.assembly import assemble_app, assemble_interactors
from app.dependencies.auth import get_user_from_token
from app.settings.config import AuthConfig, Config, PersistenceConfig, ServerConfig
from tests.fake import get_user_from_token_stub

ROOT_PATH = Path(__file__).parents[1]
ENV_BASE_PATH = ROOT_PATH / ".env.base"
ENV_DEVELOPMENT_PATH = ROOT_PATH / ".env.development"

for path in [
    ENV_BASE_PATH,
    ENV_DEVELOPMENT_PATH,
]:
    if path.exists() and path.is_file():
        load_dotenv(path)


def override_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[get_user_from_token] = get_user_from_token_stub


def assemble_test_config(injector: Injector | None) -> Injector:
    def make_config() -> Config:
        server_config = ServerConfig(
            host=os.environ["HOST"],
            port=os.environ["PORT"],  # noqa
            reload=os.getenv("RELOAD", False),
        )

        persistence_config = PersistenceConfig(
            db_url=os.environ["TEST_DB_URL"],
            db_migrations_path=os.environ["ALEMBIC_CONFIG_PATH"],
            alembic_config_path=os.environ["MIGRATIONS_PATH"],
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

        return Config(
            server=server_config,
            persistence=persistence_config,
            auth=auth_config,
        )

    injector = injector or Injector()
    injector.binder.bind(Config, to=make_config)

    return injector


def assemble_test_db(injector: Injector) -> Injector:
    def make_engine() -> Engine:
        config = injector.get(Config)
        return create_engine(
            url=config.persistence.db_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

    injector.binder.bind(Engine, to=make_engine, scope=singleton)

    def make_session() -> Session:
        engine = injector.get(Engine)
        return Session(bind=engine)

    injector.binder.bind(Session, to=make_session)

    return injector


def assemble_test_app(injector: Injector) -> Injector:
    assemble_app(injector=injector)
    override_dependencies(app=injector.get(FastAPI))

    return injector


test_root_injector = Injector()
assemble_test_config(test_root_injector)
assemble_test_db(test_root_injector)
assemble_interactors(test_root_injector)
assemble_test_app(test_root_injector)
