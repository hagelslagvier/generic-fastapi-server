from pydantic import BaseModel


class Config(BaseModel):
    host: str
    port: int
    reload: bool
    db_url: str
    alembic_config_path: str
    db_migrations_path: str
