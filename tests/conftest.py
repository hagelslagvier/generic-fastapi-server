from collections.abc import Generator

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.database.orm.factories import session_factory
from app.database.orm.models import Base
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
