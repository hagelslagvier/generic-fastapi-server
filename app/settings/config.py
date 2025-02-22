from pydantic import BaseModel


class ServerConfig(BaseModel):
    host: str
    port: int
    reload: bool = False


class PersistenceConfig(BaseModel):
    db_url: str
    db_migrations_path: str
    alembic_config_path: str


class AuthConfig(BaseModel):
    secret_key: str
    algorithm: str
    refresh_token_expiration_minutes: int
    access_token_expiration_minutes: int
    key_length: int
    iterations: int


class Config(BaseModel):
    server: ServerConfig
    persistence: PersistenceConfig
    auth: AuthConfig
