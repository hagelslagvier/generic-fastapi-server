import pytest
from sqlalchemy.orm.session import Session

from app.db.orm.crud.errors import DoesNotExistError
from tests.test_orm.models import UserCRUD
from tests.types import SideEffect


def test_if_can_count_records(session: Session, content: SideEffect) -> None:
    user_crud = UserCRUD()
    count = user_crud.count(session=session)

    assert count == 10


def test_if_can_create_record(session: Session) -> None:
    name = "John Doe"
    age = 20

    user_crud = UserCRUD()

    created = user_crud.create(session=session, payload={"name": name, "age": age})
    assert all([created.id, created.created_on, created.updated_on])
    assert created.name == name
    assert created.age == age


def test_if_raises_exception_when_record_not_exist(session: Session) -> None:
    user_crud = UserCRUD()

    with pytest.raises(DoesNotExistError) as error:
        user_crud.get(session=session, id=42)

    assert (
        str(error.value)
        == "Instance of model='<class 'tests.test_orm.models.User'>' with id='42' was not found"
    )


def test_if_can_get_record(session: Session) -> None:
    name = "John Doe"
    age = 20

    user_crud = UserCRUD()

    created = user_crud.create(session=session, payload={"name": name, "age": age})
    assert created.id

    retrieved = user_crud.get(session=session, id=created.id)
    assert created.id == retrieved.id
    assert retrieved.name == name
    assert retrieved.age == age


def test_if_can_read_records(session: Session, content: SideEffect) -> None:
    user_crud = UserCRUD()

    retrieved = user_crud.read(session=session)

    assert {item.id for item in retrieved} == set(range(1, 11))


def test_if_can_update_record(session: Session) -> None:
    name = "John Doe"
    age = 20

    user_crud = UserCRUD()

    created = user_crud.create(session=session, payload={"name": name, "age": age})
    assert created.id

    updated = user_crud.update(
        session=session, id=created.id, payload={"name": "Joseph"}
    )
    assert updated.name == "Joseph"
    assert updated.age == 20

    retrieved = user_crud.get(session=session, id=created.id)
    assert retrieved.name == "Joseph"
    assert retrieved.age == 20

    updated = user_crud.update(session=session, id=created.id, payload={"age": "21"})
    assert updated.name == "Joseph"
    assert updated.age == 21

    retrieved = user_crud.get(session=session, id=created.id)
    assert retrieved.name == "Joseph"
    assert retrieved.age == 21

    updated = user_crud.update(
        session=session, id=created.id, payload={"name": "Jack", "age": "22"}
    )
    assert updated.name == "Jack"
    assert updated.age == 22

    retrieved = user_crud.get(session=session, id=created.id)
    assert retrieved.name == "Jack"
    assert retrieved.age == 22
