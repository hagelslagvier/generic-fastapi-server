import pytest
from fastapi import FastAPI
from sqlalchemy import Engine
from starlette.testclient import TestClient

from app.db.orm.crud.common import UserCRUD
from app.db.orm.crud.interfaces import SessionFactoryInterface
from app.db.orm.models import Base
from tests.assembly import test_root_injector
from tests.types import SideEffect


@pytest.fixture
def db() -> None:
    engine = test_root_injector.get(Engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def content(db: SideEffect) -> None:
    payload = [
        {"login": f"foo_{index}", "password": f"bar_{index}"} for index in range(5)
    ]
    session_factory = test_root_injector.get(SessionFactoryInterface)  # type: ignore[type-abstract]
    with session_factory.make() as session:
        user_crud = UserCRUD(session=session)
        user_crud.create_many(payload=payload)


@pytest.fixture
def test_client(content: SideEffect) -> TestClient:
    app = test_root_injector.get(FastAPI)
    client = TestClient(app)

    return client
