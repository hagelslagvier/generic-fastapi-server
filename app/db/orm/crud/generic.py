from typing import Any, Dict, Generator, List, Optional, Sequence, Type, TypeVar, Union

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.orm.crud.errors import DoesNotExistError
from app.db.orm.crud.interfaces import CRUDInterface

T = TypeVar("T")  # ORM Model Type


class GenericCRUD(CRUDInterface[T]):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _get_model(self) -> Type[T]:
        (bases,) = self.__orig_bases__  # type:ignore
        (model,) = bases.__args__

        return model  # type:ignore

    def count(self) -> int:
        model = self._get_model()
        query = select(func.count()).select_from(model)
        count = self.session.execute(query).scalar() or 0

        return count

    def create(self, payload: Dict[str, Any]) -> T:
        model = self._get_model()

        instance = model(**payload)

        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)

        return instance

    def create_many(self, payload: List[Dict[str, Any]]) -> Sequence[T]:
        model = self._get_model()

        instances = [model(**item) for item in payload]

        self.session.add_all(instances)
        self.session.commit()

        for instance in instances:
            self.session.refresh(instance)

        return instances

    def read(self, id: Union[int, str]) -> T:
        model = self._get_model()

        instance = self.session.get(model, id)

        if not instance:
            raise DoesNotExistError(
                f"Instance of model='{model}' with id='{id}' was not found"
            )

        return instance

    def read_many(
        self,
        where: Optional[Any] = None,
        order_by: Optional[Any] = None,
        take: int = 10,
        skip: int = 0,
    ) -> Generator[T, None, None]:
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

        items = (item for item in self.session.execute(query).scalars())

        return items

    def update(self, id: Union[int, str], payload: Dict[str, Any]) -> T:
        instance = self.read(id=id)

        for k, v in payload.items():
            setattr(instance, k, v)

        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)

        return instance

    def delete(self, id: Union[int, str]) -> T:
        instance = self.read(id=id)

        self.session.delete(instance)
        self.session.commit()

        return instance
