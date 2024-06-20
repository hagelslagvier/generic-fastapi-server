from typing import Generator
from sqlalchemy.orm import Session

from app.assembly import db_assembly


def make_session() -> Generator:
    with db_assembly().get(Session) as session:
        yield session
