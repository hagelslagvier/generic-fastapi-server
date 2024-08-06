from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, Generic, Optional, Sequence, TypeVar, Union

T = TypeVar("T")


class CRUDInterface(ABC, Generic[T]):
    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def create(self, payload: Dict[str, Any]) -> T:
        pass

    @abstractmethod
    def create_many(self, payload: Sequence[Dict[str, Any]]) -> Sequence[T]:
        pass

    @abstractmethod
    def read(self, id: Union[int, str]) -> T:
        pass

    @abstractmethod
    def read_many(
        self,
        where: Optional[Any] = None,
        order_by: Optional[Any] = None,
        skip: int = 0,
        take: int = 10,
    ) -> Generator[T, None, None]:
        pass

    @abstractmethod
    def update(self, id: Union[int, str], payload: Dict[str, Any]) -> T:
        pass

    @abstractmethod
    def delete(self, id: Union[int, str]) -> T:
        pass
