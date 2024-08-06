from typing import Generator

import pytest
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.db.orm.crud.generic import session_factory
from tests.assembly import test_root_injector
from tests.test_crud.generic_crud import GroupCRUD, StudentCRUD
from tests.test_crud.generic_models import Base


@pytest.yield_fixture
def engine() -> Generator[Engine, None, None]:
    engine = test_root_injector.get(Engine)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.yield_fixture
def session() -> Generator[Session, None, None]:
    session = test_root_injector.get(Session)
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def content(engine: Engine) -> None:
    with session_factory(bind=engine) as session:
        group_crud = GroupCRUD(session=session)
        student_crud = StudentCRUD(session=session)

        group_1, group_2 = group_crud.create_many(
            payload=[
                {"code": "1"},
                {"code": "2"},
            ]
        )
        student_crud.create_many(
            payload=[
                {"name": "S1_G1", "group_id": group_1.id},
                {"name": "S2_G1", "group_id": group_1.id},
                {"name": "S3_G1", "group_id": group_1.id},
                {"name": "S4_G1", "group_id": group_1.id},
                {"name": "S5_G1", "group_id": group_1.id},
            ]
        )
        student_crud.create_many(
            payload=[
                {"name": "S1_G2", "group_id": group_2.id},
                {"name": "S2_G2", "group_id": group_2.id},
            ]
        )
