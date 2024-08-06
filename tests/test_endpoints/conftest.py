import pytest
from fastapi import FastAPI
from sqlalchemy import Engine
from starlette.testclient import TestClient

from app.db.orm.crud.common import UserCRUD
from app.db.orm.crud.generic import session_factory
from tests.assembly import test_root_injector
from tests.types import SideEffect


@pytest.fixture
def content(engine: Engine) -> None:
    with session_factory(bind=engine) as session:
        user_crud = UserCRUD(session=session)
        user_crud.create_many(
            payload=[
                {
                    "login": f"user-{index}",
                    "password": f"password-{index}",
                    "email": f"user-{index}@abc.com",
                }
                for index in range(5)
            ]
        )


@pytest.fixture
def test_client(content: SideEffect, engine: Engine) -> TestClient:
    app = test_root_injector.get(FastAPI)
    client = TestClient(app)
    return client
