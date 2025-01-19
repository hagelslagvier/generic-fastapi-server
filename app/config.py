from pydantic import BaseModel


class Config(BaseModel):
    host: str
    port: int
    reload: bool
    db_url: str
    alembic_config_path: str
    db_migrations_path: str
    secret_key: str
    algorithm: str
    refresh_token_expiration_minutes: int
    access_token_expiration_minutes: int
    key_length: int
    iterations: int
