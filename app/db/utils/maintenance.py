from sqlalchemy import Engine

from app.assembly import root_injector
from app.db.orm.crud.generic import session_factory
from app.endpoints.users.schema import UserSchemaOutput
from app.interactors.users.interactors import UserCRUD


def create_super_user(
    login: str,
    password: str,
    email: str | None = None,
    engine: Engine = root_injector.get(Engine),
) -> dict:
    payload = {
        "login": login,
        "password": password,
        "is_admin": True,
        "is_email_confirmed": True,
    }
    if email:
        payload.update({"email": email})

    with session_factory(bind=engine) as session:
        user_crud = UserCRUD(session=session)
        user_model = user_crud.create(payload=payload)
        user = UserSchemaOutput(**user_model.__dict__).model_dump()

    return user
