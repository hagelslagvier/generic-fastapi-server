import pytest
from unittest.mock import patch

from fastapi import FastAPI
from sqlalchemy import Engine
from starlette.testclient import TestClient

from app.assembly import root_assembly, db_assembly
from app.db.orm.models import Base


@pytest.fixture
def config():
    with patch("app.assembly.dotenv_values") as mock:
        config = {"DB_URI": "sqlite:///"}
        mock.return_value = config

        yield config


@pytest.fixture
def db(config):
    engine = db_assembly().get(Engine)
    Base.metadata.create_all(engine)


@pytest.fixture
def test_client(db):
    app = root_assembly().get(FastAPI)
    client = TestClient(app)

    return client
