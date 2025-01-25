import pytest
from inzicht import session_factory
from sqlalchemy import Engine

from app.interactors.readiness.interactors import ReadinessStatusCRUD


@pytest.fixture
def content(engine: Engine) -> None:
    with session_factory(bind=engine) as session:
        payload = {"hostname": "foo", "ready": False}
        ReadinessStatusCRUD(session=session).create(payload=payload)
