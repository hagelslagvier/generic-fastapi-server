from fastapi import APIRouter, Depends
from injector import Injector
from pydantic import NonNegativeInt, PositiveInt
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from app.database.orm.crud.generic import session_factory
from app.dependencies.injector import make_injector
from app.endpoints.users.schema import UserSchemaInput, UserSchemaOutput
from app.interactors.users.interactors import UserCRUD

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
def get_many(
    skip: NonNegativeInt = 0,
    take: PositiveInt = 5,
    injector: Injector = Depends(make_injector),
) -> list[UserSchemaOutput]:
    users = UserCRUD(session=injector.get(Session)).read_many(skip=skip, take=take)
    response = [UserSchemaOutput(**user.__dict__) for user in users]
    return response


@router.get("/{id}")
def get_one(
    id: int,
    injector: Injector = Depends(make_injector),
) -> UserSchemaOutput:
    user = UserCRUD(session=injector.get(Session)).read(id=id)
    response = UserSchemaOutput(**user.__dict__)
    return response


@router.post("/")
def post(
    user_schema: UserSchemaInput,
    injector: Injector = Depends(make_injector),
) -> UserSchemaOutput:
    with session_factory(bind=injector.get(Engine)) as session:
        user = UserCRUD(session=session).create(
            payload=user_schema.model_dump(exclude_none=True)
        )
    response = UserSchemaOutput(**user.__dict__)
    return response


@router.put("/{id}")
def put(
    id: int,
    user_schema: UserSchemaInput,
    injector: Injector = Depends(make_injector),
) -> UserSchemaOutput:
    with session_factory(bind=injector.get(Engine)) as session:
        user = UserCRUD(session=session).update(
            id=id,
            payload=user_schema.model_dump(),
        )
    response = UserSchemaOutput(**user.__dict__)
    return response


@router.delete("/{id}")
def delete(
    id: int,
    injector: Injector = Depends(make_injector),
) -> UserSchemaOutput:
    with session_factory(bind=injector.get(Engine)) as session:
        user = UserCRUD(session=session).delete(id=id)
    response = UserSchemaOutput(**user.__dict__)
    return response
