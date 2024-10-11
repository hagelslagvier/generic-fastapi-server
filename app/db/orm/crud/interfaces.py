from abc import ABC, abstractmethod
from collections.abc import Generator, Sequence
from typing import Any, Generic, TypeVar

from app.db.orm.models import Base

T = TypeVar("T", bound=Base)


class CRUDInterface(ABC, Generic[T]):
    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def create(self, *, payload: dict[str, Any]) -> T:
        pass

    @abstractmethod
    def create_many(self, *, payload: Sequence[dict[str, Any]]) -> Sequence[T]:
        pass

    @abstractmethod
    def read(self, id: int | str) -> T:
        pass

    @abstractmethod
    def read_many(
        self,
        *,
        where: Any | None = None,
        order_by: Any | None = None,
        skip: int = 0,
        take: int = 10,
    ) -> Generator[T, None, None]:
        pass

    @abstractmethod
    def update(self, id: int | str, *, payload: dict[str, Any]) -> T:
        pass

    @abstractmethod
    def delete(self, id: int | str) -> T:
        pass
