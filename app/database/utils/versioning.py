from alembic import command
from alembic.config import Config as AlembicConfig

from app.settings.config import Config as AppConfig


def migrate(config: AppConfig) -> None:
    alembic_config = AlembicConfig(config.persistence.alembic_config_path)
    alembic_config.set_main_option(
        "script_location", config.persistence.db_migrations_path
    )
    alembic_config.set_main_option("sqlalchemy.url", config.persistence.db_url)

    command.upgrade(alembic_config, "head")
