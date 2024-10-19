import os
from pathlib import Path

from dotenv import load_dotenv
from injector import Injector, singleton
from sqlalchemy import Engine, StaticPool, create_engine
from sqlalchemy.orm import Session

from app.assembly import assemble_app, assemble_endpoints
from app.config import Config

ROOT_PATH = Path(__file__).parents[1]
ENV_BASE_PATH = ROOT_PATH / ".env.base"
ENV_DEVELOPMENT_PATH = ROOT_PATH / ".env.development"

for path in [
    ENV_BASE_PATH,
    ENV_DEVELOPMENT_PATH,
]:  # in Dockerfile, ENV_DEVELOPMENT_PATH (.env.development) is not copied to the image
    if path.exists() and path.is_file():
        load_dotenv(path)


def assemble_test_config(injector: Injector | None) -> Injector:
    def make_config() -> Config:
        return Config(
            host=os.environ["HOST"],
            port=os.environ["PORT"],
            db_url=os.environ["TEST_DB_URL"],
            alembic_config_path=os.environ["ALEMBIC_CONFIG_PATH"],
            db_migrations_path=os.environ["MIGRATIONS_PATH"],
            reload=os.getenv("RELOAD", False),
        )

    injector = injector or Injector()
    injector.binder.bind(Config, to=make_config)

    return injector


def assemble_test_db(injector: Injector) -> Injector:
    def make_engine() -> Engine:
        config = injector.get(Config)
        return create_engine(
            url=config.db_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

    injector.binder.bind(Engine, to=make_engine, scope=singleton)

    def make_session() -> Session:
        engine = injector.get(Engine)
        return Session(bind=engine)

    injector.binder.bind(Session, to=make_session)

    return injector


test_root_injector = Injector()
assemble_test_config(test_root_injector)
assemble_test_db(test_root_injector)
assemble_endpoints(test_root_injector)
assemble_app(test_root_injector)
