import pytest
from sqlalchemy import Engine

from app.db.orm.crud.generic import session_factory
from tests.test_crud.generic_crud import CourseCRUD, GroupCRUD, LockerCRUD, StudentCRUD


@pytest.fixture
def content(engine: Engine) -> None:
    with session_factory(bind=engine) as session:
        locker_crud = LockerCRUD(session=session)
        course_crud = CourseCRUD(session=session)
        group_crud = GroupCRUD(session=session)
        student_crud = StudentCRUD(session=session)

        lockers = locker_crud.create_many(
            payload=[{"code": locker_index} for locker_index in range(7)]
        )
        courses = course_crud.create_many(
            payload=[
                {"title": "Course_1"},
                {"title": "Course_2"},
                {"title": "Course_3"},
                {"title": "Course_4"},
                {"title": "Course_5"},
            ]
        )
        groups = group_crud.create_many(
            payload=[
                {"title": "1"},
                {"title": "2"},
            ]
        )
        student_crud.create_many(
            payload=[
                {
                    "name": "S1_G1",
                    "group": groups[0],
                    "locker": lockers[0],
                    "courses": [courses[0], courses[1]],
                },
                {
                    "name": "S2_G1",
                    "group": groups[0],
                    "locker": lockers[1],
                    "courses": [courses[0]],
                },
                {
                    "name": "S3_G1",
                    "group": groups[0],
                    "locker": lockers[2],
                    "courses": [courses[0]],
                },
                {
                    "name": "S4_G1",
                    "group": groups[0],
                    "locker": lockers[3],
                    "courses": [courses[0]],
                },
                {
                    "name": "S5_G1",
                    "group": groups[0],
                    "locker": lockers[4],
                    "courses": [courses[0], courses[2]],
                },
                {
                    "name": "S1_G2",
                    "group": groups[1],
                    "locker": lockers[5],
                    "courses": [courses[0], courses[3]],
                },
                {
                    "name": "S2_G2",
                    "group": groups[1],
                    "locker": lockers[6],
                    "courses": [courses[0], courses[4]],
                },
            ]
        )
