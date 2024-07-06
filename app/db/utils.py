import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from dotenv import load_dotenv

load_dotenv()


ROOT_PATH = Path(__file__).parents[2]
ALEMBIC_CONFIG_PATH = ROOT_PATH / "alembic.ini"
MIGRATIONS_PATH = ROOT_PATH / "app/db/migrations"


def migrate() -> None:
    config = Config(str(ALEMBIC_CONFIG_PATH))
    config.set_main_option("sqlalchemy.url", os.getenv("DB_URL"))
    config.set_main_option("script_location", str(MIGRATIONS_PATH))
    command.upgrade(config, "head")
