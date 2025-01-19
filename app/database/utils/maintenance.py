import logging
from datetime import timedelta
from typing import Any

from inzicht import session_factory
from sqlalchemy import Engine

from app.assembly import root_injector
from app.database.orm.models import User
from app.interactors.auth.interfaces import (
    SecretManagerInterface,
    TokenManagerInterface,
)
from app.interactors.users.interactors import UserCRUD

HOUR = 60
WEEK = 60 * 24 * 7

logging.basicConfig()
logging.root.setLevel(logging.INFO)

logger = logging.getLogger("database.utils.maintenance")


def create_user(
    login: str,
    password: str,
    email: str = "undefined@email.com",
    refresh_token_ttl: int = WEEK,
    access_token_ttl: int = HOUR,
    is_admin: bool = False,
    engine: Engine | None = None,
) -> User:
    engine = engine or root_injector.get(Engine)
    secret_manager = root_injector.get(SecretManagerInterface)
    token_manager = root_injector.get(TokenManagerInterface)

    password = secret_manager.make_hash(secret=password)

    refresh_token_timedelta = timedelta(minutes=refresh_token_ttl)
    refresh_token = token_manager.create_token(payload={}, ttl=refresh_token_timedelta)

    access_token_timedelta = timedelta(minutes=access_token_ttl)
    access_token = token_manager.create_token(payload={}, ttl=access_token_timedelta)

    payload = {
        "login": login,
        "password": password,
        "email": email,
        "is_email_confirmed": True,
        "refresh_token": refresh_token,
        "access_token": access_token,
        "is_admin": is_admin,
    }

    with session_factory(bind=engine) as session:
        user = UserCRUD(session=session).create(payload=payload)

    logger.info(f"User created: {user}")

    return user  # type: ignore


def read_user(login: str, engine: Engine | None = None) -> User | None:
    engine = engine or root_injector.get(Engine)

    with session_factory(bind=engine) as session:
        users = UserCRUD(session=session).read_many(where=User.login == login)
        found = list(users)
        if len(found) == 1:
            [user] = found
            logger.info(f"User with login '{login}' retrieved: {user}")
            return user  # type: ignore
        else:
            logger.error(f"User with login '{login}' not found")
            return None


def update_user(
    login: str,
    password: str | None = None,
    email: str | None = None,
    refresh_token: str | None = None,
    access_token: str | None = None,
    is_admin: bool = False,
    engine: Engine | None = None,
) -> User | None:
    engine = engine or root_injector.get(Engine)

    with session_factory(bind=engine) as session:
        users = UserCRUD(session=session).read_many(where=User.login == login)
        found = list(users)
        if len(found) == 1:
            [user] = found
        else:
            logger.error(f"User with login '{login}' not found")
            return None

    payload: dict[str, Any] = {}

    if password:
        payload["password"] = password
    if email:
        payload["email"] = email
    if refresh_token:
        payload["refresh_token"] = refresh_token
    if access_token:
        payload["access_token"] = access_token
    if is_admin is not None:
        payload["is_admin"] = is_admin

    if payload:
        payload["login"] = login
    else:
        logger.error(f"No attributes set to update user with login '{login}'")

    with session_factory(bind=engine) as session:
        user = UserCRUD(session=session).update(id=user.id, payload=payload)

    logger.info(f"User with login '{login}' updated: {user}")

    return user  # type: ignore


def delete_user(
    login: str,
    engine: Engine | None = None,
) -> User | None:
    engine = engine or root_injector.get(Engine)

    with session_factory(bind=engine) as session:
        users = UserCRUD(session=session).read_many(where=User.login == login)
        found = list(users)
        if len(found) == 1:
            [user] = found
        else:
            logger.error(f"User with login '{login}' not found")
            return None

        deleted = UserCRUD(session=session).delete(id=user.id)
        logger.info(f"User with login '{login}' deleted: {user}")
        return deleted  # type: ignore


def update_user_tokens(login: str, engine: Engine | None = None) -> User | None:
    engine = engine or root_injector.get(Engine)
    token_manager = root_injector.get(TokenManagerInterface)

    with session_factory(bind=engine) as session:
        users = UserCRUD(session=session).read_many(where=User.login == login)
        found = list(users)
        if len(found) == 1:
            [user] = found
        else:
            logger.error(f"User with login '{login}' not found")
            return None

    refresh_token_timedelta = timedelta(minutes=WEEK)
    refresh_token = token_manager.create_token(payload={}, ttl=refresh_token_timedelta)

    access_token_timedelta = timedelta(minutes=HOUR)
    access_token = token_manager.create_token(payload={}, ttl=access_token_timedelta)

    payload = {
        "login": login,
        "refresh_token": refresh_token,
        "access_token": access_token,
    }

    with session_factory(bind=engine) as session:
        user = UserCRUD(session=session).update(id=user.id, payload=payload)

    logger.info(f"User tokens updated: {user}")

    return user  # type: ignore
