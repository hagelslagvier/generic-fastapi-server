import pytest
from fastapi import FastAPI
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.db.orm.crud.common import UserCRUD
from app.db.orm.models import Base
from tests.assembly import test_root_injector


@pytest.fixture
def db():
    engine = test_root_injector.get(Engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def content(db):
    session = test_root_injector.get(Session)

    user_crud = UserCRUD()
    for index in range(5):
        user_crud.create(
            session=session,
            payload={
                "login": f"foo_{index}",
                "password": f"bar_{index}",
            },
        )


@pytest.fixture
def test_client(db, content):
    app = test_root_injector.get(FastAPI)
    client = TestClient(app)

    return client
