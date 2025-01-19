from collections.abc import Generator

import pytest
from inzicht import session_factory
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.database.orm.models import Base
from app.interactors.auth.secret_manager import SecretManager
from app.interactors.auth.token_manager import (
    TokenManager,
)
from tests.assembly import test_root_injector


@pytest.fixture
def engine() -> Generator[Engine, None, None]:
    engine = test_root_injector.get(Engine)
    metadata = Base.metadata
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)
    yield engine


@pytest.fixture
def session(engine: Engine) -> Generator[Session, None, None]:
    with session_factory(bind=engine) as session:
        yield session


@pytest.fixture
def secret_manager() -> SecretManager:
    return SecretManager(key_length=32, iterations=100_000)


@pytest.fixture
def token_manager() -> TokenManager:
    return TokenManager(
        secret_key="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
        algorithm="HS256",
    )
