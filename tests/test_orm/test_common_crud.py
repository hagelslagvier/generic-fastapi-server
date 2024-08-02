import pytest
from sqlalchemy.orm.session import Session

from app.db.orm.crud.errors import DoesNotExistError
from tests.test_orm.models import UserCRUD
from tests.types import SideEffect


def test_if_can_count_records(session: Session, content: SideEffect) -> None:
    user_crud = UserCRUD(session=session)
    count = user_crud.count()

    assert count == 10


def test_if_can_create_single_record(session: Session) -> None:
    name = "John Doe"
    age = 20

    user_crud = UserCRUD(session=session)

    created = user_crud.create(payload={"name": name, "age": age})
    assert all([created.id, created.created_on, created.updated_on])
    assert created.name == name
    assert created.age == age


def test_if_can_create_multiple_records(session: Session) -> None:
    name = "John Doe"
    age = 20

    payload = [{"name": f"{name}_{index}", "age": age + index} for index in range(0, 5)]

    user_crud = UserCRUD(session=session)

    created = user_crud.create_many(payload=payload)

    for payload_item, instance in zip(payload, created):
        assert all([instance.id, instance.created_on, instance.updated_on])
        assert instance.name == payload_item["name"]
        assert instance.age == payload_item["age"]


def test_if_raises_exception_when_retrieves_nonexistent_record(
    session: Session,
) -> None:
    user_crud = UserCRUD(session=session)

    with pytest.raises(DoesNotExistError) as error:
        user_crud.read(id=42)

    assert (
        str(error.value)
        == "Instance of model='<class 'tests.test_orm.models.User'>' with id='42' was not found"
    )


def test_if_can_read_single_record(session: Session) -> None:
    name = "John Doe"
    age = 20

    user_crud = UserCRUD(session=session)

    created = user_crud.create(payload={"name": name, "age": age})
    assert created.id

    retrieved = user_crud.read(id=created.id)
    assert created.id == retrieved.id
    assert retrieved.name == name
    assert retrieved.age == age


def test_if_can_read_multiple_records(session: Session, content: SideEffect) -> None:
    user_crud = UserCRUD(session=session)

    retrieved = user_crud.read_many()

    assert {item.id for item in retrieved} == set(range(1, 11))


def test_if_can_update_record(session: Session) -> None:
    name = "John Doe"
    age = 20

    user_crud = UserCRUD(session=session)

    created = user_crud.create(payload={"name": name, "age": age})
    assert created.id

    updated = user_crud.update(id=created.id, payload={"name": "Joseph"})
    assert updated.name == "Joseph"
    assert updated.age == 20

    retrieved = user_crud.read(id=created.id)
    assert retrieved.name == "Joseph"
    assert retrieved.age == 20

    updated = user_crud.update(id=created.id, payload={"age": "21"})
    assert updated.name == "Joseph"
    assert updated.age == 21

    retrieved = user_crud.read(id=created.id)
    assert retrieved.name == "Joseph"
    assert retrieved.age == 21

    updated = user_crud.update(id=created.id, payload={"name": "Jack", "age": "22"})
    assert updated.name == "Jack"
    assert updated.age == 22

    retrieved = user_crud.read(id=created.id)
    assert retrieved.name == "Jack"
    assert retrieved.age == 22
