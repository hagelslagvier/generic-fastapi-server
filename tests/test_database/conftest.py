import pytest
from inzicht import session_factory
from sqlalchemy import Engine

from app.interactors.users.interactors import UserCRUD


@pytest.fixture
def content(engine: Engine) -> None:
    with session_factory(bind=engine) as session:
        payload = {
            "login": "john_doe",
            "password": "secret",
            "email": "john.doe@mail.com",
            "is_email_confirmed": True,
            "refresh_token": "refresh",
            "access_token": "access",
            "is_admin": True,
        }
        UserCRUD(session=session).create(payload=payload)
