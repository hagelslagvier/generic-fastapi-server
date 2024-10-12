import pytest
from sqlalchemy import Engine

from app.db.orm.crud.generic import session_factory
from app.interactors.users.interactors import UserCRUD


@pytest.fixture
def content(engine: Engine) -> None:
    with session_factory(bind=engine) as session:
        user_crud = UserCRUD(session=session)
        user_crud.create_many(
            payload=[
                {
                    "login": f"user-{index}",
                    "password": f"password-{index}",
                    "email": f"user-{index}@abc.com",
                }
                for index in range(5)
            ]
        )
