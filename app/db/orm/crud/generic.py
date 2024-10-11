from collections.abc import Generator, Sequence
from contextlib import contextmanager
from typing import Any, TypeVar

from sqlalchemy import Engine, func, select
from sqlalchemy.orm import Session

from app.db.orm.crud.errors import DoesNotExistError
from app.db.orm.crud.interfaces import CRUDInterface
from app.db.orm.models import Base

T = TypeVar("T", bound=Base)


@contextmanager
def session_factory(bind: Engine) -> Generator[Session, None, None]:
    with Session(bind=bind, expire_on_commit=False) as session:
        try:
            session.begin()
            yield session
        except:
            session.rollback()
            raise
        else:
            session.commit()


class GenericCRUD(CRUDInterface[T]):
    def __init__(self, session: Session) -> None:
        self.session = session

    def _get_model(self) -> type[T]:
        (bases,) = self.__orig_bases__  # type:ignore
        (model,) = bases.__args__
        return model  # type:ignore

    def count(self) -> int:
        model = self._get_model()
        query = select(func.count()).select_from(model)
        count = self.session.execute(query).scalar() or 0
        return count

    def create(self, *, payload: dict[str, Any]) -> T:
        model = self._get_model()
        instance = model.new(**payload)
        self.session.add(instance)
        self.session.flush()
        return instance

    def create_many(self, *, payload: Sequence[dict[str, Any]]) -> Sequence[T]:
        model = self._get_model()
        instances = [model.new(**item) for item in payload]
        self.session.add_all(instances)
        self.session.flush()
        return instances

    def read(self, id: int | str) -> T:
        model = self._get_model()
        instance = self.session.get(model, id)
        if not instance:
            raise DoesNotExistError(
                f"Instance of model='{model}' with id='{id}' was not found"
            )
        return instance

    def read_many(
        self,
        *,
        where: Any | None = None,
        order_by: Any | None = None,
        skip: int = 0,
        take: int = 10,
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

    def update(self, id: int | str, *, payload: dict[str, Any]) -> T:
        instance = self.read(id=id)
        instance.update(**payload)
        self.session.add(instance)
        self.session.flush()
        return instance

    def delete(self, id: int | str) -> T:
        instance = self.read(id=id)
        self.session.delete(instance)
        self.session.flush()
        return instance
