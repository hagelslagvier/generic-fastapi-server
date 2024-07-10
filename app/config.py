from dataclasses import dataclass


@dataclass
class Config:
    db_url: str
    alembic_config_path: str
    db_migrations_path: str
