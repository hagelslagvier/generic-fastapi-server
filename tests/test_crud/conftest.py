import pytest
from sqlalchemy import Engine

from app.db.orm.crud.generic import session_factory
from tests.test_crud.generic_crud import GroupCRUD, StudentCRUD


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
