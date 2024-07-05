from typing import Generator

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from tests.assembly import test_root_injector
from tests.test_orm.models import User, UserCRUD
from tests.types import SideEffect


@pytest.fixture
def engine() -> Engine:
    return test_root_injector.get(Engine)


@pytest.fixture
def schema(engine: Engine) -> None:
    User.metadata.drop_all(bind=engine)
    User.metadata.create_all(bind=engine)


@pytest.fixture
def session(engine: Engine, schema: SideEffect) -> Generator[Session, None, None]:
    with Session(bind=engine) as session:
        yield session


@pytest.fixture
def content(session: Session) -> None:
    user_crud = UserCRUD()
    items = [
        {"name": "a", "age": 1},
        {"name": "b", "age": 2},
        {"name": "c", "age": 3},
        {"name": "d", "age": 4},
        {"name": "e", "age": 5},
        {"name": "f", "age": 6},
        {"name": "g", "age": 7},
        {"name": "h", "age": 8},
        {"name": "i", "age": 9},
        {"name": "j", "age": 10},
    ]
    for item in items:
        user_crud.create(session=session, payload=item)
