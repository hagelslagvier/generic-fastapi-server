import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from injector import Injector
from sqlalchemy import Engine, StaticPool, create_engine
from sqlalchemy.orm import Session

from app.assembly import assemble_app
from app.config import Config

ROOT_PATH = Path(__file__).parents[1]
ENV_BASE_PATH = ROOT_PATH / ".env.base"
ENV_DEV_PATH = ROOT_PATH / ".env.dev"

for path in [
    ENV_BASE_PATH,
    ENV_DEV_PATH,
]:  # in Dockerfile, ENV_DEV_PATH (.env.dev) is not copied to the image
    if path.exists() and path.is_file():
        load_dotenv(path)


def assemble_test_config(injector: Optional[Injector]) -> Injector:
    def make_config() -> Config:
        return Config(
            host=os.getenv("HOST", ""),
            port=os.getenv("PORT", 0),
            reload=os.getenv("RELOAD", False),
            db_url=os.getenv("TEST_DB_URL", ""),
            alembic_config_path=os.getenv("ALEMBIC_CONFIG_PATH", ""),
            db_migrations_path=os.getenv("MIGRATIONS_PATH", ""),
        )

    injector = injector or Injector()
    injector.binder.bind(Config, to=make_config)

    return injector


def assemble_db(injector: Injector) -> Injector:
    def make_engine() -> Engine:
        config = injector.get(Config)
        return create_engine(
            url=config.db_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

    injector.binder.bind(Engine, to=make_engine)

    def make_session() -> Session:
        engine = injector.get(Engine)
        return Session(bind=engine)

    injector.binder.bind(Session, to=make_session)

    return injector


test_root_injector = Injector()
assemble_test_config(test_root_injector)
assemble_db(test_root_injector)
assemble_app(test_root_injector)
