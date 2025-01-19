from inzicht import session_factory
from sqlalchemy import Engine

from app.database.utils.maintenance import (
    create_user,
    read_user,
    update_user,
    update_user_tokens,
)
from app.interactors.users.interactors import UserCRUD
from tests.aliases import SideEffect


def test_if_can_create_user(engine: Engine) -> None:
    with session_factory(bind=engine) as session:
        found = UserCRUD(session=session).read_many()
        users = list(found)

        assert len(users) == 0

    created_user = create_user(
        login="John Doe", password="secret", email="jon_doe@acme.com", engine=engine
    )

    with session_factory(bind=engine) as session:
        found = UserCRUD(session=session).read_many()
        users = list(found)

        assert len(users) == 1

        [retrieved_user] = users

    assert retrieved_user.id == created_user.id


def test_if_can_read(engine: Engine, content: SideEffect) -> None:
    user = read_user(login="john_doe", engine=engine)

    assert user
    assert user.id == 1


def test_if_can_update_user(engine: Engine, content: SideEffect) -> None:
    user = read_user(login="john_doe", engine=engine)

    assert user
    assert user.id == 1
    assert user.login == "john_doe"
    assert user.password == "secret"
    assert user.email == "john.doe@mail.com"
    assert user.is_email_confirmed is True
    assert user.refresh_token == "refresh"
    assert user.access_token == "access"
    assert user.is_admin is True

    updated_user = update_user(
        login="john_doe",
        password="new-secret",
        email="new@mail.com",
        refresh_token="new-refresh",
        access_token="new-access",
        is_admin=False,
        engine=engine,
    )

    assert updated_user
    assert updated_user.id == 1
    assert updated_user.login == "john_doe"
    assert updated_user.password == "new-secret"
    assert updated_user.email == "new@mail.com"
    assert updated_user.is_email_confirmed is True
    assert updated_user.refresh_token == "new-refresh"
    assert updated_user.access_token == "new-access"
    assert updated_user.is_admin is False


def test_if_can_delete_user(engine: Engine, content: SideEffect) -> None:
    user = read_user(login="john_doe", engine=engine)

    assert user
    assert user.id == 1


def test_if_can_update_user_tokens(engine: Engine, content: SideEffect) -> None:
    user = read_user(login="john_doe", engine=engine)

    assert user
    assert user.id == 1

    updated_user = update_user_tokens(login=user.login, engine=engine)

    assert updated_user
    assert updated_user.id == user.id
    assert updated_user.refresh_token != user.refresh_token
    assert updated_user.access_token != user.access_token
