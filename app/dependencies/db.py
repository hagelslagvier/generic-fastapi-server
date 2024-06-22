from typing import Generator

from sqlalchemy.orm import Session

from app.assembly import root_injector


def make_session() -> Generator:
    with root_injector.get(Session) as session:
        yield session
