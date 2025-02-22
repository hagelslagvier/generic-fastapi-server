#!/usr/bin/env python3

import logging
import os
from pathlib import Path

import typer
from dotenv import load_dotenv

from app.database.utils.introspection import make_erd as do_make_erd
from app.database.utils.maintenance import (
    create_user,
    delete_user,
    read_user,
    update_user,
    update_user_tokens,
)

ROOT_PATH = Path(__file__).parents[3]
ENV_DEVELOPMENT_PATH = ROOT_PATH / ".env.develop"

logging.basicConfig()
logging.root.setLevel(logging.INFO)

logger = logging.getLogger("database.utils.introspection")

for path in [
    ENV_DEVELOPMENT_PATH,
]:
    if path.exists() and path.is_file():
        load_dotenv(path)

HOUR = 60
WEEK = 60 * 24 * 7

DATABASE_URL = os.environ["DB_URL"]
ERD_PATH = ROOT_PATH / "ERD.svg"


cli = typer.Typer()


@cli.command()
def create(
    login: str,
    password: str,
    email: str = "undefined@email.com",
    refresh_token_ttl: int = WEEK,
    access_token_ttl: int = HOUR,
    is_admin: bool = False,
) -> None:
    create_user(
        login=login,
        password=password,
        email=email,
        refresh_token_ttl=refresh_token_ttl,
        access_token_ttl=access_token_ttl,
        is_admin=is_admin,
    )


@cli.command()
def read(
    login: str,
) -> None:
    read_user(login=login)


@cli.command()
def update(
    login: str,
    password: str | None = None,
    email: str | None = None,
    refresh_token: str | None = None,
    access_token: str | None = None,
    is_admin: bool = False,
) -> None:
    update_user(
        login=login,
        password=password,
        email=email,
        refresh_token=refresh_token,
        access_token=access_token,
        is_admin=is_admin,
    )


@cli.command()
def delete(login: str) -> None:
    delete_user(login=login)


@cli.command()
def update_tokens(login: str) -> None:
    update_user_tokens(login=login)


@cli.command()
def make_erd(db_url: str = DATABASE_URL, erd_path: str = str(ERD_PATH)) -> None:
    do_make_erd(db_url=db_url, erd_path=erd_path)


if __name__ == "__main__":
    cli()
