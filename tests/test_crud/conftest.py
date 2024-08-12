import pytest
from sqlalchemy import Engine

from app.db.orm.crud.generic import session_factory
from tests.test_crud.generic_crud import GroupCRUD, LockerCRUD, StudentCRUD


@pytest.fixture
def content(engine: Engine) -> None:
    with session_factory(bind=engine) as session:
        group_crud = GroupCRUD(session=session)
        student_crud = StudentCRUD(session=session)
        locker_crud = LockerCRUD(session=session)

        lockers = locker_crud.create_many(
            payload=[{"code": locker_index} for locker_index in range(7)]
        )
        groups = group_crud.create_many(
            payload=[
                {"title": "1"},
                {"title": "2"},
            ]
        )
        student_crud.create_many(
            payload=[
                {"name": "S1_G1", "group_id": groups[0].id, "locker_id": lockers[0].id},
                {"name": "S2_G1", "group_id": groups[0].id, "locker_id": lockers[1].id},
                {"name": "S3_G1", "group_id": groups[0].id, "locker_id": lockers[2].id},
                {"name": "S4_G1", "group_id": groups[0].id, "locker_id": lockers[3].id},
                {"name": "S5_G1", "group_id": groups[0].id, "locker_id": lockers[4].id},
            ]
        )
        student_crud.create_many(
            payload=[
                {"name": "S1_G2", "group_id": groups[1].id, "locker_id": lockers[5].id},
                {"name": "S2_G2", "group_id": groups[1].id, "locker_id": lockers[6].id},
            ]
        )
