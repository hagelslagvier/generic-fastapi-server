from typing import List

from fastapi import Depends
from injector import Injector
from pydantic import NonNegativeInt, PositiveInt
from sqlalchemy.orm import Session

from app.db.orm.crud.common import UserCRUD
from app.endpoints.custom import Router
from app.endpoints.users.schema import UserSchemaInput, UserSchemaOutput

router = Router(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
def read_many(
    skip: NonNegativeInt = 0,
    take: PositiveInt = 5,
    injector: Injector = Depends(lambda: router.injector),
) -> List[UserSchemaOutput]:
    users = UserCRUD(session=injector.get(Session)).read_many(skip=skip, take=take)
    response = [UserSchemaOutput(**user.__dict__) for user in users]
    return response


@router.get("/{id}")
def read_one(
    id: int,
    injector: Injector = Depends(lambda: router.injector),
) -> UserSchemaOutput:
    user = UserCRUD(session=injector.get(Session)).read(id=id)
    response = UserSchemaOutput(**user.__dict__)

    return response


@router.post("/")
def create(
    user_schema: UserSchemaInput,
    injector: Injector = Depends(lambda: router.injector),
) -> UserSchemaOutput:
    user = UserCRUD(session=injector.get(Session)).create(
        payload=user_schema.dict(exclude_none=True)
    )
    response = UserSchemaOutput(**user.__dict__)

    return response


@router.put("/{id}")
def put(
    id: int,
    user_schema: UserSchemaInput,
    injector: Injector = Depends(lambda: router.injector),
) -> UserSchemaOutput:
    user = UserCRUD(session=injector.get(Session)).update(
        id=id,
        payload=user_schema.dict(exclude_none=True),
    )
    response = UserSchemaOutput(**user.__dict__)

    return response


@router.delete("/{id}")
def delete(
    id: int,
    injector: Injector = Depends(lambda: router.injector),
) -> UserSchemaOutput:
    user = UserCRUD(session=injector.get(Session)).delete(id=id)
    response = UserSchemaOutput(**user.__dict__)

    return response
