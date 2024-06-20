from typing import List
from pydantic import NonNegativeInt
from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.db import make_session
from app.endpoints.users.schema import UserSchemaOutput, UserSchemaInput
from app.db.orm.crud.common import UserCRUD


from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
def read_many(
    skip: NonNegativeInt = 0,
    take: int = 5,
    session: Session = Depends(make_session),
) -> List[UserSchemaOutput]:
    users = UserCRUD().read(session=session, skip=skip, take=take)
    response = [UserSchemaOutput(**user.__dict__) for user in users]
    return response


@router.get("/{id}")
def read_one(id: int, session: Session = Depends(make_session)) -> UserSchemaOutput:
    user = UserCRUD().get(session=session, id=id)
    response = UserSchemaOutput(**user.__dict__)

    return response


@router.post("/")
def create(
    user_schema: UserSchemaInput, session: Session = Depends(make_session)
) -> UserSchemaOutput:
    user = UserCRUD().create(
        session=session, payload=user_schema.dict(exclude_none=True)
    )
    response = UserSchemaOutput(**user.__dict__)

    return response


@router.put("/{id}")
def put(
    id: int, user_schema: UserSchemaInput, session: Session = Depends(make_session)
) -> UserSchemaOutput:
    user = UserCRUD().update(
        id=id, payload=user_schema.dict(exclude_none=True), session=session
    )
    response = UserSchemaOutput(**user.__dict__)

    return response


@router.delete("/")
def delete(id: int, session: Session = Depends(make_session)) -> UserSchemaOutput:
    user = UserCRUD().delete(id=id, session=session)
    response = UserSchemaOutput(**user.__dict__)

    return response
