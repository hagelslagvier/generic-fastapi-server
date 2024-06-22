from typing import Any, Dict, Generator, Generic, Optional, Type, TypeVar, Union

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.orm.crud.errors import DoesNotExistError

MT = TypeVar("MT")  # ORM Model Type


class GenericCRUD(Generic[MT]):
    def _get_model(self) -> Type[MT]:
        (bases,) = self.__orig_bases__  # type:ignore
        (model,) = bases.__args__

        return model  # type:ignore

    def count(self, session: Session) -> int:
        model = self._get_model()
        query = select(func.count()).select_from(model)
        count = session.execute(query).scalar() or 0

        return count

    def create(self, session: Session, payload: Dict[str, Any]) -> MT:
        model = self._get_model()

        instance = model(**payload)

        session.add(instance)
        session.commit()
        session.refresh(instance)

        return instance

    def get(
        self, session: Session, id: Union[int, str]
    ) -> MT:  # TODO: rename -> read_one
        model = self._get_model()

        instance = session.get(model, id)

        if not instance:
            raise DoesNotExistError(
                f"Instance of model='{model}' with id='{id}' was not found"
            )

        return instance

    def read(  # TODO: rename -> read_many
        self,
        session: Session,
        where: Optional[Any] = None,
        order_by: Optional[Any] = None,
        take: int = 10,
        skip: int = 0,
    ) -> Generator[MT, None, None]:
        model = self._get_model()

        query = select(model)
        if where is not None:
            query = query.filter(where)

        if order_by is not None:
            query = query.order_by(order_by)

        if skip:
            query = query.offset(skip)

        if take:
            query = query.limit(take)

        items = (item for item in session.execute(query).scalars())

        return items

    def update(
        self, session: Session, id: Union[int, str], payload: Dict[str, Any]
    ) -> MT:
        instance = self.get(session=session, id=id)

        for k, v in payload.items():
            setattr(instance, k, v)

        session.add(instance)
        session.commit()
        session.refresh(instance)

        return instance

    def delete(self, session: Session, id: Union[int, str]) -> MT:
        instance = self.get(session=session, id=id)

        session.delete(instance)
        session.commit()

        return instance
